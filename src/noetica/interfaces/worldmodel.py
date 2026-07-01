"""WorldModel — the twin/state-sync ENGINE interface (content is domain-owned).

Purpose: the mechanism of state-sync / versioning / provenance for a world model. The
    engine is Noetica's; the manufacturing/engineering twin CONTENT is domain-owned.
Owner: Noetica (Layer 2) owns the engine + interface (§6.1 evolution; §8.4).
Consumer: Mini Prometheus (factory/product twin content); Velith (engineering models).
Constitution: §8.4 (engine vs content); §9.2 (digital-twin engine = Noetica).
Future implementation owner: Noetica (engine); domains own twin CONTENT.

Interface surface only (PE-1). No twin/physics here.
"""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from noetica.interfaces.provenance import Provenance


@runtime_checkable
class WorldModel(Protocol):
    """State-sync/versioning/provenance engine for a world model. Content is domain-owned."""

    def sync(self, snapshot: Any, provenance: Provenance) -> str: ...   # returns version
    def at(self, version: str) -> Any | None: ...
