"""PE-20 unit tests — Reflection (§6.9). Grounded self-critique; form only."""
from __future__ import annotations

from noetica.interfaces.episode import Episode
from noetica.interfaces.provenance import Provenance
from noetica.interfaces.reflection import Reflector
from noetica.interfaces.verification import Verdict, VerdictStatus
from noetica.reflection import GroundedReflector, Revision
from noetica.state import InMemoryStateSubstrate


def _v(status: VerdictStatus) -> Verdict:
    return Verdict(status=status)


def test_satisfies_reflector_protocol() -> None:
    assert isinstance(GroundedReflector(), Reflector)


def test_passed_verdict_needs_no_revision() -> None:
    rev = GroundedReflector().reflect("cand", _v(VerdictStatus.PASSED))
    assert rev.revise is False and "verified" in rev.feedback


def test_failed_verdict_proposes_revision_with_grounded_feedback() -> None:
    rev = GroundedReflector().reflect("cand", _v(VerdictStatus.FAILED))
    assert rev.revise is True and "FAILED" in rev.feedback


def test_reflect_on_episode_uses_its_verdict() -> None:
    ep = Episode(task_id="t", verdict=_v(VerdictStatus.FAILED),
                 provenance=Provenance(source="a", transform="p"))
    rev = GroundedReflector().reflect("cand", ep)
    assert rev.revise is True


def test_ungrounded_outcome_revises() -> None:
    rev = GroundedReflector().reflect("cand", outcome="not-a-verdict")
    assert rev.revise is True and "ungrounded" in rev.feedback


def test_injected_strategy_overrides_default() -> None:
    def always_stop(attempt: object, outcome: object) -> Revision:
        return Revision(revise=False, attempt=attempt, feedback="custom")

    rev = GroundedReflector(strategy=always_stop).reflect("cand", _v(VerdictStatus.FAILED))
    assert rev.revise is False and rev.feedback == "custom"


def test_writes_critique_to_state_blackboard() -> None:
    state = InMemoryStateSubstrate()
    GroundedReflector(state=state).reflect("cand", _v(VerdictStatus.FAILED), run_id="R1", index=2)
    rec = state.get_record("reflection:R1:2")
    assert rec is not None and rec.provenance.source == "reflection"


def test_deterministic() -> None:
    r = GroundedReflector()
    a = r.reflect("cand", _v(VerdictStatus.FAILED))
    b = r.reflect("cand", _v(VerdictStatus.FAILED))
    assert a == b
