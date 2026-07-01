"""Context — working-set assembly + window budgeting for a SINGLE inference.

Purpose: select, from memory and the knowledge store, the relevant subset for one act
    of cognition (driven by causal relevance and active constraints, not similarity
    alone). Distinct from Memory (persistence) and Knowledge (structured store).
Owner: Noetica (Layer 2) (§6.6).
Consumer: Velith; Mini Prometheus.
Constitution: §6.6; §6.20; Law 13.
Future implementation owner: Noetica (default assembler).

Interface surface only (PE-1). No selection algorithm here.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class Context:
    """The momentary working set for one inference. Schema only."""

    items: tuple[Any, ...] = ()
    token_budget: int = 0
    schema_version: str = "0.1.0"


@runtime_checkable
class ContextAssembler(Protocol):
    """Assembles a Context under a token budget for one inference step."""

    def assemble(self, goal: Any, token_budget: int) -> Context: ...
