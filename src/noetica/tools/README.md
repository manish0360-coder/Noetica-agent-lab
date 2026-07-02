# src/noetica/tools — Tool Runtime & Interface

**Constitution:** §6.12 (tool system + interface; async non-blocking), Principle 9
(wrap, don't rebuild), §6.14 (budget cost guard).

## Purpose
Register, invoke, and **sandbox** tools, with **async, non-blocking** invocation so the
reasoning loop never blocks on a multi-day solve. Noetica owns the runtime; the tools
themselves are wrapped external kernels owned by domains.

## Responsibilities
- `register(tool, cost)` — register a `Tool` by name (with an optional per-invocation cost).
- `invoke(name, **kwargs)` — synchronous, **sandboxed** (a raising tool becomes a failed
  `ToolResult`, never crashes the runtime), budget-charged.
- `submit / poll / result / cancel` — **non-blocking** async dispatch on a worker pool.
- Budget: each invocation charges the injected `BudgetMeter` (**hard guard**) before running.

## Non-responsibilities (NOT here)
- **Concrete tools / external kernels** (CAD, solvers, MES, robots) — domain-owned behind
  the `Tool` interface.
- **OS/container-level sandboxing** — that is infra (§6.21 adapters); here "sandbox" means
  fault isolation of tool exceptions.
- **Reasoning, planning, runtime orchestration, domain logic.**

## Dependencies
- `noetica.interfaces.tool` (`Tool`/`ToolResult`), `noetica.interfaces.budget.BudgetMeter`
  (a concrete meter — e.g. PE-6 — is injected). Python stdlib (`concurrent.futures`).
- No vendor SDK, no other layer, no `reference/`.

## Consumers
- Skill (PE-15), Reasoning (PE-18), Runtime (PE-21); domains implement concrete tools.

## Constitution references
§6.12 · Principle 9 · §6.14.

## Future implementation milestones
- **Now (PE-12):** `ToolRuntime` (register/invoke/sandbox + async submit/poll/result/cancel).
- **Later:** domain tools behind `Tool`; richer async (timeouts/quotas) and OS-sandbox
  adapters by extraction (Law 8).
