"""StateSubstrate — the persistent, typed, provenance-tracked shared state (the CORE).

Purpose: the substrate every other mechanism reads and writes; generators, planners,
    verifiers, and learners are typed transformations over it. Its evolution target is
    belief/probabilistic state.
Owner: Noetica (Layer 2) — the true core (§6.1).
Consumer: Velith; Mini Prometheus (the artifact-under-design / twin content live here).
Constitution: §6.1; Principle 2 (state-centric); D9; Law 3.
Future implementation owner: Noetica (default substrate; later belief-state, §8.3).

Interface surface only (PE-1). No storage engine implemented.
"""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from noetica.interfaces.provenance import Provenance


@runtime_checkable
class StateSubstrate(Protocol):
    """Typed, provenance-tracked shared state. Reads/writes carry provenance (§6.2)."""

    def get(self, key: str) -> Any | None: ...
    def put(self, key: str, value: Any, provenance: Provenance) -> None: ...
    def history(self, key: str) -> tuple[Any, ...]: ...
