"""PE-9 unit tests — Guardrails / Safety Policy Engine (§6.16, Law 17).

Platform tests: policy evaluation only; the engine never executes actions.
"""
from __future__ import annotations

import dataclasses

import pytest

from noetica.interfaces.guardrail import Decision, Guardrail
from noetica.guardrails import FunctionPolicy, GuardrailEngine, allow_all, deny_all


def test_engine_satisfies_guardrail_protocol() -> None:
    assert isinstance(GuardrailEngine(), Guardrail)


def test_empty_engine_allows() -> None:
    assert GuardrailEngine().check({"op": "noop"}).allowed is True


def test_oversight_denial_is_final_and_prefixed() -> None:
    eng = GuardrailEngine(oversight=(deny_all("oversight_boundary", "not permitted"),))
    d = eng.check({"op": "x"})
    assert d.allowed is False
    assert d.reason.startswith("oversight:oversight_boundary")


def test_domain_denial_denies_with_policy_prefix() -> None:
    eng = GuardrailEngine(domain=(deny_all("no_writes", "writes blocked"),))
    d = eng.check({"op": "write"})
    assert d.allowed is False and d.reason.startswith("policy:no_writes")


def test_oversight_deny_cannot_be_overridden_by_domain_allow() -> None:
    # Oversight denies; a permissive domain policy must NOT be able to allow it (Law 17).
    eng = GuardrailEngine(
        oversight=(deny_all("boundary", "final"),),
        domain=(allow_all("permit_everything"),),
    )
    assert eng.check({"op": "x"}).allowed is False


def test_with_domain_policy_is_immutable_and_preserves_oversight() -> None:
    base = GuardrailEngine(oversight=(allow_all("boundary"),))
    extended = base.with_domain_policy(deny_all("no_delete", "delete blocked"))
    assert base.domain == ()                          # original unchanged
    assert extended.oversight == base.oversight       # oversight carried over intact
    assert extended is not base
    assert extended.check({"op": "delete"}).allowed is False


def test_engine_is_frozen_oversight_cannot_be_reassigned() -> None:
    eng = GuardrailEngine(oversight=(allow_all("boundary"),))
    with pytest.raises(dataclasses.FrozenInstanceError):
        eng.oversight = ()  # type: ignore[misc]   # Law 17: boundary is immutable


def test_check_does_not_execute_the_action() -> None:
    executed = {"ran": False}

    def side_effect() -> None:
        executed["ran"] = True

    # A policy inspects the action's shape but the engine never calls the callable.
    def inspects(action: object) -> Decision:
        assert isinstance(action, dict) and "run" in action
        return Decision(allowed=True)

    eng = GuardrailEngine(domain=(FunctionPolicy("inspect", inspects),))
    result = eng.check({"run": side_effect})
    assert result.allowed is True
    assert executed["ran"] is False                   # action was NOT executed
