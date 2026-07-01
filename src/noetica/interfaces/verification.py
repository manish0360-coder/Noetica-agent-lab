"""Verifier / Verdict — the verification *protocol* (the oracle stays in the domain).

Purpose: define how a candidate is admitted or rejected against grounded truth, and the
    closed-taxonomy outcome (which may be a distribution with calibrated uncertainty).
Owner: Noetica (Layer 2) owns the PROTOCOL and the `Verdict` type.
Consumer: Velith; Mini Prometheus.
Constitution: §6.11; Law 15 (protocol above / oracle in domain); Law 16 (verdicts may
    be distributions; grounding honest); D16.7 / D17 (taxonomy; flaky is provenance).
Future implementation owner: the DOMAIN — Velith `SweVerifier` (SWE), later FEA/SPICE;
    Mini Prometheus manufacturing checks. Noetica ships only a reference/fake verifier
    for its own self-tests (Law 20).

Interface surface only (PE-1). No implementation, no oracle.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Protocol, runtime_checkable


class VerdictStatus(str, Enum):
    """Closed grounded-outcome taxonomy (D16.7). Measurement-quality signals (e.g.
    flakiness) are provenance, never members here (D17/D21)."""

    PASSED = "PASSED"
    FAILED = "FAILED"
    PATCH_APPLY_FAILED = "PATCH_APPLY_FAILED"
    NO_PATCH = "NO_PATCH"
    INFRA_ERROR = "INFRA_ERROR"


@dataclass(frozen=True)
class Verdict:
    """Grounded outcome of verification. Distribution-capable via `confidence` so an
    approximate oracle can be honest (Law 16). Schema only — no validation logic here."""

    status: VerdictStatus
    confidence: float = 1.0                        # 1.0 = exact (zero model-gap, SWE)
    detail: Mapping[str, Any] = field(default_factory=dict)  # provenance-side signals
    schema_version: str = "0.1.0"


@runtime_checkable
class Verifier(Protocol):
    """The verification protocol. A domain supplies the concrete oracle."""

    def verify(self, task: Any, candidate: Any) -> Verdict: ...
