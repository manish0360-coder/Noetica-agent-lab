"""Typed, immutable observability records.

Purpose: the value types the observability mechanism emits — a structured log event and a
    metric sample. Immutable and JSON-serializable so runs are auditable (Principle 7).
Owner: Noetica (Layer 2).
Consumer: every later mechanism (emits); Velith; Mini Prometheus.
Constitution: §6.17; Principle 7; Law 18; Law 21 (schema_version).
Future implementation owner: Noetica.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

SCHEMA_VERSION = "0.1.0"


@dataclass(frozen=True)
class LogEvent:
    """One structured log event: a name, arbitrary typed fields, and a UTC timestamp."""

    event: str
    fields: Mapping[str, Any]
    timestamp: str
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class MetricSample:
    """One metric sample: a name, a float value, string tags, and a UTC timestamp."""

    name: str
    value: float
    tags: Mapping[str, str]
    timestamp: str
    schema_version: str = SCHEMA_VERSION


def serialize_log_event(e: LogEvent) -> dict[str, Any]:
    return {
        "schema_version": e.schema_version,
        "kind": "log",
        "event": e.event,
        "fields": dict(e.fields),
        "timestamp": e.timestamp,
    }


def serialize_metric(m: MetricSample) -> dict[str, Any]:
    return {
        "schema_version": m.schema_version,
        "kind": "metric",
        "name": m.name,
        "value": m.value,
        "tags": dict(m.tags),
        "timestamp": m.timestamp,
    }
