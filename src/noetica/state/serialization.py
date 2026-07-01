"""Serialization contract for state records/snapshots (Law 21 — versioned data contract).

Purpose: a stable, versioned, JSON-safe wire form for provenance, state records, and
    snapshots, with round-trip deserialization. Every payload carries `schema_version`;
    a schema change requires a version bump + migration (§11.7, §11.10).
Owner: Noetica (Layer 2).
Consumer: Velith; Mini Prometheus (persist/exchange state via this contract).
Constitution: §6.2; Law 21; §11.7 (content/identity discipline).
Future implementation owner: Noetica.

Values must be JSON-serializable for `to_json`; the record structure itself is always
serializable. No domain logic.
"""
from __future__ import annotations

from types import MappingProxyType
from typing import Any, Mapping

from noetica.interfaces.provenance import Provenance
from noetica.state.records import SCHEMA_VERSION, StateRecord, StateSnapshot


def serialize_provenance(p: Provenance) -> dict[str, Any]:
    return {
        "source": p.source,
        "transform": p.transform,
        "inputs": list(p.inputs),
        "attributes": dict(p.attributes),
        "schema_version": p.schema_version,
    }


def deserialize_provenance(d: Mapping[str, Any]) -> Provenance:
    return Provenance(
        source=d["source"],
        transform=d["transform"],
        inputs=tuple(d.get("inputs", ())),
        attributes=dict(d.get("attributes", {})),
        schema_version=d.get("schema_version", SCHEMA_VERSION),
    )


def serialize_record(r: StateRecord) -> dict[str, Any]:
    return {
        "schema_version": r.schema_version,
        "key": r.key,
        "value": r.value,
        "provenance": serialize_provenance(r.provenance),
        "version": r.version,
        "revision": r.revision,
    }


def deserialize_record(d: Mapping[str, Any]) -> StateRecord:
    return StateRecord(
        key=d["key"],
        value=d["value"],
        provenance=deserialize_provenance(d["provenance"]),
        version=d["version"],
        revision=d["revision"],
        schema_version=d.get("schema_version", SCHEMA_VERSION),
    )


def serialize_snapshot(s: StateSnapshot) -> dict[str, Any]:
    return {
        "schema_version": s.schema_version,
        "revision": s.revision,
        "records": {k: serialize_record(v) for k, v in s.records.items()},
    }


def deserialize_snapshot(d: Mapping[str, Any]) -> StateSnapshot:
    records = {k: deserialize_record(v) for k, v in d["records"].items()}
    return StateSnapshot(
        revision=d["revision"],
        records=MappingProxyType(records),
        schema_version=d.get("schema_version", SCHEMA_VERSION),
    )
