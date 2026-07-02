"""Typed, immutable knowledge records and query patterns (schema-agnostic).

Purpose: the value types the knowledge engine stores — a typed, provenance-tracked entity
    record and a typed graph relation — plus the query patterns used for retrieval. The
    `kind` and property `data` are domain-supplied labels/values; NO domain knowledge is
    hard-coded here.
Owner: Noetica (Layer 2).
Consumer: Context (PE-16); Velith (engineering ontology); Mini Prometheus (mfg concepts).
Constitution: §6.5 (knowledge store engine); §6.20 (distinct from Memory/Context);
    Law 3 (engine vs content); Law 21 (schema_version).
Future implementation owner: Noetica (engine); domains (content).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from noetica.interfaces.provenance import Provenance

SCHEMA_VERSION = "0.1.0"


@dataclass(frozen=True)
class KnowledgeRecord:
    """A typed, provenance-tracked entity: an id, a domain-supplied `kind`, its property
    `data`, and provenance. Schema-agnostic — the platform stores it without interpreting
    the domain meaning of `kind`/`data`."""

    entity_id: str
    kind: str
    data: Mapping[str, Any]
    provenance: Provenance
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class Relation:
    """A typed, provenance-tracked graph edge: subject --predicate--> object."""

    subject: str
    predicate: str
    obj: str
    provenance: Provenance
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class EntityQuery:
    """Retrieval pattern over entities: by `kind` (None = any) and optional property
    equality filter `where` (schema-agnostic dict equality)."""

    kind: str | None = None
    where: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class RelationQuery:
    """Graph pattern over relations; each field None acts as a wildcard."""

    subject: str | None = None
    predicate: str | None = None
    obj: str | None = None
