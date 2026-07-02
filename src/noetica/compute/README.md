# src/noetica/compute — Compute Interface & Budgeting

**Constitution:** §6.21 (Amendment 3 — Infrastructure Ownership; infra is external to the
four layers), §6.14 (budget cost guard), Principle 9 (wrap, don't rebuild).

## Purpose
A vendor-neutral abstraction to **schedule, execute (via an adapter), track, and cancel**
compute work, enforcing budget limits through the `BudgetMeter` interface. Noetica owns the
compute *interface + budgeting*; domains own the *adapters*; external infrastructure owns
*execution*.

## Responsibilities
- `request(spec)` — schedule work (budget pre-check / cost guard); assign a handle.
- `place(handle)` — charge the budget (**hard cost guard**) and delegate execution to the
  external `ExecutionAdapter`.
- `cost(handle)` / `status(handle)` — track work.
- `cancel(handle)` — cancel placed work at the adapter, or drop scheduled work.

## Non-responsibilities (NOT here)
- **Kubernetes, Docker, cloud providers, GPUs, engineering solvers, Velith adapters,
  infrastructure orchestration** — external; concrete adapters implement `ExecutionAdapter`
  and live in domain/external code, never in the platform.
- **Runtime behavior, reasoning, planning** — separate subsystems.
- Refunding already-charged cost on cancel (charged spend is committed).

## Dependencies
- `noetica.interfaces.budget.BudgetMeter` (a concrete meter — e.g. PE-6 — is injected);
  `noetica.compute.spec` / `.adapter`.
- Python standard library only. No vendor SDK, no other layer, no `reference/`.

## Consumers
- Runtime (PE-21); Velith / Mini Prometheus implement concrete `ExecutionAdapter`s.

## Constitution references
§6.21 · §6.14 · Principle 9.

## Future implementation milestones
- **Now (PE-11):** `ComputeSpec`/`WorkStatus`, `ExecutionAdapter` seam, `ComputeBroker`.
- **Later (domain/external):** concrete adapters (local, solver-cluster, GPU, edge, OPC UA)
  behind `ExecutionAdapter`; async completion polling by extraction (Law 8).
