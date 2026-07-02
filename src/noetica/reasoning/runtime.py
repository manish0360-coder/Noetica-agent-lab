"""ReasoningRuntime — the FORM of reasoning (§6.7, DN-7).

Iterates inference (via an injected ModelRouter), applies a verification seam (an injected
Verifier), and backtracks/retries within a budget. It is a control plane OVER the shared
State substrate (DN-7 blackboard): it reads Context/State and records step outcomes to State
with provenance. It owns NONE of: planning, reflection, memory, knowledge, context, tool
execution, state, the verification protocol/oracle, or the runtime lifecycle. All
capabilities are consumed by dependency injection; no other platform mechanism is imported.
No conversation loop, no autonomous agent, no homunculus, no semantic self-critique, no
domain logic.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from noetica.interfaces.budget import BudgetMeter
from noetica.interfaces.context import ContextAssembler
from noetica.interfaces.provenance import Provenance
from noetica.interfaces.router import ModelRequest, ModelRouter
from noetica.interfaces.state import StateSubstrate
from noetica.interfaces.verification import VerdictStatus, Verifier
from noetica.reasoning.models import ReasoningResult, ReasoningStep

MessageBuilder = Callable[[Any, Any], tuple[Mapping[str, Any], ...]]


def _default_messages(goal: Any, context: Any) -> tuple[Mapping[str, Any], ...]:
    """Generic, non-domain assembly of a model request: optional context + the goal."""
    messages: list[Mapping[str, Any]] = []
    items = getattr(context, "items", ()) if context is not None else ()
    if items:
        joined = "\n".join(str(getattr(item, "content", item)) for item in items)
        messages.append({"role": "system", "content": joined})
    messages.append({"role": "user", "content": str(goal)})
    return tuple(messages)


class ReasoningRuntime:
    """A bounded reasoning loop: infer -> verify -> (backtrack/retry) until PASSED, budget
    exhausted, or max_steps. Consumes Router/Verifier (+ optional Context/Budget/State) by
    injection. Satisfies the `ReasoningLoop` interface (step/run)."""

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
        """One inference iteration over the given working state/goal (form only)."""
        return self._infer(state, 0)

    def run(self, goal: Any, max_steps: int = 1) -> ReasoningResult:
        steps: list[ReasoningStep] = []
        for i in range(max_steps):
            if self._budget is not None and self._budget.exceeded():
                break  # meta-control: stop thinking when the budget is exhausted
            step = self._infer(goal, i)
            steps.append(step)
            if self._state is not None:
                self._state.put(
                    f"reasoning:step:{i}",
                    {"candidate": step.candidate, "status": step.verdict.status.value},
                    step.provenance,
                )
            if step.verdict.status is VerdictStatus.PASSED:
                return ReasoningResult(goal=str(goal), success=True, steps=tuple(steps), final=step)
        final = steps[-1] if steps else None
        return ReasoningResult(goal=str(goal), success=False, steps=tuple(steps), final=final)

    def _infer(self, goal: Any, index: int) -> ReasoningStep:
        context = self._context.assemble(goal, self._token_budget) if self._context is not None else None
        response = self._router.route(ModelRequest(messages=self._messages(goal, context)))
        candidate = response.text
        verdict = self._verifier.verify(goal, candidate)  # verification seam (invocation only)
        provenance = Provenance(source="reasoning", transform=f"step:{index}", inputs=(str(goal),))
        return ReasoningStep(index=index, candidate=candidate, verdict=verdict, provenance=provenance)
