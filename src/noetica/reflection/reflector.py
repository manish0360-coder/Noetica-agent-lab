"""GroundedReflector — the default self-critique mechanism (§6.9, DN-7, Law 7).

Inspects an attempt against its GROUNDED outcome (a Verdict) and proposes a revision. The
critique is deterministic and uses the verifier's verdict — never a model opinion
(never LLM-as-judge). A validated critique strategy may be injected (the promotion path for
a MiniFlyWire-validated reflection primitive, Law 7). Optionally records the critique to the
State blackboard with provenance. Self-critique ONLY: no planning/reasoning ownership, no
runtime lifecycle, no autonomous agent, no conversation loop, no domain logic; no other
platform mechanism imported.
"""
from __future__ import annotations

import uuid
from collections.abc import Callable
from typing import Any

from noetica.interfaces.provenance import Provenance
from noetica.interfaces.state import StateSubstrate
from noetica.interfaces.verification import Verdict, VerdictStatus
from noetica.reflection.models import Revision

CritiqueStrategy = Callable[[Any, Any], Revision]


def _verdict_of(outcome: Any) -> Verdict | None:
    if isinstance(outcome, Verdict):
        return outcome
    candidate = getattr(outcome, "verdict", None)  # e.g. an Episode carries a Verdict
    return candidate if isinstance(candidate, Verdict) else None


def grounded_critique(attempt: Any, outcome: Any) -> Revision:
    """Default critique: revise unless the grounded verdict PASSED."""
    verdict = _verdict_of(outcome)
    if verdict is None:
        return Revision(revise=True, attempt=attempt, feedback="ungrounded outcome; revise")
    if verdict.status is VerdictStatus.PASSED:
        return Revision(revise=False, attempt=attempt, feedback="verified: no revision needed")
    return Revision(
        revise=True,
        attempt=attempt,
        feedback=f"verdict={verdict.status.value} detail={dict(verdict.detail)}",
    )


class GroundedReflector:
    """Self-critique mechanism. Default strategy is grounded (verdict-based); a validated
    strategy may be injected. Satisfies the `Reflector` interface."""

    def __init__(
        self,
        *,
        strategy: CritiqueStrategy | None = None,
        state: StateSubstrate | None = None,
    ) -> None:
        self._strategy = strategy if strategy is not None else grounded_critique
        self._state = state

    def reflect(self, attempt: Any, outcome: Any, run_id: str | None = None, index: int = 0) -> Revision:
        revision = self._strategy(attempt, outcome)
        if self._state is not None:
            rid = run_id if run_id is not None else uuid.uuid4().hex
            provenance = Provenance(source="reflection", transform="critique", inputs=(str(attempt),))
            self._state.put(
                f"reflection:{rid}:{index}",
                {"revise": revision.revise, "feedback": revision.feedback},
                provenance,
            )
        return revision
