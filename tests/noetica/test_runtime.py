"""PE-21 unit tests — Runtime integrator (§6.3). Injected mechanisms; ReferenceVerifier only."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from noetica.budget import InMemoryBudgetMeter
from noetica.episodes import InMemoryEpisodeStore
from noetica.guardrails import GuardrailEngine, deny_all
from noetica.interfaces.runtime import Runtime as RuntimeProto
from noetica.interfaces.tool import ToolResult
from noetica.interfaces.verification import Verdict, VerdictStatus
from noetica.memory import InMemoryMemoryStore, UnfilteredWriteFilter
from noetica.runtime import (
    EpisodeHandle,
    Propose,
    Runtime,
    SkillRequest,
    Stop,
    TerminalReason,
    ToolRequest,
    YieldSignal,
)
from noetica.skills import SkillRuntime
from noetica.state import InMemoryStateSubstrate
from noetica.tools import ToolRuntime
from noetica.verification import ReferenceVerifier


def _verifier() -> ReferenceVerifier:
    return ReferenceVerifier(default=Verdict(status=VerdictStatus.FAILED),
                             script={"good": Verdict(status=VerdictStatus.PASSED)},
                             key_fn=lambda task, candidate: str(candidate))


@dataclass
class _EchoTool:
    name: str = "echo"
    def invoke(self, **kwargs: Any) -> ToolResult:
        return ToolResult(ok=True, output=kwargs.get("value"))


@dataclass
class _MarkerSkill:
    name: str = "mark"
    def apply(self, state: Any, **kwargs: Any) -> Any:
        return "marked"


def _always(activation: Any):
    return lambda handle: activation


def test_runtime_satisfies_interface() -> None:
    assert isinstance(Runtime(activator=_always(Propose("good")), verifier=_verifier()), RuntimeProto)


def test_run_success_persists_and_writes_memory() -> None:
    store = InMemoryEpisodeStore()
    mem = InMemoryMemoryStore(UnfilteredWriteFilter())
    rt = Runtime(activator=_always(Propose("good")), verifier=_verifier(),
                 episode_store=store, memory=mem)
    result = rt.run("g")
    assert result.success and result.terminal is TerminalReason.PASSED
    assert result.episode is not None and result.episode.provenance.source == "runtime"
    assert len(list(store)) == 1 and len(mem) == 1


def test_tool_request_dispatched_by_runtime_not_reasoning() -> None:
    tools = ToolRuntime(InMemoryBudgetMeter(100.0))
    tools.register(_EchoTool())
    state = InMemoryStateSubstrate()
    calls = {"n": 0}

    def activator(handle: EpisodeHandle):
        calls["n"] += 1
        return ToolRequest("echo", {"value": 7}) if calls["n"] == 1 else Propose("good")

    rt = Runtime(activator=activator, verifier=_verifier(), tools=tools, state=state)
    result = rt.run("g", max_steps=4)
    assert result.success
    # runtime dispatched the tool and wrote the result to the blackboard
    assert state.get_record("episode:%s:dispatch:0" % result.episode_id) is not None


def test_skill_request_dispatched() -> None:
    skills = SkillRuntime(InMemoryStateSubstrate(), ToolRuntime(InMemoryBudgetMeter(100.0)))
    skills.register(_MarkerSkill())
    calls = {"n": 0}

    def activator(handle: EpisodeHandle):
        calls["n"] += 1
        return SkillRequest("mark") if calls["n"] == 1 else Propose("good")

    rt = Runtime(activator=activator, verifier=_verifier(), skills=skills)
    assert rt.run("g", max_steps=4).success


def test_circuit_breaker_step_limit() -> None:
    rt = Runtime(activator=_always(Propose("bad")), verifier=_verifier())
    result = rt.run("g", max_steps=3)
    assert result.success is False and result.terminal is TerminalReason.STEP_LIMIT and result.steps == 3


def test_circuit_breaker_budget() -> None:
    rt = Runtime(activator=_always(Propose("good")), verifier=_verifier(),
                 budget=InMemoryBudgetMeter(0.0))
    result = rt.run("g", max_steps=5)
    assert result.terminal is TerminalReason.BUDGET_EXCEEDED and result.success is False


def test_oversight_halts_at_setup() -> None:
    guard = GuardrailEngine(oversight=(deny_all("boundary", "no"),))
    rt = Runtime(activator=_always(Propose("good")), verifier=_verifier(), guardrail=guard)
    result = rt.run("g")
    assert result.terminal is TerminalReason.OVERSIGHT_DENIED and result.success is False


def test_stop_activation_ends_run() -> None:
    rt = Runtime(activator=_always(Stop("done")), verifier=_verifier())
    result = rt.run("g", max_steps=5)
    assert result.terminal is TerminalReason.STOPPED


def test_submit_interface_path() -> None:
    rt = Runtime(activator=_always(Propose("x")), verifier=_verifier())
    rt.start_episode("g")
    assert rt.submit("good").status is VerdictStatus.PASSED


def test_step_yields_signal() -> None:
    rt = Runtime(activator=_always(Propose("bad")), verifier=_verifier())
    eid = rt.start_episode("g")
    sig = rt.step(eid)
    assert isinstance(sig, YieldSignal) and sig.reason == "verified_retry"
