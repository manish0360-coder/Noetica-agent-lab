"""KnowledgeStore — the typed, provenance-tracked semantic/graph store ENGINE.

Purpose: accumulate *structured* knowledge (entities, relations, constraints,
    transitions) — schema-agnostic storage/retrieval. Noetica owns the engine; domains
    populate it with content.
Owner: Noetica (Layer 2) owns the engine + interface (§6.5).
Consumer: Velith (populates engineering ontology); Mini Prometheus (mfg concepts).
Constitution: §6.5; §6.20 (distinct from Memory/Context); Law 3 (engine vs content).
Future implementation owner: Noetica (default engine); domains supply content only.

Interface surface only (PE-1). No graph/retrieval implementation.
"""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from noetica.interfaces.provenance import Provenance


@runtime_checkable
class KnowledgeStore(Protocol):
    """Schema-agnostic typed knowledge engine. Content is domain-owned."""

    def upsert(self, entity_id: str, data: Any, provenance: Provenance) -> None: ...
    def get(self, entity_id: str) -> Any | None: ...
    def query(self, pattern: Any) -> tuple[Any, ...]: ...
