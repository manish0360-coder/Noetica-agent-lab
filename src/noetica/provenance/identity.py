"""Provenance identity — canonical serialization + content hash.

Purpose: the authoritative, versioned wire form for a `Provenance` value, a reusable
    canonical SHA-256 over any JSON-safe structure, and the provenance content hash
    (stable identity for a lineage node). Separates reproducible identity from mutable
    metadata (§11.7).
Owner: Noetica (Layer 2).
Consumer: State Substrate; ProvenanceLedger; Episode & Episode Store (PE-4); Velith;
    Mini Prometheus.
Constitution: §6.2; §11.7 (content-hash identity); Law 21.
Future implementation owner: Noetica.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from noetica.interfaces.provenance import Provenance

PROV_SCHEMA_VERSION = "0.1.0"


def canonical_sha256(obj: Any) -> str:
    """Deterministic SHA-256 over the canonical JSON of a JSON-safe structure.

    Canonical form: sorted keys, tight separators, UTF-8. The single shared hashing
    primitive for reproducible identity across the platform (§11.7).
    """
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def serialize_provenance(p: Provenance) -> dict[str, Any]:
    """Canonical, JSON-safe dict for a Provenance. The authoritative provenance form."""
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
        schema_version=d.get("schema_version", PROV_SCHEMA_VERSION),
    )


def content_hash(p: Provenance) -> str:
    """Deterministic content hash of a Provenance — the lineage node id (§11.7)."""
    return canonical_sha256(serialize_provenance(p))
