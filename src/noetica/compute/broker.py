"""ComputeBroker — the default Compute Interface mechanism (§6.21).

Purpose: a vendor-neutral broker to SCHEDULE, EXECUTE (via an external adapter), TRACK, and
    CANCEL compute work, enforcing budget limits through the BudgetMeter interface. It does
    NOT run infrastructure itself — execution is delegated to an ExecutionAdapter; the
    platform owns the interface + budgeting, domains own the adapters (§6.21).
Owner: Noetica (Layer 2).
Consumer: Runtime (PE-21); Velith / Mini Prometheus implement concrete adapters.
Constitution: §6.21 (Amendment 3); §6.14 (budget cost guard); Principle 9.
Future implementation owner: Noetica (broker); domains/external (adapters + execution).

Scope: scheduling/tracking/cancelling + budget guard + delegation ONLY. No Kubernetes,
Docker, cloud providers, GPUs, engineering solvers, Velith adapters, infrastructure
orchestration, runtime behavior, reasoning, or planning. Consumes the BudgetMeter INTERFACE
(a concrete meter is injected).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from noetica.compute.adapter import ExecutionAdapter
from noetica.compute.spec import ComputeSpec, WorkStatus
from noetica.interfaces.budget import BudgetMeter


class ComputeError(RuntimeError):
    """Base error for compute-broker failures."""


class UnknownHandleError(ComputeError):
    """No work item exists for the handle."""


class ComputeBudgetError(ComputeError):
    """The work's estimated cost cannot be afforded within the remaining budget."""


class InvalidStateError(ComputeError):
    """The operation is not valid for the work item's current lifecycle state."""


@dataclass
class _WorkItem:
    spec: ComputeSpec
    status: WorkStatus
    cost: float


class ComputeBroker:
    """Vendor-neutral compute broker. Satisfies the `ComputeInterface`
    (request/place/cost) and adds tracking (`status`) and `cancel`."""

    def __init__(self, adapter: ExecutionAdapter, budget: BudgetMeter) -> None:
        self._adapter = adapter
        self._budget = budget
        self._work: dict[str, _WorkItem] = {}
        self._counter = 0

    # ── ComputeInterface ─────────────────────────────────────────────────────────
    def request(self, spec: Any) -> str:
        """Schedule work: budget pre-check (cost guard), assign a handle, status=SCHEDULED.
        Nothing is charged or executed yet."""
        if not isinstance(spec, ComputeSpec):
            raise TypeError("compute spec must be a ComputeSpec")
        if spec.estimated_cost < 0:
            raise ValueError("estimated_cost must be non-negative")
        if spec.estimated_cost > self._budget.remaining():
            raise ComputeBudgetError(
                f"estimated cost {spec.estimated_cost} exceeds remaining {self._budget.remaining()}"
            )
        handle = f"work-{self._counter}"
        self._counter += 1
        self._work[handle] = _WorkItem(spec=spec, status=WorkStatus.SCHEDULED, cost=spec.estimated_cost)
        return handle

    def place(self, handle: str) -> None:
        """Place work for execution: charge the budget (HARD guard) and delegate to the
        external execution adapter. Idempotent only from SCHEDULED."""
        item = self._require(handle)
        if item.status is not WorkStatus.SCHEDULED:
            raise InvalidStateError(f"{handle} is {item.status.value}; expected SCHEDULED")
        self._budget.spend(item.cost, f"compute:{item.spec.kind}")   # hard cost guard
        item.status = WorkStatus.PLACED
        self._adapter.place(handle, item.spec)                       # external execution

    def cost(self, handle: str) -> float:
        return self._require(handle).cost

    # ── tracking + cancellation ───────────────────────────────────────────────
    def status(self, handle: str) -> WorkStatus:
        return self._require(handle).status

    def cancel(self, handle: str) -> None:
        """Cancel work. Placed work is cancelled at the adapter; scheduled work is dropped
        before execution. Already-charged cost is not refunded."""
        item = self._require(handle)
        if item.status is WorkStatus.CANCELLED:
            return
        if item.status is WorkStatus.PLACED:
            self._adapter.cancel(handle)
        item.status = WorkStatus.CANCELLED

    def handles(self) -> tuple[str, ...]:
        return tuple(self._work.keys())

    def _require(self, handle: str) -> _WorkItem:
        item = self._work.get(handle)
        if item is None:
            raise UnknownHandleError(handle)
        return item
