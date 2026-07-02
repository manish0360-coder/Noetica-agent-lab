"""Noetica · router — Model Abstraction & Routing (§6.15).

Make any model provider swappable behind one seam so the system's identity depends on no
single model or vendor (Principle 3), with a HARD cost guard (§6.14). PE-10 provides the
`ModelProvider` seam and the deterministic, budget-guarded `DefaultModelRouter`. No
vendor logic, prompt engineering, reasoning, planning, memory, or runtime.
"""
from __future__ import annotations

from noetica.router.provider import ModelProvider
from noetica.router.router import (
    BudgetGuardError,
    DefaultModelRouter,
    NoProviderError,
    RoutingError,
)

__all__ = [
    "DefaultModelRouter",
    "ModelProvider",
    "RoutingError",
    "NoProviderError",
    "BudgetGuardError",
]
