"""Noetica · guardrails — Safety Policy Engine (§6.16, Law 17).

Noetica owns the engine that enforces policy, including the IMMUTABLE human-oversight
boundary the system may never modify (Law 17). Domains supply domain-policy content. PE-9
provides `GuardrailEngine` (evaluates policies, returns decisions, never executes actions)
and the `Policy`/`FunctionPolicy` abstraction. No reasoning/planning/runtime/domain rules.
"""
from __future__ import annotations

from noetica.guardrails.engine import GuardrailEngine
from noetica.guardrails.policy import FunctionPolicy, Policy, allow_all, deny_all

__all__ = ["GuardrailEngine", "Policy", "FunctionPolicy", "allow_all", "deny_all"]
