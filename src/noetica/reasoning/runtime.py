"""ReasoningRuntime — the FORM of reasoning (§6.7, DN-7).

Iterates inference (injected ModelRouter), applies a verification seam (injected Verifier),
and backtracks/retries within a budget. Retries are non-sterile but LOCAL and DETERMINISTIC:
each retry re-presents the previous candidate(s) and their raw verifier output (no semantic
self-critique, no reflection). Control plane over the shared State substrate (DN-7): each run
has a unique run_id so state keys never collide across concurrent/historical runs. Owns none
of planning/reflection/memory/knowledge/context/tool-execution/state/verification-oracle/
runtime-lifecycle; all capabilities injected; no other platform mechanism imported. No
conversation loop / agent / homunculus / domain logic.
"""
from __future__ import annotations

import uuid
from collections.abc import Callable, Mapping
from typing import Any

from noetica.interfaces.budget import BudgetMeter
from noetica.interfaces.context import ContextAssembler
from noetica.interfaces.provenance import Provenance
from noetica.interfaces.router import ModelRequest, ModelRouter
from noetica.interfaces.state import StateSubstrate
from noetica.interfaces.verification import VerdictStatus, Verifier
from noetica.reasoning.models import ReasoningResult, ReasoningStep

MessageBuilder = Callable[[Any, Any, tuple[ReasoningStep, ...]], tuple[Mapping[str, Any], ...]]

DEFAULT_MAX_STEPS = 3


def _default_messages(
    goal: Any, context: Any, history: tuple[ReasoningStep, ...]
) -> tuple[Mapping[str, Any], ...]:
    """Generic, non-domain request assembly: optional context, raw prior attempts, the goal.

    Prior attempts are re-presented verbatim (candidate + verdict status/detail) so retries
    are not sterile — this is deterministic, local feedback, NOT semantic self-critique.
    """
    messages: list[Mapping[str, Any]] = []
    items = getattr(context, "items", ()) if context is not None else ()
    if items:
        messages.append({"role": "system", "content": "\n".join(str(getattr(it, "content", it)) for it in items)})
    for prior in history:
        messages.append({
            "role": "system",
            "content": (
                f"previous_attempt verdict={prior.verdict.status.value} "
                f"detail={dict(prior.verdict.detail)}: {prior.candidate}"
            ),
        })
    messages.append({"role": "user", "content": str(goal)})
    return tuple(messages)


class ReasoningRuntime:
    """Bounded reasoning loop: infer -> verify -> (retry with prior feedback) until PASSED,
    budget exhausted, or max_steps. Satisfies the `ReasoningLoop` interface (step/run)."""

    def __init__(
        self,
        router: ModelRouter,
        verifier: Verifier,
        *,
        context: ContextAssembler | None = None,
        budget: BudgetMeter | None = None,
        state: StateSubstrate | None = None,
        token_budget: int = 0,
        message_builder: MessageBuilder | None = None,
    ) -> None:
        self._router = router
        self._verifier = verifier
        self._context = context
        self._budget = budget
        self._state = state
        self._token_budget = token_budget
        self._messages = message_builder if message_builder is not None else _default_messages

    def step(self, state: Any) -> ReasoningStep:
        """One inference iteration over the given working state/goal (no history)."""
        return self._infer(state, 0, ())

    def run(self, goal: Any, max_steps: int = DEFAULT_MAX_STEPS, run_id: str | None = None) -> ReasoningResult:
        rid = run_id if run_id is not None else uuid.uuid4().hex
        steps: list[ReasoningStep] = []
        for i in range(max_steps):
            if self._budget is not None and self._budget.exceeded():
                break  # meta-control: stop when the budget is exhausted
            step = self._infer(goal, i, tuple(steps))  # prior steps fed back into inference
            steps.append(step)
            if self._state is not None:
                self._state.put(
                    f"reasoning:{rid}:step:{i}",
                    {"candidate": step.candidate, "status": step.verdict.status.value},
                    step.provenance,
                )
            if step.verdict.status is VerdictStatus.PASSED:
                return ReasoningResult(goal=str(goal), success=True, run_id=rid, steps=tuple(steps), final=step)
        final = steps[-1] if steps else None
        return ReasoningResult(goal=str(goal), success=False, run_id=rid, steps=tuple(steps), final=final)

    def _infer(self, goal: Any, index: int, history: tuple[ReasoningStep, ...]) -> ReasoningStep:
        context = self._context.assemble(goal, self._token_budget) if self._context is not None else None
        response = self._router.route(ModelRequest(messages=self._messages(goal, context, history)))
        candidate = response.text
        verdict = self._verifier.verify(goal, candidate)  # verification seam (invocation only)
        provenance = Provenance(source="reasoning", transform=f"step:{index}", inputs=(str(goal),))
        return ReasoningStep(index=index, candidate=candidate, verdict=verdict, provenance=provenance)
