"""Noetica · state — State Substrate (Constitution §6.1). THE true core.

The persistent, typed, provenance-tracked shared state. PE-2 provides the default
implementation (`InMemoryStateSubstrate`) plus its typed records and versioned
serialization contract. Domain-agnostic; no memory/planner/reasoning/runtime/routing.
"""
from __future__ import annotations

from noetica.state.records import SCHEMA_VERSION, StateRecord, StateSnapshot
from noetica.state.serialization import (
    deserialize_provenance,
    deserialize_record,
    deserialize_snapshot,
    serialize_provenance,
    serialize_record,
    serialize_snapshot,
)
from noetica.state.substrate import InMemoryStateSubstrate

__all__ = [
    "InMemoryStateSubstrate",
    "StateRecord",
    "StateSnapshot",
    "SCHEMA_VERSION",
    "serialize_provenance",
    "deserialize_provenance",
    "serialize_record",
    "deserialize_record",
    "serialize_snapshot",
    "deserialize_snapshot",
]
