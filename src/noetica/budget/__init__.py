"""Noetica · budget — Budget & Meta-control (§6.14).

Bounded rationality as a first-class mechanism: meter and HARD-cap the cost of
computation so the system reasons about how much to think and stops before bankruptcy.
PE-6 provides the default `InMemoryBudgetMeter`, immutable ledger/snapshot records, and
versioned serialization. Domain-agnostic; no router/compute/memory/runtime; the learned
meta-control policy is gated (PE-G5).
"""
from __future__ import annotations

from noetica.budget.meter import BudgetExceededError, InMemoryBudgetMeter
from noetica.budget.records import SCHEMA_VERSION, BudgetSnapshot, LedgerEntry
from noetica.budget.serialization import (
    deserialize_ledger_entry,
    deserialize_snapshot,
    serialize_ledger_entry,
    serialize_snapshot,
)

__all__ = [
    "InMemoryBudgetMeter",
    "BudgetExceededError",
    "LedgerEntry",
    "BudgetSnapshot",
    "SCHEMA_VERSION",
    "serialize_ledger_entry",
    "deserialize_ledger_entry",
    "serialize_snapshot",
    "deserialize_snapshot",
]
