"""EvalHarness — the experiment machinery (arms, held-out lock, metrics).

Purpose: own measurement discipline ONCE and reuse it across every vertical and rung —
    arms, the mechanically-enforced held-out lock, frozen evaluation, metrics.
Owner: Noetica (Layer 2) (§6.10).
Consumer: Velith (configures arms A0–A4); Mini Prometheus.
Constitution: §6.10; §5.6; D8; §11.10 (integrity checks); Law 20 (fake verifier in
    Noetica self-tests).
Future implementation owner: Noetica (default harness); domains configure, never rebuild.

Interface surface only (PE-1). No experiment logic here.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, runtime_checkable


@dataclass(frozen=True)
class EvalResult:
    """Frozen-evaluation result. Schema only (effect size + spread reported by impl)."""

    metrics: Mapping[str, float] = field(default_factory=dict)
    schema_version: str = "0.1.0"


@runtime_checkable
class EvalHarness(Protocol):
    """Runs arms under a held-out lock and returns frozen-evaluation results."""

    def register_arm(self, name: str, config: Any) -> None: ...
    def run(self) -> EvalResult: ...
