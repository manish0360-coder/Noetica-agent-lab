# src/noetica/budget — Budget & Meta-control

**Constitution:** §6.14 (budget / meta-control), Principle 5 (bounded rationality is
first-class), Law 21 (versioned records).

## Purpose
Meter and **hard-cap** the cost of computation. Without meta-control the system either
under-thinks (cheap and wrong) or over-thinks (correct and bankrupt). This is the
bounded-rationality primitive: know how much has been spent, whether more can be afforded,
and stop before exceeding the cap.

## Responsibilities
- Track cumulative spend against a fixed limit; expose `remaining()` and `exceeded()`.
- Enforce a **hard cost guard**: `spend()` raises `BudgetExceededError` and leaves state
  unchanged if a spend would overspend.
- Offer a `can_spend()` pre-check (the meta-control question "can I afford this?").
- Keep an immutable **ledger** and `snapshot()` for audit; versioned serialization (Law 21).

## Non-responsibilities (NOT here)
- **Model Router** (§6.15) and **Compute** (§6.21) — they *consume* this meter's guard.
- **Memory**, **Knowledge**, **Context**, **Reasoning**, **Planning**, **Runtime**.
- A **learned** meta-control policy — gated **PE-G5** (Appendix D); this default is a
  hand-set cap only.
- Any domain cost model or content.

## Dependencies
- Structurally satisfies `noetica.interfaces.budget.BudgetMeter`.
- Python standard library only. **No other platform mechanism** (Tier-1), no other layer,
  no `reference/`.

## Consumers
- Model Router (PE-10), Compute (PE-11), Tool (PE-12), Reasoning (PE-18), Runtime (PE-21).
- Velith and Mini Prometheus meter their runs against it.

## Constitution references
§6.14 · Principle 5 · Law 21 · (learned policy: gated PE-G5, Appendix D).

## Future implementation milestones
- **Now (PE-6):** `InMemoryBudgetMeter` — hard-cap meter + ledger + snapshot.
- **Later (gated):** **learned meta-control policy** (PE-G5), gated on the compounding
  result (§1.7); multi-dimensional budgets (tokens/time/compute) by extraction (Law 8).
