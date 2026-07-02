"""Guardrail policy abstraction.

Purpose: the unit the safety engine evaluates — a named policy that maps an action to an
    allow/deny `Decision`. Domains supply domain-policy *content*; Noetica supplies the
    engine and the policy abstraction (§6.16).
Owner: Noetica (Layer 2).
Consumer: GuardrailEngine; Runtime (PE-21); domains supply concrete policy content.
Constitution: §6.16; Law 17.
Future implementation owner: Noetica (abstraction); domains (policy content).

A policy only EVALUATES an action and returns a Decision — it never executes the action.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from noetica.interfaces.guardrail import Decision


@runtime_checkable
class Policy(Protocol):
    """A named, side-effect-free policy: evaluate an action, return a Decision."""

    name: str

    def evaluate(self, action: Any) -> Decision: ...


@dataclass(frozen=True)
class FunctionPolicy:
    """Adapt a pure predicate `(action) -> Decision` into a named Policy."""

    name: str
    predicate: Callable[[Any], Decision]

    def evaluate(self, action: Any) -> Decision:
        return self.predicate(action)


def allow_all(name: str = "allow_all") -> FunctionPolicy:
    return FunctionPolicy(name, lambda action: Decision(allowed=True))


def deny_all(name: str = "deny_all", reason: str = "denied") -> FunctionPolicy:
    return FunctionPolicy(name, lambda action: Decision(allowed=False, reason=reason))
