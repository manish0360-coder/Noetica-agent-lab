"""Typed, immutable state records for the State Substrate.

Purpose: the value types the substrate stores — an immutable, typed, provenance-tracked
    record of one write, and an immutable point-in-time snapshot of the whole substrate.
Owner: Noetica (Layer 2).
Consumer: Velith; Mini Prometheus (read/write via the StateSubstrate interface).
Constitution: §6.1 (State Substrate is the true core); §6.2 (provenance first-class);
    Law 3 (mechanism, not content); Law 21 (versioned schema).
Future implementation owner: Noetica.

Domain-agnostic: these records carry arbitrary typed values but hold NO domain logic.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from noetica.interfaces.provenance import Provenance

# Data-contract schema version for state records (Law 21). Bump on any schema change.
SCHEMA_VERSION = "0.1.0"


@dataclass(frozen=True)
class StateRecord:
    """One immutable write to a key: its value, provenance, and versioning.

    Immutable (frozen): a write is never mutated in place; a new record is appended.
    `version` is the 1-based per-key write count; `revision` is the global monotonic
    substrate revision at write time.
    """

    key: str
    value: Any
    provenance: Provenance
    version: int
    revision: int
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class StateSnapshot:
    """Immutable point-in-time view of the whole substrate at a global revision.

    `records` maps key -> the latest StateRecord as of `revision`. The mapping is a
    read-only view (see InMemoryStateSubstrate.snapshot).
    """

    revision: int
    records: Mapping[str, StateRecord]
    schema_version: str = SCHEMA_VERSION
