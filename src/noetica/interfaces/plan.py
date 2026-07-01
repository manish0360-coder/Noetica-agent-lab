"""Plan / Planner / Executor — planning representation + executor (form).

Purpose: express, sequence, and execute plans, with a reflection seam. Planning *form*
    is reusable; planning *content* (engineering/mfg plans) is domain-owned.
Owner: Noetica (Layer 2) (§6.8).
Consumer: Velith; Mini Prometheus (express their plans AS Noetica plans).
Constitution: §6.8; Law 3 (form vs content).
Future implementation owner: Noetica (default representation + executor).

Interface surface only (PE-1). No planning/search algorithm here.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class Step:
    """One plan step. Schema only."""

    action: str
    args: tuple[Any, ...] = ()


@dataclass(frozen=True)
class Plan:
    """An ordered plan representation. Schema only — content is domain-owned."""

    goal: str
    steps: tuple[Step, ...] = ()
    schema_version: str = "0.1.0"


@runtime_checkable
class Planner(Protocol):
    """Produces a Plan for a goal (form only)."""

    def plan(self, goal: Any) -> Plan: ...


@runtime_checkable
class Executor(Protocol):
    """Executes a Plan over shared state, with a reflection seam."""

    def execute(self, plan: Plan, state: Any) -> Any: ...
