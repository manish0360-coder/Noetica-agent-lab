"""ExecutionAdapter — the seam behind which external infrastructure executes work.

Purpose: the interface concrete infra adapters implement (local, solver-cluster, GPU
    scheduler, edge/robot, OPC UA bridge). Noetica owns the interface; domains own the
    adapters; the actual running of containers/pods/hardware belongs to the infrastructure
    itself, outside the four layers (§6.21). No adapter is implemented in the platform.
Owner: Noetica (Layer 2) — the interface only.
Consumer: ComputeBroker delegates execution to an adapter.
Constitution: §6.21 (Infrastructure Ownership); Principle 9 (wrap, don't rebuild).
Future implementation owner: DOMAIN / external (concrete adapters), never here.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from noetica.compute.spec import ComputeSpec


@runtime_checkable
class ExecutionAdapter(Protocol):
    """Executes/cancels placed work on external infrastructure. Vendor-neutral seam."""

    name: str

    def place(self, handle: str, spec: ComputeSpec) -> None: ...

    def cancel(self, handle: str) -> None: ...
