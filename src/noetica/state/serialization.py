"""Serialization contract for state records/snapshots (Law 21 — versioned data contract).

Purpose: a stable, versioned, JSON-safe wire form for state records and snapshots, with
    round-trip deserialization. Provenance (de)serialization is delegated to the
    canonical owner, `noetica.provenance` (§6.2), to avoid duplicated logic.
Owner: Noetica (Layer 2).
Consumer: Velith; Mini Prometheus (persist/exchange state via this contract).
Constitution: §6.2; Law 21; §11.7; Law 13 (no duplicated abstractions).
Future implementation owner: Noetica.
"""
from __future__ import annotations

from typing import Any, Mapping

# Provenance serialization is owned by the provenance subsystem (state depends on it;
# correct dependency direction interfaces <- provenance <- state).
from noetica.provenance.identity import deserialize_provenance, serialize_provenance
from noetica.state.records import SCHEMA_VERSION, StateRecord, StateSnapshot

__all__ = [
    "serialize_provenance",
    "deserialize_provenance",
    "serialize_record",
    "deserialize_record",
    "serialize_snapshot",
    "deserialize_snapshot",
]


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
    from types import MappingProxyType

    records = {k: deserialize_record(v) for k, v in d["records"].items()}
    return StateSnapshot(
        revision=d["revision"],
        records=MappingProxyType(records),
        schema_version=d.get("schema_version", SCHEMA_VERSION),
    )
