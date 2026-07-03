"""SequentialPlanner — plan representation producer (form only, §6.8).

Builds a `Plan` (sequence of `Step`s) for a goal. Domains express their plans AS Noetica
plans by injecting a step source; the default is a single `reason` step. No domain planning
logic here.
"""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from noetica.interfaces.plan import Plan, Step

StepSource = Callable[[Any], tuple[Step, ...]]


def _default_steps(goal: Any) -> tuple[Step, ...]:
    return (Step(action="reason", args=(goal,)),)


class SequentialPlanner:
    """Produces a Plan from an injected step source (default: a single `reason` step)."""

    def __init__(self, step_source: StepSource | None = None) -> None:
        self._steps = step_source if step_source is not None else _default_steps

    def plan(self, goal: Any) -> Plan:
        return Plan(goal=str(goal), steps=self._steps(goal))
