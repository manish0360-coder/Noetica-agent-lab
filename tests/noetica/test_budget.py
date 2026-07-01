"""PE-6 unit tests — default Budget & Meta-control (§6.14).

Platform tests: no domain oracle, no real verifier (Law 20). Pure budget mechanism.
"""
from __future__ import annotations

import pytest

from noetica.interfaces.budget import BudgetMeter
from noetica.budget import (
    BudgetExceededError,
    InMemoryBudgetMeter,
    deserialize_snapshot,
    serialize_snapshot,
)


def test_satisfies_interface_protocol() -> None:
    assert isinstance(InMemoryBudgetMeter(10.0), BudgetMeter)


def test_spend_reduces_remaining_and_tracks_spent() -> None:
    m = InMemoryBudgetMeter(10.0)
    m.spend(3.0, "call:model")
    assert m.remaining() == 7.0
    assert m.spent == 3.0
    assert not m.exceeded()


def test_can_spend_precheck() -> None:
    m = InMemoryBudgetMeter(5.0)
    assert m.can_spend(5.0) is True
    assert m.can_spend(5.01) is False
    assert m.can_spend(-1.0) is False


def test_hard_guard_raises_and_leaves_state_unchanged() -> None:
    m = InMemoryBudgetMeter(5.0)
    m.spend(4.0, "step1")
    with pytest.raises(BudgetExceededError):
        m.spend(2.0, "step2")            # would exceed
    assert m.spent == 4.0 and m.remaining() == 1.0   # unchanged
    assert len(m.ledger()) == 1


def test_exact_to_limit_allowed_then_exceeded_true() -> None:
    m = InMemoryBudgetMeter(5.0)
    m.spend(5.0, "all")
    assert m.remaining() == 0.0
    assert m.exceeded() is True
    assert m.can_spend(0.0) is True and m.can_spend(0.01) is False


def test_negative_inputs_rejected() -> None:
    with pytest.raises(ValueError):
        InMemoryBudgetMeter(-1.0)
    with pytest.raises(ValueError):
        InMemoryBudgetMeter(10.0).spend(-2.0, "bad")


def test_ledger_records_cumulative() -> None:
    m = InMemoryBudgetMeter(10.0)
    m.spend(2.0, "a")
    m.spend(3.0, "b")
    entries = m.ledger()
    assert [(e.amount, e.reason, e.cumulative) for e in entries] == [
        (2.0, "a", 2.0),
        (3.0, "b", 5.0),
    ]


def test_snapshot_serialization_round_trip() -> None:
    m = InMemoryBudgetMeter(10.0)
    m.spend(2.0, "a")
    snap = m.snapshot()
    restored = deserialize_snapshot(serialize_snapshot(snap))
    assert restored.limit == 10.0 and restored.spent == 2.0 and restored.remaining == 8.0
    assert restored.ledger[0].reason == "a"
