"""Context items and the explicit assembly policy.

Purpose: the typed pieces of a working set and the EXPLICIT, declarative policy that says
    what to include (specific state keys, N recent memory episodes, an explicit knowledge
    query) — no smart retrieval, no ranking.
Owner: Noetica (Layer 2).
Consumer: ContextEngine; Reasoning (PE-18); Runtime (PE-21).
Constitution: §6.6; §6.20 (Context = momentary assembly, distinct from Memory/Knowledge);
    Law 21 (schema_version).
Future implementation owner: Noetica.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

SCHEMA_VERSION = "0.1.0"


@dataclass(frozen=True)
class ContextItem:
    """One piece of a working set: its source, a reference, the content, and its cost."""

    source: str          # "state" | "memory" | "knowledge"
    ref: str             # state key / episode id / entity id
    content: Any
    cost: int            # budget cost (e.g., token estimate)
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class ContextPolicy:
    """Explicit, declarative assembly policy. No ranking/optimization — the engine includes
    exactly what is named, in a fixed source order, under the budget."""

    state_keys: tuple[str, ...] = ()      # exact state keys to include
    memory_k: int = 0                     # number of most-recent memory episodes
    knowledge_query: Any = None           # an explicit knowledge query pattern (or None)
