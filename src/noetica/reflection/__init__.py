"""Noetica · reflection — Reflection (§6.9). Self-critique mechanism (form only).

PE-20: `GroundedReflector` inspects an attempt against its grounded Verdict and proposes a
`Revision` — deterministic, verdict-based (never LLM-as-judge). A validated critique strategy
may be injected (Law 7). Self-critique only: no planning/reasoning ownership, no runtime
lifecycle, no agent, no conversation loop, no domain logic. Deps (Roadmap v1.1): Reasoning,
Episode, State — via interfaces; the revision feeds reasoning at the consumer (not imported).
"""
from __future__ import annotations

from noetica.reflection.models import Revision
from noetica.reflection.reflector import (
    CritiqueStrategy,
    GroundedReflector,
    grounded_critique,
)

__all__ = ["GroundedReflector", "Revision", "CritiqueStrategy", "grounded_critique"]
