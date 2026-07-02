"""Versioned serialization for knowledge records/relations (Law 21).

Purpose: JSON-safe, versioned wire form for entity records and relations, delegating
    provenance to the canonical owner (`noetica.provenance`).
Owner: Noetica (Layer 2). Consumer: persistence/exchange; Velith; Mini Prometheus.
Constitution: §6.5; Law 21; Law 13 (no duplicated abstractions).
Future implementation owner: Noetica.
"""
from __future__ import annotations

from typing import Any, Mapping

from noetica.knowledge.records import SCHEMA_VERSION, KnowledgeRecord, Relation
from noetica.provenance.identity import deserialize_provenance, serialize_provenance


def serialize_record(r: KnowledgeRecord) -> dict[str, Any]:
    return {
        "schema_version": r.schema_version,
        "entity_id": r.entity_id,
        "kind": r.kind,
        "data": dict(r.data),
        "provenance": serialize_provenance(r.provenance),
    }


def deserialize_record(d: Mapping[str, Any]) -> KnowledgeRecord:
    return KnowledgeRecord(
        entity_id=d["entity_id"],
        kind=d["kind"],
        data=dict(d["data"]),
        provenance=deserialize_provenance(d["provenance"]),
        schema_version=d.get("schema_version", SCHEMA_VERSION),
    )


def serialize_relation(r: Relation) -> dict[str, Any]:
    return {
        "schema_version": r.schema_version,
        "subject": r.subject,
        "predicate": r.predicate,
        "obj": r.obj,
        "provenance": serialize_provenance(r.provenance),
    }


def deserialize_relation(d: Mapping[str, Any]) -> Relation:
    return Relation(
        subject=d["subject"],
        predicate=d["predicate"],
        obj=d["obj"],
        provenance=deserialize_provenance(d["provenance"]),
        schema_version=d.get("schema_version", SCHEMA_VERSION),
    )
