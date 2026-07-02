"""PE-11 unit tests — Compute Interface (§6.21).

Platform tests: scheduling/tracking/cancelling + budget guard; execution delegated to a
test-double adapter (real infra adapters live outside the platform). No vendor code here.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from noetica.budget import InMemoryBudgetMeter
from noetica.compute import (
    ComputeBroker,
    ComputeBudgetError,
    ComputeSpec,
    ExecutionAdapter,
    InvalidStateError,
    UnknownHandleError,
    WorkStatus,
)
from noetica.interfaces.compute import ComputeInterface


@dataclass
class _FakeAdapter:
    """Test double for external execution infrastructure."""

    name: str = "local-fake"
    placed: list[tuple[str, ComputeSpec]] = field(default_factory=list)
    cancelled: list[str] = field(default_factory=list)

    def place(self, handle: str, spec: ComputeSpec) -> None:
        self.placed.append((handle, spec))

    def cancel(self, handle: str) -> None:
        self.cancelled.append(handle)


def _broker(limit: float = 100.0) -> tuple[ComputeBroker, _FakeAdapter, InMemoryBudgetMeter]:
    adapter = _FakeAdapter()
    meter = InMemoryBudgetMeter(limit)
    return ComputeBroker(adapter, meter), adapter, meter


def test_broker_and_adapter_satisfy_protocols() -> None:
    broker, adapter, _ = _broker()
    assert isinstance(broker, ComputeInterface)
    assert isinstance(adapter, ExecutionAdapter)


def test_request_schedules_without_charging_or_executing() -> None:
    broker, adapter, meter = _broker()
    h = broker.request(ComputeSpec(kind="fea", estimated_cost=5.0))
    assert broker.status(h) is WorkStatus.SCHEDULED
    assert meter.spent == 0.0                 # not charged yet
    assert adapter.placed == []               # not executed yet
    assert broker.cost(h) == 5.0


def test_place_charges_budget_and_delegates_execution() -> None:
    broker, adapter, meter = _broker()
    h = broker.request(ComputeSpec(kind="fea", estimated_cost=5.0))
    broker.place(h)
    assert broker.status(h) is WorkStatus.PLACED
    assert meter.spent == 5.0                 # hard cost guard charged
    assert adapter.placed and adapter.placed[0][0] == h


def test_request_rejects_over_budget_nothing_charged() -> None:
    broker, adapter, meter = _broker(limit=3.0)
    with pytest.raises(ComputeBudgetError):
        broker.request(ComputeSpec(kind="big", estimated_cost=10.0))
    assert meter.spent == 0.0 and adapter.placed == []


def test_request_rejects_bad_spec_and_negative_cost() -> None:
    broker, _, _ = _broker()
    with pytest.raises(TypeError):
        broker.request({"not": "a spec"})
    with pytest.raises(ValueError):
        broker.request(ComputeSpec(kind="x", estimated_cost=-1.0))


def test_place_twice_is_invalid_state() -> None:
    broker, _, _ = _broker()
    h = broker.request(ComputeSpec(kind="x", estimated_cost=1.0))
    broker.place(h)
    with pytest.raises(InvalidStateError):
        broker.place(h)


def test_cancel_placed_calls_adapter() -> None:
    broker, adapter, _ = _broker()
    h = broker.request(ComputeSpec(kind="x", estimated_cost=1.0))
    broker.place(h)
    broker.cancel(h)
    assert broker.status(h) is WorkStatus.CANCELLED
    assert adapter.cancelled == [h]


def test_cancel_scheduled_does_not_call_adapter() -> None:
    broker, adapter, _ = _broker()
    h = broker.request(ComputeSpec(kind="x", estimated_cost=1.0))
    broker.cancel(h)
    assert broker.status(h) is WorkStatus.CANCELLED
    assert adapter.cancelled == []            # never placed -> adapter not called


def test_unknown_handle_errors() -> None:
    broker, _, _ = _broker()
    with pytest.raises(UnknownHandleError):
        broker.cost("nope")
