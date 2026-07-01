"""PE-5 unit tests — default Observability & Logging (§6.17).

Platform tests: no domain oracle, no real verifier (Law 20). Pure observability mechanism.
"""
from __future__ import annotations

import io
import json

from noetica.interfaces.observability import Observability
from noetica.observability import (
    InMemoryObservability,
    LogEvent,
    MetricSample,
    StreamObservability,
    serialize_log_event,
)


def test_defaults_satisfy_interface_protocol() -> None:
    assert isinstance(InMemoryObservability(), Observability)
    assert isinstance(StreamObservability(io.StringIO()), Observability)


def test_inmemory_records_log_events_with_fields() -> None:
    obs = InMemoryObservability()
    obs.log("episode.appended", episode_id="abc", task="t1")
    events = obs.events()
    assert len(events) == 1
    e = events[0]
    assert e.event == "episode.appended"
    assert e.fields == {"episode_id": "abc", "task": "t1"}
    assert e.timestamp  # UTC ISO timestamp present


def test_inmemory_records_metrics_with_tags() -> None:
    obs = InMemoryObservability()
    obs.metric("verify.latency_ms", 12.5, tags={"stage": "phase2"})
    obs.metric("verify.count", 1.0)  # default tags -> {}
    m = obs.metrics()
    assert m[0].name == "verify.latency_ms" and m[0].value == 12.5
    assert m[0].tags == {"stage": "phase2"}
    assert m[1].tags == {}


def test_span_emits_start_end_and_duration_metric() -> None:
    obs = InMemoryObservability()
    with obs.span("propose", task="t1"):
        pass
    names = [e.event for e in obs.events()]
    assert names == ["propose.start", "propose.end"]
    assert any(m.name == "propose.duration_ms" for m in obs.metrics())
    end_event = obs.events()[1]
    assert "duration_ms" in end_event.fields and end_event.fields["task"] == "t1"


def test_stream_writes_structured_json_lines() -> None:
    buf = io.StringIO()
    obs = StreamObservability(buf)
    obs.log("run.started", run="r1")
    obs.metric("run.cost", 3.0)
    lines = [json.loads(x) for x in buf.getvalue().strip().splitlines()]
    assert lines[0]["kind"] == "log" and lines[0]["event"] == "run.started"
    assert lines[0]["fields"] == {"run": "r1"}
    assert lines[1]["kind"] == "metric" and lines[1]["name"] == "run.cost" and lines[1]["value"] == 3.0
    assert all("timestamp" in r and r["schema_version"] for r in lines)


def test_records_are_immutable_and_serializable() -> None:
    ev = LogEvent(event="x", fields={"a": 1}, timestamp="2026-01-01T00:00:00+00:00")
    d = serialize_log_event(ev)
    assert d["kind"] == "log" and d["event"] == "x" and d["fields"] == {"a": 1}
    import dataclasses
    import pytest
    with pytest.raises(dataclasses.FrozenInstanceError):
        ev.event = "y"  # type: ignore[misc]
    _ = MetricSample(name="m", value=1.0, tags={}, timestamp="t")  # constructs
