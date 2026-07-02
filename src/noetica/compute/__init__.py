"""Noetica · compute — Compute Interface & Budgeting (§6.21).

A vendor-neutral abstraction to schedule/execute/track/cancel compute work while enforcing
budget limits — infrastructure stays EXTERNAL to the four layers. PE-11 provides
`ComputeSpec`/`WorkStatus`, the `ExecutionAdapter` seam (domains/external implement it),
and the default `ComputeBroker`. No cloud/K8s/Docker/GPU/solver/provider code.
"""
from __future__ import annotations

from noetica.compute.adapter import ExecutionAdapter
from noetica.compute.broker import (
    ComputeBroker,
    ComputeBudgetError,
    ComputeError,
    InvalidStateError,
    UnknownHandleError,
)
from noetica.compute.spec import SCHEMA_VERSION, ComputeSpec, WorkStatus

__all__ = [
    "ComputeBroker",
    "ComputeSpec",
    "WorkStatus",
    "ExecutionAdapter",
    "ComputeError",
    "UnknownHandleError",
    "ComputeBudgetError",
    "InvalidStateError",
    "SCHEMA_VERSION",
]
