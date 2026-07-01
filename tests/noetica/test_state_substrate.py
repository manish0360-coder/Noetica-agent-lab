"""PE-2 unit tests — default StateSubstrate (Constitution §6.1).

Platform tests: no domain oracle, no real verifier (Law 20). Pure state mechanism.
"""
from __future__ import annotations

import dataclasses

import pytest

from noetica.interfaces.provenance import Provenance
from noetica.interfaces.state import StateSubstrate
from noetica.state import (
    InMemoryStateSubstrate,
    StateRecord,
    StateSnapshot,
    deserialize_record,
    deserialize_snapshot,
    serialize_record,
    serialize_snapshot,
)


def _prov(t: str = "unit-test") -> Provenance:
    return Provenance(source="test", transform=t)


def test_satisfies_interface_protocol() -> None:
    sub = InMemoryStateSubstrate()
    assert isinstance(sub, StateSubstrate)  # runtime_checkable structural conformance


def test_put_then_get_returns_latest() -> None:
    sub = InMemoryStateSubstrate()
    sub.put("k", 1, _prov())
    sub.put("k", 2, _prov())
    assert sub.get("k") == 2


def test_get_missing_key_returns_none() -> None:
    assert InMemoryStateSubstrate().get("absent") is None


def test_history_is_ordered_immutable_tuple() -> None:
    sub = InMemoryStateSubstrate()
    for v in ("a", "b", "c"):
        sub.put("k", v, _prov())
    hist = sub.history("k")
    assert hist == ("a", "b", "c")
    assert isinstance(hist, tuple)


def test_per_key_version_and_global_revision() -> None:
    sub = InMemoryStateSubstrate()
    sub.put("x", 1, _prov())
    sub.put("y", 1, _prov())
    sub.put("x", 2, _prov())
    assert sub.get_record("x").version == 2   # per-key
    assert sub.get_record("y").version == 1
    assert sub.revision == 3                   # global monotonic


def test_provenance_is_retained() -> None:
    sub = InMemoryStateSubstrate()
    sub.put("k", 42, _prov("derive"))
    rec = sub.get_record("k")
    assert rec is not None and rec.provenance.transform == "derive"


def test_records_are_immutable() -> None:
    sub = InMemoryStateSubstrate()
    sub.put("k", 1, _prov())
    rec = sub.get_record("k")
    assert rec is not None
    with pytest.raises(dataclasses.FrozenInstanceError):
        rec.value = 99  # type: ignore[misc]


def test_snapshot_is_immutable_and_latest_per_key() -> None:
    sub = InMemoryStateSubstrate()
    sub.put("x", 1, _prov())
    sub.put("x", 2, _prov())
    sub.put("y", 7, _prov())
    snap = sub.snapshot()
    assert isinstance(snap, StateSnapshot)
    assert snap.revision == 3
    assert snap.records["x"].value == 2 and snap.records["y"].value == 7
    with pytest.raises(TypeError):
        snap.records["z"] = None  # type: ignore[index]  # read-only mapping


def test_record_serialization_round_trip() -> None:
    sub = InMemoryStateSubstrate()
    sub.put("k", {"nested": [1, 2, 3]}, _prov("t"))
    rec = sub.get_record("k")
    assert rec is not None
    restored = deserialize_record(serialize_record(rec))
    assert restored == rec


def test_snapshot_serialization_round_trip() -> None:
    sub = InMemoryStateSubstrate()
    sub.put("a", 1, _prov())
    sub.put("b", "two", _prov())
    snap = sub.snapshot()
    restored = deserialize_snapshot(serialize_snapshot(snap))
    assert restored.revision == snap.revision
    assert restored.records["a"] == snap.records["a"]


def test_schema_version_present() -> None:
    sub = InMemoryStateSubstrate()
    sub.put("k", 1, _prov())
    rec = sub.get_record("k")
    assert rec is not None and rec.schema_version
