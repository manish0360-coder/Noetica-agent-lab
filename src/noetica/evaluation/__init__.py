"""Noetica · evaluation — Evaluation Harness & Held-out Lock (§6.10).

The experiment machinery: arms, a mechanically-locked immutable held-out set, frozen
benchmark execution, provenance recording, and integrity enforcement. It measures
mechanisms and NEVER improves them during execution. PE-17 provides `EvaluationHarness`,
`Arm`, `HeldoutDataset`. Self-tests use only the ReferenceVerifier (Law 20). No reasoning/
planning/optimization/tuning/domain-eval/engineering-oracles.
"""
from __future__ import annotations

from noetica.evaluation.arm import Arm
from noetica.evaluation.harness import (
    DuplicateArmError,
    EvaluationHarness,
    FrozenEvaluationViolation,
)
from noetica.evaluation.heldout import HeldoutDataset, HeldoutViolation

__all__ = [
    "EvaluationHarness",
    "Arm",
    "HeldoutDataset",
    "HeldoutViolation",
    "FrozenEvaluationViolation",
    "DuplicateArmError",
]
