"""PE-19 unit tests — Planning Runtime (§6.8). Form only; injected capabilities."""
from __future__ import annotations

from typing import Any

import pytest

from noetica.interfaces.plan import Executor, Plan, Planner, Step
from noetica.interfaces.provenance import Provenance
from noetica.planning import (
    SequentialExecutor,
    SequentialPlanner,
    StepOutcome,
    UnknownActionError,
)
from noetica.state import InMemoryStateSubstrate


class _FakeReasoning:
    def step(self, state: Any) -> Any:
        return None

    def run(self, goal: Any, max_steps: int = 1) -> Any:
        return {"reasoned": goal}


def test_planner_and_executor_satisfy_protocols() -> None:
    assert isinstance(SequentialPlanner(), Planner)
    assert isinstance(SequentialExecutor(), Executor)


def test_default_plan_is_single_reason_step() -> None:
    plan = SequentialPlanner().plan("g")
    assert isinstance(plan, Plan) and len(plan.steps) == 1
    assert plan.steps[0].action == "reason" and plan.steps[0].args == ("g",)


def test_custom_step_source() -> None:
    src = lambda goal: (Step(action="a"), Step(action="b"))
    plan = SequentialPlanner(step_source=src).plan("g")
    assert [s.action for s in plan.steps] == ["a", "b"]


def test_execute_sequences_handlers_and_writes_state() -> None:
    seen: list[str] = []

    def handler(step: Step, state: Any) -> str:
        seen.append(step.action)
        return f"ran:{step.action}"

    plan = Plan(goal="g", steps=(Step(action="a"), Step(action="b")))
    state = InMemoryStateSubstrate()
    ex = SequentialExecutor(handlers={"a": handler, "b": handler})
    result = ex.execute(plan, state, run_id="R1")
    assert seen == ["a", "b"] and result.success
    assert [o.result for o in result.outcomes] == ["ran:a", "ran:b"]
    assert state.get_record("planning:R1:step:0") is not None
    assert state.get_record("planning:R1:step:1") is not None


def test_reason_action_delegates_to_injected_reasoning() -> None:
    plan = SequentialPlanner().plan("solve-x")   # single reason step
    ex = SequentialExecutor(reasoning=_FakeReasoning())
    result = ex.execute(plan, InMemoryStateSubstrate())
    assert result.outcomes[0].result == {"reasoned": "solve-x"}


def test_unknown_action_raises() -> None:
    plan = Plan(goal="g", steps=(Step(action="mystery"),))
    with pytest.raises(UnknownActionError):
        SequentialExecutor().execute(plan, InMemoryStateSubstrate())


def test_reflection_seam_is_invoked() -> None:
    calls: list[int] = []

    def reflect(outcome: StepOutcome) -> StepOutcome:
        calls.append(outcome.index)
        return outcome

    plan = SequentialPlanner().plan("g")
    SequentialExecutor(reasoning=_FakeReasoning(), reflect=reflect).execute(plan, InMemoryStateSubstrate())
    assert calls == [0]


def test_run_ids_namespace_state_keys() -> None:
    plan = SequentialPlanner().plan("g")
    ex = SequentialExecutor(reasoning=_FakeReasoning())
    state = InMemoryStateSubstrate()
    a = ex.execute(plan, state)
    b = ex.execute(plan, state)
    assert a.run_id != b.run_id
    assert state.get_record(f"planning:{a.run_id}:step:0") is not None
    assert state.get_record(f"planning:{b.run_id}:step:0") is not None


def test_step_outcome_provenance() -> None:
    plan = SequentialPlanner().plan("g")
    result = SequentialExecutor(reasoning=_FakeReasoning()).execute(plan, InMemoryStateSubstrate())
    assert result.outcomes[0].provenance.source == "planning"
