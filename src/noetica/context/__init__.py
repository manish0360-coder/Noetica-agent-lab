"""Noetica · context — Context Engine (§6.6).

Working-set assembly + window budgeting for a SINGLE inference — a momentary combination of
State, Memory, and Knowledge under an explicit policy and token budget (distinct from
Memory persistence and the Knowledge store, §6.20). PE-16 provides `ContextEngine`,
`ContextPolicy`, and `ContextItem`. No reasoning/planning/reflection/retrieval-optimization/
ranking/prompt-construction/domain logic; owns no persistence.
"""
from __future__ import annotations

from noetica.context.engine import ContextEngine
from noetica.context.models import SCHEMA_VERSION, ContextItem, ContextPolicy

__all__ = ["ContextEngine", "ContextPolicy", "ContextItem", "SCHEMA_VERSION"]
