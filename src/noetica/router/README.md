# src/noetica/router — Model Abstraction & Routing

**Constitution:** §6.15 (model routing + cost guard), Principle 3 (LLMs are swappable
components), D16.4 (adapter seed), §6.14 (budget/cost guard).

## Purpose
Make any frontier/open-weight/small model swappable behind one seam, so the system's
identity depends on no single model or vendor. Choose a provider **deterministically** and
enforce a **hard cost guard**.

## Responsibilities
- Route a `ModelRequest` to a provider based ONLY on: request metadata (model, max_tokens),
  declared provider **capabilities**, **budget** constraints, and a platform routing policy
  (lowest estimated cost, ties broken by provider name — deterministic).
- Enforce a **hard cost guard**: charge the chosen cost to the injected `BudgetMeter`
  (interface); refuse (`BudgetGuardError`) when nothing is affordable.
- Keep all provider integrations behind the `ModelProvider` interface.

## Non-responsibilities (NOT here)
- **Vendor-specific logic** and **prompt engineering** — never in the platform; concrete
  providers are domain/external adapters behind `ModelProvider`.
- **Reasoning, planning, memory behavior, runtime orchestration** — separate subsystems.
- **Engineering-domain functionality** / Velith logic.

## Dependencies
- `noetica.interfaces.router` (`ModelRequest`/`ModelResponse`/`ModelRouter`),
  `noetica.interfaces.budget.BudgetMeter` (a concrete meter — e.g. PE-6
  `InMemoryBudgetMeter` — is injected).
- Python standard library only. No vendor SDK, no other layer, no `reference/`.

## Consumers
- Reasoning (PE-18), Runtime (PE-21); Velith; Mini Prometheus.

## Constitution references
§6.15 · Principle 3 · D16.4 · §6.14.

## Future implementation milestones
- **Now (PE-10):** `ModelProvider` seam + deterministic, budget-guarded `DefaultModelRouter`.
- **Later (domain/external):** concrete vendor adapters behind `ModelProvider`; richer
  routing policy by extraction (Law 8). A learned routing policy is gated (PE-G5).
