"""Versioned serialization for budget records (Law 21).

Purpose: JSON-safe, versioned wire form for ledger entries and meter snapshots (audit).
Owner: Noetica (Layer 2). Consumer: observability/audit; Velith; Mini Prometheus.
Constitution: §6.14; Law 21; §11.7.
Future implementation owner: Noetica.
"""
from __future__ import annotations

from typing import Any, Mapping

from noetica.budget.records import SCHEMA_VERSION, BudgetSnapshot, LedgerEntry


def serialize_ledger_entry(e: LedgerEntry) -> dict[str, Any]:
    return {
        "schema_version": e.schema_version,
        "amount": e.amount,
        "reason": e.reason,
        "cumulative": e.cumulative,
    }


def deserialize_ledger_entry(d: Mapping[str, Any]) -> LedgerEntry:
    return LedgerEntry(
        amount=d["amount"],
        reason=d["reason"],
        cumulative=d["cumulative"],
        schema_version=d.get("schema_version", SCHEMA_VERSION),
    )


def serialize_snapshot(s: BudgetSnapshot) -> dict[str, Any]:
    return {
        "schema_version": s.schema_version,
        "limit": s.limit,
        "spent": s.spent,
        "remaining": s.remaining,
        "exceeded": s.exceeded,
        "ledger": [serialize_ledger_entry(e) for e in s.ledger],
    }


def deserialize_snapshot(d: Mapping[str, Any]) -> BudgetSnapshot:
    return BudgetSnapshot(
        limit=d["limit"],
        spent=d["spent"],
        remaining=d["remaining"],
        exceeded=d["exceeded"],
        ledger=tuple(deserialize_ledger_entry(e) for e in d.get("ledger", [])),
        schema_version=d.get("schema_version", SCHEMA_VERSION),
    )
