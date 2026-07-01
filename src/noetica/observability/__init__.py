"""Noetica · observability — Observability & Logging (§6.17).

Structured logging, metrics, and traces — the operational-visibility substrate the
platform emits through (non-negotiable with provenance, Principle 7). PE-5 provides typed
records and default implementations (in-memory + JSON-line stream) with a `span()` trace
helper. Domain-agnostic; depends only on the frozen interfaces.
"""
from __future__ import annotations

from noetica.observability.defaults import (
    InMemoryObservability,
    ObservabilityBase,
    StreamObservability,
)
from noetica.observability.records import (
    SCHEMA_VERSION,
    LogEvent,
    MetricSample,
    serialize_log_event,
    serialize_metric,
)

__all__ = [
    "InMemoryObservability",
    "StreamObservability",
    "ObservabilityBase",
    "LogEvent",
    "MetricSample",
    "serialize_log_event",
    "serialize_metric",
    "SCHEMA_VERSION",
]
