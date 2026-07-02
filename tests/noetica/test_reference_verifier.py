"""PE-8 unit tests — ReferenceVerifier (§6.11, Law 20).

Platform tests: the reference/fake verifier only; no domain oracle (Law 20).
"""
from __future__ import annotations

from noetica.interfaces.verification import Verdict, VerdictStatus, Verifier
from noetica.verification import ReferenceVerifier, always


def test_satisfies_verifier_protocol() -> None:
    assert isinstance(ReferenceVerifier(), Verifier)


def test_default_is_passed_and_deterministic() -> None:
    v = ReferenceVerifier()
    a = v.verify("task1", "candidate")
    b = v.verify("task1", "candidate")
    assert a.status is VerdictStatus.PASSED
    assert a == b                                   # deterministic


def test_configured_default_verdict() -> None:
    v = ReferenceVerifier(default=Verdict(status=VerdictStatus.FAILED, confidence=0.5))
    out = v.verify("t", "c")
    assert out.status is VerdictStatus.FAILED and out.confidence == 0.5


def test_scripted_per_task_overrides_default() -> None:
    v = ReferenceVerifier(
        default=Verdict(status=VerdictStatus.PASSED),
        script={"bad": Verdict(status=VerdictStatus.FAILED)},
    )
    assert v.verify("bad", "x").status is VerdictStatus.FAILED     # scripted
    assert v.verify("good", "x").status is VerdictStatus.PASSED    # default


def test_custom_key_fn() -> None:
    v = ReferenceVerifier(
        script={"c1": Verdict(status=VerdictStatus.NO_PATCH)},
        key_fn=lambda task, candidate: str(candidate),
    )
    assert v.verify("t", "c1").status is VerdictStatus.NO_PATCH


def test_always_helper() -> None:
    v = always(VerdictStatus.INFRA_ERROR)
    assert v.verify("t", "c").status is VerdictStatus.INFRA_ERROR


def test_no_domain_inspection() -> None:
    # The candidate's domain "meaning" never affects the verdict — only the key/config do.
    v = ReferenceVerifier(default=Verdict(status=VerdictStatus.PASSED))
    assert v.verify("t", {"patch": "def broken(:"}).status is VerdictStatus.PASSED
    assert v.verify("t", 42).status is VerdictStatus.PASSED
