"""Noetica · knowledge — Knowledge Store engine (§6.5).

The typed, provenance-tracked, schema-agnostic semantic/graph store ENGINE: storage,
indexing, retrieval of entities and relations. Noetica owns the engine; domains populate
it with content. PE-13 provides `InMemoryKnowledgeStore` (backed by the State substrate),
typed records/queries, and versioned serialization. No domain knowledge/facts/physics/
prompts/reasoning/planning/memory/world-models.
"""
from __future__ import annotations

from noetica.knowledge.records import (
    SCHEMA_VERSION,
    EntityQuery,
    KnowledgeRecord,
    Relation,
    RelationQuery,
)
from noetica.knowledge.serialization import (
    deserialize_record,
    deserialize_relation,
    serialize_record,
    serialize_relation,
)
from noetica.knowledge.store import InMemoryKnowledgeStore

__all__ = [
    "InMemoryKnowledgeStore",
    "KnowledgeRecord",
    "Relation",
    "EntityQuery",
    "RelationQuery",
    "SCHEMA_VERSION",
    "serialize_record",
    "deserialize_record",
    "serialize_relation",
    "deserialize_relation",
]
