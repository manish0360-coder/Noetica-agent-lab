"""Typed, immutable budget records.

Purpose: the value types the budget meter produces — an immutable ledger entry per spend
    and an immutable snapshot of meter state, for audit.
Owner: Noetica (Layer 2).
Consumer: Model Router (PE-10), Compute (PE-11), Tool (PE-12), Reasoning (PE-18); Velith;
    Mini Prometheus.
Constitution: §6.14 (bounded rationality); Principle 5; Law 21 (schema_version).
Future implementation owner: Noetica.
"""
from __future__ import annotations

from dataclasses import dataclass

SCHEMA_VERSION = "0.1.0"


@dataclass(frozen=True)
class LedgerEntry:
    """One immutable record of a spend: the amount, its reason, and the cumulative total."""

    amount: float
    reason: str
    cumulative: float
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class BudgetSnapshot:
    """Immutable snapshot of meter state at a point in time."""

    limit: float
    spent: float
    remaining: float
    exceeded: bool
    ledger: tuple[LedgerEntry, ...]
    schema_version: str = SCHEMA_VERSION
