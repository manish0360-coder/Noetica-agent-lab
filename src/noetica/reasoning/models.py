"""Reasoning step/result value types (form only; no domain content)."""
from __future__ import annotations

from dataclasses import dataclass

from noetica.interfaces.provenance import Provenance
from noetica.interfaces.verification import Verdict

SCHEMA_VERSION = "0.1.0"


@dataclass(frozen=True)
class ReasoningStep:
    """One inference iteration: the candidate produced and its grounded verdict."""

    index: int
    candidate: str
    verdict: Verdict
    provenance: Provenance
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class ReasoningResult:
    """Outcome of a bounded reasoning run: success and the sequence of steps."""

    goal: str
    success: bool
    steps: tuple[ReasoningStep, ...]
    final: ReasoningStep | None
    schema_version: str = SCHEMA_VERSION
