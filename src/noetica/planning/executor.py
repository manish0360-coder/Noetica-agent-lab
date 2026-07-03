"""SequentialExecutor — plan executor (form only, §6.8, DN-7).

Sequences a Plan's steps over the shared State substrate (blackboard). Each step's action is
run by an injected handler; the `reason` action delegates to an injected `ReasoningLoop`
(consumed by injection, DN-7). A reflection SEAM (post-step hook) is exposed for PE-20 to
plug into — planning does NOT import or implement reflection. Owns sequencing only: no
domain actions, no reasoning content, no runtime lifecycle.
"""
from __future__ import annotations

import uuid
from collections.abc import Callable, Mapping
from typing import Any

from noetica.interfaces.plan import Plan, Step
from noetica.interfaces.provenance import Provenance
from noetica.interfaces.reasoning import ReasoningLoop
from noetica.planning.models import ExecutionResult, StepOutcome

ActionHandler = Callable[[Step, Any], Any]
ReflectSeam = Callable[[StepOutcome], StepOutcome]


class ExecutorError(RuntimeError):
    """Base error for plan execution."""


class UnknownActionError(ExecutorError):
    """No handler (and no reasoning fallback) for a step's action."""


class SequentialExecutor:
    """Executes a Plan step-by-step over State; delegates `reason` to injected reasoning."""

    def __init__(
        self,
        *,
        handlers: Mapping[str, ActionHandler] | None = None,
        reasoning: ReasoningLoop | None = None,
        reflect: ReflectSeam | None = None,
    ) -> None:
        self._handlers: dict[str, ActionHandler] = dict(handlers or {})
        self._reasoning = reasoning
        self._reflect = reflect

    def execute(self, plan: Plan, state: Any, run_id: str | None = None) -> ExecutionResult:
        rid = run_id if run_id is not None else uuid.uuid4().hex
        outcomes: list[StepOutcome] = []
        for index, step in enumerate(plan.steps):
            result = self._run_step(step, state)
            provenance = Provenance(
                source="planning", transform=f"step:{index}:{step.action}", inputs=(plan.goal,)
            )
            outcome = StepOutcome(index=index, step=step, result=result, provenance=provenance)
            if self._reflect is not None:
                outcome = self._reflect(outcome)  # reflection seam (hook only)
            outcomes.append(outcome)
            state.put(f"planning:{rid}:step:{index}", {"action": step.action}, outcome.provenance)
        return ExecutionResult(plan=plan, run_id=rid, outcomes=tuple(outcomes), success=True)

    def _run_step(self, step: Step, state: Any) -> Any:
        handler = self._handlers.get(step.action)
        if handler is not None:
            return handler(step, state)
        if step.action == "reason" and self._reasoning is not None:
            goal = step.args[0] if step.args else ""
            return self._reasoning.run(goal)
        raise UnknownActionError(step.action)
