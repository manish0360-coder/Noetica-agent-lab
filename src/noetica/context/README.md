# src/noetica/context — Context Engine

**Constitution:** §6.6 (context assembly + window budgeting), §6.20 (Context is a momentary
assembly, distinct from Memory/Knowledge), Law 13.

## Purpose
Assemble a **bounded working context for a single inference** by combining State, Memory,
and Knowledge according to an **explicit policy** and a **token budget**. Context is scarce;
this decides what fits — without any smart retrieval.

## Responsibilities
- `assemble(goal, token_budget)` → a `Context` of `ContextItem`s.
- Combine sources per an explicit `ContextPolicy`: exact `state_keys`, `memory_k` most-recent
  episodes (via Memory's fixed retriever), an explicit `knowledge_query`.
- Enforce the budget by **prefix truncation in fixed source order** (no reordering).

## Non-responsibilities (NOT here)
- **Reasoning, planning, reflection, retrieval optimization, ranking heuristics, autonomous
  behavior, prompt construction, domain logic** — none.
- **Persistence** — Context is temporary; the engine owns no State/Memory/Knowledge (they
  are injected references it reads but does not own).

## Dependencies
- `noetica.interfaces.{context,state,memory,knowledge}` (concrete State/Memory/Knowledge —
  PE-2/PE-14/PE-13 — are injected).
- Python standard library only. No other layer, no `reference/`.

## Consumers
- Reasoning (PE-18), Runtime (PE-21).

## Constitution references
§6.6 · §6.20 · Law 13.

## Future implementation milestones
- **Now (PE-16):** `ContextEngine` — explicit-policy assembly + budget truncation.
- **Later:** richer, still-explicit policies by extraction (Law 8). Causal-relevance
  retrieval (a MiniFlyWire finding) is promoted by re-implementation (Law 7), never as an
  ad-hoc heuristic here.
