"""Noetica · tools — Tool Runtime & Interface (§6.12).

The mechanism for registering, invoking, and sandboxing tools, with async non-blocking
invocation (the reasoning loop must never block on a long solve). Concrete tools are
wrapped external kernels owned by domains ("wrap, don't rebuild") — none here. PE-12
provides `ToolRuntime`. Consumes the BudgetMeter interface (injected).
"""
from __future__ import annotations

from noetica.tools.runtime import (
    DuplicateToolError,
    ToolBudgetError,
    ToolError,
    ToolRuntime,
    UnknownHandleError,
    UnknownToolError,
)

__all__ = [
    "ToolRuntime",
    "ToolError",
    "UnknownToolError",
    "DuplicateToolError",
    "ToolBudgetError",
    "UnknownHandleError",
]
