"""InMemoryBudgetMeter — the default Budget & Meta-control mechanism (§6.14).

Purpose: meter and HARD-cap the cost of computation — the bounded-rationality primitive
    that lets the system reason about how much to think and stop before bankruptcy.
Owner: Noetica (Layer 2).
Consumer: Model Router (PE-10), Compute (PE-11), Tool (PE-12), Reasoning (PE-18); Runtime.
Constitution: §6.14; Principle 5 ("computation is a costly act").
Future implementation owner: Noetica (this default; a LEARNED meta-control policy is gated
    PE-G5, Appendix D — not built here).

Scope: the budget METER only. No router, compute, memory, knowledge, context, reasoning,
planning, or runtime; no learned policy; no domain content. Depends on no other platform
mechanism (structurally satisfies the `BudgetMeter` interface).
"""
from __future__ import annotations

from noetica.budget.records import BudgetSnapshot, LedgerEntry


class BudgetExceededError(RuntimeError):
    """Raised when a spend would exceed the remaining budget (the hard cost guard)."""


class InMemoryBudgetMeter:
    """Append-only budget meter with a hard cap. Satisfies `BudgetMeter` (spend/remaining/
    exceeded) and adds a pre-check, ledger, and snapshot."""

    def __init__(self, limit: float) -> None:
        if limit < 0:
            raise ValueError("budget limit must be non-negative")
        self._limit = float(limit)
        self._spent = 0.0
        self._ledger: list[LedgerEntry] = []

    # ── BudgetMeter interface ───────────────────────────────────────────────────
    def spend(self, amount: float, reason: str) -> None:
        """Record a spend. HARD guard: raises BudgetExceededError if it would overspend;
        the meter state is left unchanged in that case."""
        if amount < 0:
            raise ValueError("spend amount must be non-negative")
        if self._spent + amount > self._limit:
            raise BudgetExceededError(
                f"spend {amount} for {reason!r} exceeds remaining {self.remaining()}"
            )
        self._spent += amount
        self._ledger.append(
            LedgerEntry(amount=amount, reason=reason, cumulative=self._spent)
        )

    def remaining(self) -> float:
        return self._limit - self._spent

    def exceeded(self) -> bool:
        """True when the budget is exhausted (no remaining budget)."""
        return self.remaining() <= 0

    # ── meta-control surface ────────────────────────────────────────────────────
    def can_spend(self, amount: float) -> bool:
        """Pre-check: can this amount be spent without exceeding the cap?"""
        return amount >= 0 and (self._spent + amount) <= self._limit

    @property
    def limit(self) -> float:
        return self._limit

    @property
    def spent(self) -> float:
        return self._spent

    def ledger(self) -> tuple[LedgerEntry, ...]:
        return tuple(self._ledger)

    def snapshot(self) -> BudgetSnapshot:
        return BudgetSnapshot(
            limit=self._limit,
            spent=self._spent,
            remaining=self.remaining(),
            exceeded=self.exceeded(),
            ledger=tuple(self._ledger),
        )
