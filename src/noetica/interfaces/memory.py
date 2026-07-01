"""Memory — episodic/experience persistence + the write-filter policy.

Purpose: persist experience over time and decide *what is retained* (verified-only vs
    unfiltered) — the write-filter is the single manipulated variable of the compounding
    experiment.
Owner: Noetica (Layer 2) owns the framework and the `WriteFilter`/`MemoryStore` interfaces.
Consumer: Velith; Mini Prometheus.
Constitution: §6.4; §6.20 (Memory is persistence-of-experience, distinct from
    Knowledge/Context); D7 (A0–A4 arms); Law 13.
Future implementation owner: Noetica (default memory + filters); MiniFlyWire feeds
    forgetting/retention primitives by re-implementation (Law 7).

Interface surface only (PE-1). No retention/forgetting algorithm here.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from noetica.interfaces.episode import Episode


@runtime_checkable
class WriteFilter(Protocol):
    """Decides whether an episode is retained. The ONLY legal difference between the
    A1 (unfiltered) and A2 (verified) experiment arms (D7)."""

    def admit(self, episode: Episode) -> bool: ...


@runtime_checkable
class MemoryStore(Protocol):
    """Persistence of experience over time, governed by a WriteFilter."""

    def write(self, episode: Episode) -> bool: ...          # subject to the filter
    def recall(self, query: object, k: int = 5) -> tuple[Episode, ...]: ...
