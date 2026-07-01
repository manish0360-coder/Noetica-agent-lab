"""Provenance identity — canonical serialization + content hash.

Purpose: the authoritative, versioned wire form for a `Provenance` value and its
    deterministic content hash (stable identity for a lineage node). Separates
    reproducible identity from mutable metadata (§11.7).
Owner: Noetica (Layer 2).
Consumer: the State Substrate (records provenance) and the ProvenanceLedger; Velith;
    Mini Prometheus.
Constitution: §6.2 (provenance first-class); §11.7 (content-hash identity); Law 21.
Future implementation owner: Noetica.

No Memory/Episode/Knowledge/Runtime/Planner/Router logic. Operates only on the
`Provenance` value type from the frozen interface surface.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from noetica.interfaces.provenance import Provenance

PROV_SCHEMA_VERSION = "0.1.0"


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
    """Deterministic sha256 over the canonical provenance form — the lineage node id.

    Stable across runs given identical provenance (§11.7 reproducible identity).
    """
    payload = json.dumps(
        serialize_provenance(p), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
