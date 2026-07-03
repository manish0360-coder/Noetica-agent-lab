"""Planning outcome value types (form only; no domain content)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from noetica.interfaces.plan import Plan, Step
from noetica.interfaces.provenance import Provenance

SCHEMA_VERSION = "0.1.0"


@dataclass(frozen=True)
class StepOutcome:
    index: int
    step: Step
    result: Any
    provenance: Provenance
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class ExecutionResult:
    plan: Plan
    run_id: str
    outcomes: tuple[StepOutcome, ...]
    success: bool
    schema_version: str = SCHEMA_VERSION
