"""Reflector — the self-critique loop (a validated MiniFlyWire primitive, re-implemented).

Purpose: inspect an attempt and propose a revision — converts experience into correction.
Owner: Noetica (Layer 2) (§6.9).
Consumer: Velith; Mini Prometheus.
Constitution: §6.9; §4.1 (promoted from MiniFlyWire by re-implementation, Law 7).
Future implementation owner: Noetica (re-implemented from a validated MiniFlyWire spec).

Interface surface only (PE-1). No critique algorithm here.
"""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Reflector(Protocol):
    """Given an attempt and its outcome, propose a revised approach. Form only."""

    def reflect(self, attempt: Any, outcome: Any) -> Any: ...
