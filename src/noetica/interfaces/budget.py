"""BudgetMeter — meta-control / bounded rationality.

Purpose: govern how much to think, which model to call, when to simulate, when to stop —
    computation is a costly act. The long-term policy is *learned*, not hand-tuned.
Owner: Noetica (Layer 2) (§6.14).
Consumer: Velith; Mini Prometheus.
Constitution: §6.14; Principle 5 (bounded rationality first-class).
Future implementation owner: Noetica (default meter; learned policy is gated, App. D).

Interface surface only (PE-1). No policy/algorithm here.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class BudgetMeter(Protocol):
    """Meters and caps the cost of computation."""

    def spend(self, amount: float, reason: str) -> None: ...
    def remaining(self) -> float: ...
    def exceeded(self) -> bool: ...
