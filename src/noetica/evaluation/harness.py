"""EvaluationHarness — the default evaluation engine (§6.10).

Purpose: run experiment arms over a locked held-out benchmark under FROZEN evaluation, and
    measure them — it exists ONLY to measure mechanisms, never to improve them during
    execution. It performs no memory/state writes; it records provenance-complete eval
    episodes; it mechanically enforces the held-out lock and the frozen discipline.
Owner: Noetica (Layer 2).
Consumer: Velith configures arms A0–A4; Mini Prometheus.
Constitution: §6.10; §5.6 (held-out lock, frozen eval); D8; §11.10; Law 20 (self-tests use
    the reference/fake verifier only).
Future implementation owner: Noetica.

Scope: arm management + frozen benchmark execution + held-out locking + provenance +
integrity enforcement ONLY. NO reasoning, planning, reflection, runtime behavior,
optimization policies, benchmark tuning, domain-specific evaluation, or engineering oracles
(the oracle is the injected Verifier; self-tests use only the ReferenceVerifier).
"""
from __future__ import annotations

from typing import Any

from noetica.evaluation.arm import Arm
from noetica.evaluation.heldout import HeldoutDataset, HeldoutViolation
from noetica.interfaces.episode import Episode
from noetica.interfaces.evaluation import EvalResult
from noetica.interfaces.provenance import Provenance
from noetica.interfaces.verification import Verdict, VerdictStatus, Verifier


class FrozenEvaluationViolation(RuntimeError):
    """Raised when an arm's memory or state is modified during evaluation (not frozen)."""


class DuplicateArmError(RuntimeError):
    """An arm with the given name is already registered."""


class EvaluationHarness:
    """Frozen evaluation engine over a locked held-out set. Measures arms; never mutates
    them. Satisfies the `EvalHarness` interface (register_arm/run)."""

    def __init__(self, verifier: Verifier, heldout: HeldoutDataset) -> None:
        self._verifier = verifier
        self._heldout = heldout
        self._arms: dict[str, Arm] = {}
        self._episodes: list[Episode] = []

    def register_arm(self, name: str, config: Any) -> None:
        if not isinstance(config, Arm):
            raise TypeError("arm config must be an Arm")
        if name in self._arms:
            raise DuplicateArmError(name)
        self._arms[name] = config

    def run(self) -> EvalResult:
        metrics: dict[str, float] = {}
        for name, arm in self._arms.items():
            rev_before = arm.state.revision if arm.state is not None else None
            mem_before = {e.task_id for e in arm.memory} if arm.memory is not None else set()

            passed = 0
            total = 0
            for task in self._heldout:
                candidate = arm.solver(task)
                verdict: Verdict = self._verifier.verify(task, candidate)
                self._episodes.append(
                    Episode(
                        task_id=task,
                        verdict=verdict,
                        provenance=Provenance(source="eval", transform=f"arm:{name}", inputs=(task,)),
                    )
                )
                total += 1
                if verdict.status is VerdictStatus.PASSED:
                    passed += 1

            self._enforce_integrity(name, arm, rev_before, mem_before)

            metrics[f"{name}.pass_rate"] = (passed / total) if total else 0.0
            metrics[f"{name}.n"] = float(total)

        return EvalResult(metrics=metrics)

    def episodes(self) -> tuple[Episode, ...]:
        """Provenance-complete eval episodes (harness log; never written to arm memory)."""
        return tuple(self._episodes)

    def _enforce_integrity(
        self, name: str, arm: Arm, rev_before: int | None, mem_before: set[str]
    ) -> None:
        # Frozen: state must be unchanged during measurement.
        if arm.state is not None and arm.state.revision != rev_before:
            raise FrozenEvaluationViolation(f"arm {name!r}: state modified during evaluation")
        if arm.memory is not None:
            mem_after = {e.task_id for e in arm.memory}
            # Held-out lock: no held-out task may be present in memory.
            leaked = self._heldout.ids & mem_after
            if leaked:
                raise HeldoutViolation(f"arm {name!r}: held-out tasks in memory: {sorted(leaked)}")
            # Frozen: memory must be unchanged during measurement.
            if mem_after != mem_before:
                raise FrozenEvaluationViolation(f"arm {name!r}: memory modified during evaluation")
