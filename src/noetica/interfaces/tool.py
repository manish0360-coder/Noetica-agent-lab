"""Tool — the tool system interface ("wrap, don't rebuild").

Purpose: register, invoke, and sandbox external capabilities. Noetica owns the
    mechanism; the concrete tools are wrapped external kernels owned by domains. Long-
    running tools require async/non-blocking invocation (the loop must never block).
Owner: Noetica (Layer 2) owns the interface + runtime (§6.12).
Consumer: Velith (CAD, solvers); Mini Prometheus (MES, PLC, robots).
Constitution: §6.12; Principle 9 (wrap, don't rebuild).
Future implementation owner: DOMAIN (concrete tools); Noetica ships the runtime.

Interface surface only (PE-1). No tool implementation here.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, runtime_checkable


@dataclass(frozen=True)
class ToolResult:
    """Result of a tool invocation. Schema only."""

    ok: bool
    output: Any = None
    detail: Mapping[str, Any] = field(default_factory=dict)


@runtime_checkable
class Tool(Protocol):
    """A wrapped external capability. Domains implement; Noetica registers/invokes."""

    name: str

    def invoke(self, **kwargs: Any) -> ToolResult: ...
