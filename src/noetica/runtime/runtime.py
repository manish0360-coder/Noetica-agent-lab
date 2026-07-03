"""Runtime — the integrator (§6.3, PE-21 spec). Owns operation order; owns no cognition.

Drives the frozen state machine: setup -> [guard -> activate -> (dispatch tool/skill |
verify) -> yield]* -> persist -> teardown. All cognition (activation), verification, tools,
skills, guardrails, budget, memory, observability and the substrate are INJECTED via
interfaces (DI graph). The Runtime dispatches on the injected activation's TYPE and writes
results to the State blackboard; it implements no inference/planning/critique/retrieval/
model call. Non-autonomous: bounded by max_steps + BudgetMeter + the caller pump (yield
protocol) — infinite oscillation is impossible.
"""
from __future__ import annotations

import uuid
from collections.abc import Callable
from typing import Any

from noetica.interfaces.budget import BudgetMeter
from noetica.interfaces.episode import Episode, EpisodeStore
from noetica.interfaces.guardrail import Guardrail
from noetica.interfaces.memory import MemoryStore
from noetica.interfaces.observability import Observability
from noetica.interfaces.provenance import Provenance
from noetica.interfaces.state import StateSubstrate
from noetica.interfaces.verification import Verdict, VerdictStatus, Verifier
from noetica.runtime.models import (
    EpisodeHandle,
    EpisodeState,
    Propose,
    RunResult,
    SkillRequest,
    Stop,
    StepOutcome,
    TerminalReason,
    ToolRequest,
    YieldSignal,
)
from noetica.skills import SkillRuntime
from noetica.tools import ToolRuntime

Activation = ToolRequest | SkillRequest | Propose | Stop
Activator = Callable[[EpisodeHandle], Activation]

DEFAULT_MAX_STEPS = 8


class Runtime:
    """Satisfies the `Runtime` interface (start_episode/submit/end_episode) and adds the
    step/run drivers. Injected mechanisms only; no cognition implemented here."""

    def __init__(
        self,
        *,
        activator: Activator,
        verifier: Verifier,
        guardrail: Guardrail | None = None,
        budget: BudgetMeter | None = None,
        observability: Observability | None = None,
        state: StateSubstrate | None = None,
        episode_store: EpisodeStore | None = None,
        memory: MemoryStore | None = None,
        tools: ToolRuntime | None = None,
        skills: SkillRuntime | None = None,
        max_steps: int = DEFAULT_MAX_STEPS,
    ) -> None:
        self._activator = activator
        self._verifier = verifier
        self._guardrail = guardrail
        self._budget = budget
        self._obs = observability
        self._state = state
        self._store = episode_store
        self._memory = memory
        self._tools = tools
        self._skills = skills
        self._max_steps = max_steps
        self._episodes: dict[str, EpisodeHandle] = {}
        self._built: dict[str, Episode] = {}
        self._current: str | None = None

    # ── Runtime interface ────────────────────────────────────────────────────────
    def start_episode(self, goal: Any) -> str:
        episode_id = uuid.uuid4().hex
        handle = EpisodeHandle(episode_id=episode_id, goal=str(goal), state=EpisodeState.SETUP)
        self._episodes[episode_id] = handle
        self._current = episode_id
        self._write(handle, "goal", {"goal": str(goal)}, "setup")
        self._log("episode.start", episode_id=episode_id)
        if self._guardrail is not None and not self._guardrail.check(
            {"episode": episode_id, "phase": "setup"}
        ).allowed:
            handle.terminal = TerminalReason.OVERSIGHT_DENIED
            handle.state = EpisodeState.HALTED
        else:
            handle.state = EpisodeState.GUARD_CHECK
        return episode_id

    def submit(self, candidate: Any) -> Verdict:
        handle = self._require(self._current)
        return self._verify(handle, str(candidate))

    def end_episode(self, episode_id: str) -> None:
        handle = self._require(episode_id)
        episode = self._build_and_persist(handle)
        self._built[episode_id] = episode
        handle.state = EpisodeState.FAILED if handle.terminal is TerminalReason.INFRA_ERROR else EpisodeState.DONE
        self._log("episode.end", episode_id=episode_id,
                  terminal=(handle.terminal.value if handle.terminal else ""))

    # ── drivers (yield protocol) ─────────────────────────────────────────────────
    def step(self, episode_id: str) -> YieldSignal:
        handle = self._require(episode_id)
        if handle.terminal is not None:
            return YieldSignal("terminated", episode_id, handle.state)
        if self._budget is not None and self._budget.exceeded():
            handle.terminal = TerminalReason.BUDGET_EXCEEDED
            handle.state = EpisodeState.TEARDOWN
            return YieldSignal("budget_exhausted", episode_id, handle.state)
        if self._guardrail is not None and not self._guardrail.check(
            {"episode": episode_id, "step": handle.step_index}
        ).allowed:
            handle.terminal = TerminalReason.OVERSIGHT_DENIED
            handle.state = EpisodeState.HALTED
            return YieldSignal("oversight_halt", episode_id, handle.state)

        handle.state = EpisodeState.ACTIVATE
        activation = self._activator(handle)
        index = handle.step_index
        handle.step_index += 1

        if isinstance(activation, Stop):
            handle.terminal = TerminalReason.STOPPED
            handle.state = EpisodeState.TEARDOWN
            return YieldSignal("stopped", episode_id, handle.state)
        if isinstance(activation, (ToolRequest, SkillRequest)):
            handle.state = EpisodeState.DISPATCH
            result = self._dispatch(activation)
            provenance = self._write(handle, f"dispatch:{index}", {"result": repr(result)}, f"dispatch:{index}")
            handle.outcomes.append(StepOutcome(index=index, kind="dispatch", detail=result, provenance=provenance))
            handle.state = EpisodeState.YIELD
            return YieldSignal("dispatched", episode_id, handle.state)
        if isinstance(activation, Propose):
            self._verify(handle, activation.candidate)
            reason = "verified_pass" if handle.terminal is TerminalReason.PASSED else "verified_retry"
            return YieldSignal(reason, episode_id, handle.state)

        handle.terminal = TerminalReason.INFRA_ERROR
        handle.state = EpisodeState.FAILED
        return YieldSignal("infra_error", episode_id, handle.state)

    def run(self, goal: Any, max_steps: int | None = None) -> RunResult:
        episode_id = self.start_episode(goal)
        handle = self._episodes[episode_id]
        limit = max_steps if max_steps is not None else self._max_steps
        for _ in range(limit):                       # circuit breaker: step limit
            if handle.terminal is not None:
                break
            self.step(episode_id)
            if handle.terminal is not None:
                break
        if handle.terminal is None:
            handle.terminal = TerminalReason.STEP_LIMIT
        self.end_episode(episode_id)
        return RunResult(
            episode_id=episode_id,
            goal=handle.goal,
            success=handle.terminal is TerminalReason.PASSED,
            terminal=handle.terminal,
            steps=handle.step_index,
            episode=self._built.get(episode_id),
        )

    def episode(self, episode_id: str) -> Episode | None:
        return self._built.get(episode_id)

    # ── internals ────────────────────────────────────────────────────────────────
    def _verify(self, handle: EpisodeHandle, candidate: str) -> Verdict:
        handle.state = EpisodeState.VERIFY
        verdict = self._verifier.verify(handle.goal, candidate)
        index = handle.step_index
        provenance = self._write(handle, f"verify:{index}", {"status": verdict.status.value}, f"verify:{index}")
        handle.outcomes.append(StepOutcome(index=index, kind="verify", detail=verdict, provenance=provenance))
        handle.final_verdict = verdict
        if verdict.status is VerdictStatus.PASSED:
            handle.terminal = TerminalReason.PASSED
            handle.state = EpisodeState.PERSIST
        else:
            handle.state = EpisodeState.YIELD
        return verdict

    def _dispatch(self, activation: ToolRequest | SkillRequest) -> Any:
        if isinstance(activation, ToolRequest):
            if self._tools is None:
                raise RuntimeError("ToolRequest emitted but no ToolRuntime injected")
            return self._tools.invoke(activation.tool, **activation.kwargs)
        if self._skills is None:
            raise RuntimeError("SkillRequest emitted but no SkillRuntime injected")
        return self._skills.apply(activation.skill, **activation.kwargs)

    def _build_and_persist(self, handle: EpisodeHandle) -> Episode:
        handle.state = EpisodeState.PERSIST
        verdict = handle.final_verdict if handle.final_verdict is not None else Verdict(status=VerdictStatus.NO_PATCH)
        episode = Episode(
            task_id=handle.goal,
            verdict=verdict,
            cost={"steps": handle.step_index},
            environment={"terminal": handle.terminal.value if handle.terminal else ""},
            provenance=Provenance(source="runtime", transform="episode", inputs=(handle.goal,)),
        )
        if self._store is not None:
            self._store.append(episode)
        if self._memory is not None:
            self._memory.write(episode)   # retention decided by the write-filter, not the Runtime
        return episode

    def _write(self, handle: EpisodeHandle, suffix: str, value: Any, transform: str) -> Provenance:
        provenance = Provenance(source="runtime", transform=transform, inputs=(handle.goal,))
        if self._state is not None:
            self._state.put(f"episode:{handle.episode_id}:{suffix}", value, provenance)
        return provenance

    def _log(self, event: str, **fields: Any) -> None:
        if self._obs is not None:
            self._obs.log(event, **fields)

    def _require(self, episode_id: str | None) -> EpisodeHandle:
        if episode_id is None or episode_id not in self._episodes:
            raise KeyError(f"unknown episode: {episode_id}")
        return self._episodes[episode_id]
