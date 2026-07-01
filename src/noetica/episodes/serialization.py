"""Versioned serialization contract for episodes (Law 21).

Purpose: a stable, JSON-safe wire form for an Episode (including its Verdict and optional
    Provenance), with round-trip deserialization; every payload carries schema_version.
Owner: Noetica (Layer 2).
Consumer: Episode Store (JSONL persistence); Velith; Mini Prometheus; MiniFlyWire (datasets).
Constitution: §7.5; Law 21; §11.7.
Future implementation owner: Noetica.
"""
from __future__ import annotations

from typing import Any, Mapping

from noetica.interfaces.episode import Episode
from noetica.interfaces.verification import Verdict, VerdictStatus
from noetica.provenance.identity import deserialize_provenance, serialize_provenance


def _serialize_verdict(v: Verdict) -> dict[str, Any]:
    return {
        "status": v.status.value,
        "confidence": v.confidence,
        "detail": dict(v.detail),
        "schema_version": v.schema_version,
    }


def _deserialize_verdict(d: Mapping[str, Any]) -> Verdict:
    return Verdict(
        status=VerdictStatus(d["status"]),
        confidence=d.get("confidence", 1.0),
        detail=dict(d.get("detail", {})),
        schema_version=d.get("schema_version", "0.1.0"),
    )


def serialize_episode(e: Episode) -> dict[str, Any]:
    return {
        "schema_version": e.schema_version,
        "task_id": e.task_id,
        "verdict": _serialize_verdict(e.verdict),
        "cost": dict(e.cost),
        "environment": dict(e.environment),
        "content_hash": e.content_hash,
        "provenance": serialize_provenance(e.provenance) if e.provenance is not None else None,
    }


def deserialize_episode(d: Mapping[str, Any]) -> Episode:
    prov = d.get("provenance")
    return Episode(
        task_id=d["task_id"],
        verdict=_deserialize_verdict(d["verdict"]),
        cost=dict(d.get("cost", {})),
        environment=dict(d.get("environment", {})),
        content_hash=d.get("content_hash", ""),
        provenance=deserialize_provenance(prov) if prov is not None else None,
        schema_version=d.get("schema_version", "0.1.0"),
    )
