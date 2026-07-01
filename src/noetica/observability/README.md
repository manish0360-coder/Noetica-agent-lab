# src/noetica/observability — Observability & Logging

**Constitution:** §6.17 (observability), Principle 7 (non-negotiable with provenance),
Law 18 (records must not diverge from reality), Law 21 (versioned records).

## Purpose
Structured logging, metrics, and traces — the ability to see *what the system did and why*.
The operational-visibility substrate every later mechanism emits through, and the basis on
which a human overseer and the evaluation harness trust runs.

## Responsibilities
- Emit **structured log events** (`log(event, **fields)`) and **metric samples**
  (`metric(name, value, tags)`) as immutable, JSON-serializable records with UTC timestamps.
- Provide lightweight **traces** via `span(name, ...)` (start/end events + duration metric).
- Ship default implementations: `InMemoryObservability` (introspection + tests) and
  `StreamObservability` (structured JSON lines to a stream; default stderr).

## Non-responsibilities (NOT here)
- **Memory**, **Knowledge**, **Context**, **Reasoning**, **Planning**, **Runtime**.
- **Provenance / lineage** (that is §6.2, a distinct subsystem — `noetica.provenance`).
- Metrics backends/exporters, dashboards, tracing UIs (added by extraction, Law 8).
- Any domain content.

## Dependencies
- `noetica.interfaces.observability.Observability` (the contract satisfied).
- Python standard library only. **No other platform mechanism** (Tier-1: zero platform
  deps), no other layer, no `reference/`.

## Consumers
- Every later PE mechanism emits through this (retro-wired into State/Provenance/Episode).
- Velith and Mini Prometheus emit operational signals.

## Constitution references
§6.17 · Principle 7 · Law 18 · Law 21 · (distinct from §6.2 provenance).

## Future implementation milestones
- **Now (PE-5):** typed records; in-memory + JSON-line stream defaults; `span()` traces.
- **Later (by extraction, Law 8):** exporters/backends (OpenTelemetry-style), sampling,
  redaction — each added only when a real consumer needs it.
