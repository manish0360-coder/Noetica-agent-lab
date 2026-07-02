"""ContextEngine — the default Context assembler (§6.6).

Purpose: assemble a BOUNDED working context for a SINGLE inference by combining State,
    Memory, and Knowledge according to an EXPLICIT policy and a token budget. It performs
    no reasoning, retrieval optimization, or ranking — it includes exactly what the policy
    names, in a fixed source order, truncated to fit the budget.
Owner: Noetica (Layer 2).
Consumer: Reasoning (PE-18), Runtime (PE-21).
Constitution: §6.6; §6.20 (Context distinct from Memory/Knowledge — a momentary assembly);
    Law 13.
Future implementation owner: Noetica.

Scope: working-set assembly + budget truncation ONLY. NO reasoning, planning, reflection,
retrieval optimization, ranking heuristics, autonomous behavior, prompt construction, or
domain logic. Context is TEMPORARY — the engine owns no persistence; State/Memory/Knowledge
are injected references it reads but does not own.
"""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from noetica.context.models import ContextItem, ContextPolicy
from noetica.interfaces.context import Context
from noetica.interfaces.knowledge import KnowledgeStore
from noetica.interfaces.memory import MemoryStore
from noetica.interfaces.state import StateSubstrate


def _default_cost(content: Any) -> int:
    """A simple, deterministic budget cost (crude token estimate). Not a ranking signal."""
    return max(1, len(str(content)) // 4)


class ContextEngine:
    """Assembles a bounded working set from injected State/Memory/Knowledge per an explicit
    policy. Owns none of them; returns a temporary `Context`."""

    def __init__(
        self,
        state: StateSubstrate,
        memory: MemoryStore,
        knowledge: KnowledgeStore,
        policy: ContextPolicy,
        cost_fn: Callable[[Any], int] | None = None,
    ) -> None:
        self._state = state
        self._memory = memory
        self._knowledge = knowledge
        self._policy = policy
        self._cost = cost_fn if cost_fn is not None else _default_cost

    def assemble(self, goal: Any, token_budget: int) -> Context:
        collected = self._collect(goal)
        chosen = self._apply_budget(collected, token_budget)
        return Context(items=tuple(chosen), token_budget=token_budget)

    def _collect(self, goal: Any) -> list[ContextItem]:
        items: list[ContextItem] = []
        # 1) State — exact keys, in policy order.
        for key in self._policy.state_keys:
            value = self._state.get(key)
            if value is not None:
                items.append(ContextItem("state", key, value, self._cost(value)))
        # 2) Memory — the store's fixed recency retriever (no optimization here).
        if self._policy.memory_k > 0:
            for episode in self._memory.recall(goal, self._policy.memory_k):
                items.append(
                    ContextItem("memory", str(getattr(episode, "task_id", "")), episode, self._cost(episode))
                )
        # 3) Knowledge — the explicit query pattern from the policy.
        if self._policy.knowledge_query is not None:
            for record in self._knowledge.query(self._policy.knowledge_query):
                ref = getattr(record, "entity_id", getattr(record, "subject", ""))
                items.append(ContextItem("knowledge", str(ref), record, self._cost(record)))
        return items

    def _apply_budget(self, items: list[ContextItem], token_budget: int) -> list[ContextItem]:
        if token_budget <= 0:
            return []
        chosen: list[ContextItem] = []
        total = 0
        for item in items:
            if total + item.cost > token_budget:
                break  # prefix truncation in explicit order — no optimization/reordering
            chosen.append(item)
            total += item.cost
        return chosen
