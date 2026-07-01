"""Observability — structured logging, metrics, traces.

Purpose: see what the system did and why — non-negotiable with provenance; lets the
    human overseer and the eval harness trust runs.
Owner: Noetica (Layer 2) (§6.17).
Consumer: Velith; Mini Prometheus (emit).
Constitution: §6.17; Principle 7.
Future implementation owner: Noetica (default; seeded by re-implementing the MiniNoetica
    JSONL logger pattern — never imported).

Interface surface only (PE-1). No logging backend here.
"""
from __future__ import annotations

from typing import Any, Mapping, Protocol, runtime_checkable


@runtime_checkable
class Observability(Protocol):
    """Structured events, metrics, and traces across the platform."""

    def log(self, event: str, **fields: Any) -> None: ...
    def metric(self, name: str, value: float, tags: Mapping[str, str] | None = None) -> None: ...
