"""Default Observability implementations (§6.17).

Purpose: the reusable structured logging/metrics/traces mechanism the platform emits
    through. `InMemoryObservability` collects records (introspection + tests);
    `StreamObservability` writes structured JSON lines to a stream (default stderr) that
    survives as a log stream. Both provide `span()` for lightweight traces.
Owner: Noetica (Layer 2).
Consumer: every later mechanism; Velith; Mini Prometheus.
Constitution: §6.17; Principle 7; Law 18.
Future implementation owner: Noetica (exporters/backends by extraction, Law 8).

Scope: observability ONLY. No Memory/Knowledge/Context/Reasoning/Planning/Runtime; no
domain content. Depends only on the frozen interfaces (no other platform mechanism).
"""
from __future__ import annotations

import abc
import json
import sys
import time
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Mapping, TextIO

from noetica.observability.records import (
    LogEvent,
    MetricSample,
    serialize_log_event,
    serialize_metric,
)


def _now() -> str:
    """UTC ISO-8601 timestamp — always UTC for correct time arithmetic."""
    return datetime.now(timezone.utc).isoformat()


class ObservabilityBase(abc.ABC):
    """Shared behavior: `span()` traces expressed in terms of `log`/`metric`.

    Concrete subclasses implement `log` and `metric`; structurally they satisfy the
    `noetica.interfaces.observability.Observability` protocol.
    """

    @abc.abstractmethod
    def log(self, event: str, **fields: Any) -> None: ...

    @abc.abstractmethod
    def metric(self, name: str, value: float, tags: Mapping[str, str] | None = None) -> None: ...

    @contextmanager
    def span(self, name: str, **fields: Any) -> Iterator[None]:
        """Trace a block: emit `<name>.start`/`<name>.end` events + a duration metric."""
        self.log(f"{name}.start", **fields)
        start = time.perf_counter()
        try:
            yield
        finally:
            duration_ms = round((time.perf_counter() - start) * 1000, 3)
            self.log(f"{name}.end", duration_ms=duration_ms, **fields)
            self.metric(f"{name}.duration_ms", duration_ms)


class InMemoryObservability(ObservabilityBase):
    """Collects log events and metric samples in memory. Non-persistent."""

    def __init__(self) -> None:
        self._events: list[LogEvent] = []
        self._metrics: list[MetricSample] = []

    def log(self, event: str, **fields: Any) -> None:
        self._events.append(LogEvent(event=event, fields=dict(fields), timestamp=_now()))

    def metric(self, name: str, value: float, tags: Mapping[str, str] | None = None) -> None:
        self._metrics.append(
            MetricSample(name=name, value=value, tags=dict(tags or {}), timestamp=_now())
        )

    def events(self) -> tuple[LogEvent, ...]:
        return tuple(self._events)

    def metrics(self) -> tuple[MetricSample, ...]:
        return tuple(self._metrics)


class StreamObservability(ObservabilityBase):
    """Writes one structured JSON line per record to a text stream (default stderr)."""

    def __init__(self, stream: TextIO | None = None) -> None:
        self._stream: TextIO = stream if stream is not None else sys.stderr

    def log(self, event: str, **fields: Any) -> None:
        record = serialize_log_event(
            LogEvent(event=event, fields=dict(fields), timestamp=_now())
        )
        self._stream.write(json.dumps(record, ensure_ascii=False) + "\n")

    def metric(self, name: str, value: float, tags: Mapping[str, str] | None = None) -> None:
        record = serialize_metric(
            MetricSample(name=name, value=value, tags=dict(tags or {}), timestamp=_now())
        )
        self._stream.write(json.dumps(record, ensure_ascii=False) + "\n")
