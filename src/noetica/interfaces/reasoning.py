"""ReasoningLoop — the FORM of reasoning (a runtime), never a mind.

Purpose: iterate inference, apply verification seams, backtrack. Owns *how* to run a
    reasoning loop; *what* is reasoned about is domain content (never here).
Owner: Noetica (Layer 2) (§6.7).
Consumer: Velith; Mini Prometheus.
Constitution: §6.7; Principle "no homunculus"; Law 3/5.
Future implementation owner: Noetica (default loop). Domain reasoning CONTENT stays in
    Velith / Mini Prometheus.

Interface surface only (PE-1). No reasoning algorithm here.
"""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ReasoningLoop(Protocol):
    """Drives condition-driven iteration over shared state. Form only."""

    def step(self, state: Any) -> Any: ...                  # one inference iteration
    def run(self, goal: Any, max_steps: int = 1) -> Any: ...
