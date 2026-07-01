"""Noetica · provenance — Provenance & Lineage (Constitution §6.2).

The derivation record of every belief and artifact — first-class and non-negotiable
(Principle 7, Law 18). PE-3 provides the default mechanism: canonical provenance
identity/hashing and an in-memory lineage ledger. Domain-agnostic; no memory/episodes/
knowledge/runtime/planner/router.
"""
from __future__ import annotations

from noetica.provenance.identity import (
    PROV_SCHEMA_VERSION,
    canonical_sha256,
    content_hash,
    deserialize_provenance,
    serialize_provenance,
)
from noetica.provenance.ledger import (
    LineageNode,
    ProvenanceLedger,
    deserialize_node,
    serialize_node,
)

__all__ = [
    "ProvenanceLedger",
    "LineageNode",
    "content_hash",
    "canonical_sha256",
    "serialize_provenance",
    "deserialize_provenance",
    "serialize_node",
    "deserialize_node",
    "PROV_SCHEMA_VERSION",
]
