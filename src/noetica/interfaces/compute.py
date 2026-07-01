"""ComputeInterface — abstract compute request/placement/cap (infra is EXTERNAL).

Purpose: how the system asks for and bounds compute, independent of any vendor.
    Infrastructure (cloud/K8s/GPU/edge) is external to the four layers; domains own the
    concrete adapters; the running of containers/hardware belongs to the infra itself.
Owner: Noetica (Layer 2) owns the interface + budgeting (§6.21).
Consumer: Velith; Mini Prometheus (implement concrete adapters).
Constitution: §6.21 (Amendment 3, Infrastructure Ownership); §9.2 matrix.
Future implementation owner: DOMAIN adapters (solver-cluster, GPU-scheduler, edge);
    Noetica ships the interface + BudgetMeter binding.

Interface surface only (PE-1). No adapter/infra here.
"""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ComputeInterface(Protocol):
    """Request, place, and cap a unit of compute work. Vendor-neutral."""

    def request(self, spec: Any) -> str: ...                # returns a work handle
    def place(self, handle: str) -> None: ...
    def cost(self, handle: str) -> float: ...
