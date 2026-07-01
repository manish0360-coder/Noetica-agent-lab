"""Guardrail — the safety policy ENGINE (enforces the immutable oversight boundary).

Purpose: enforce policy, including the human-oversight boundary the system may never
    modify. Noetica owns the engine; domains supply domain policy (content).
Owner: Noetica (Layer 2) owns the engine + interface (§6.16).
Consumer: Velith; Mini Prometheus (supply domain policy).
Constitution: §6.16; Principle 6 / Law 17 (grounding & oversight immutable).
Future implementation owner: Noetica (engine); domains provide policy content.

Interface surface only (PE-1). No policy logic here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class Decision:
    """Allow/deny outcome of a guardrail check. Schema only."""

    allowed: bool
    reason: str = ""


@runtime_checkable
class Guardrail(Protocol):
    """Evaluates an action against policy; the oversight boundary is immutable (Law 17)."""

    def check(self, action: Any) -> Decision: ...
