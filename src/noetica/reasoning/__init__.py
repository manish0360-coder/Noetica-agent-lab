"""Noetica · reasoning — Reasoning Runtime (§6.7). The FORM of reasoning only.

PE-18: `ReasoningRuntime` — iterate inference (Router), verification seam (Verifier),
backtrack/retry within Budget, as a control plane over the State substrate (DN-7). Owns no
planning/reflection/memory/knowledge/context/tool-execution/state/verification-oracle/
runtime-lifecycle; capabilities are injected. No conversation loop / agent / homunculus /
self-critique / domain logic.
"""
from __future__ import annotations

from noetica.reasoning.models import ReasoningResult, ReasoningStep
from noetica.reasoning.runtime import ReasoningRuntime

__all__ = ["ReasoningRuntime", "ReasoningStep", "ReasoningResult"]
