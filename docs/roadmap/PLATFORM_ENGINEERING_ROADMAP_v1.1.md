# Platform Engineering Roadmap v1.1 — FROZEN

**Supersedes:** `PLATFORM_ENGINEERING_ROADMAP_v1.md` (retained for history, §11.6). The
**only** change is the internal ordering of the Tier-1 milestones (PE-4..PE-9); Tier-2+
(PE-10..PE-21) and the gated set are unchanged.
**Status:** RATIFIED / FROZEN. Changes require a superseding decision (§11.7).
**Authority:** `docs/constitution/HANDBOOK_v1.1.md`.
**Derivation rule / ordering principle:** unchanged from v1 — strictly by true
implementation dependency (hard edges), lowest first; ties broken by *first-consumer
proximity* (Law 8), never by cross-cutting importance.

**Completed:** PE-1 (interfaces), PE-2 (State), PE-3 (Provenance).

---

## Why v1.1 (the review finding)

A dependency review of the Tier-1 set found two defects in v1:

1. **Episode was placed too late (PE-9).** Its only hard platform dependency is
   **Provenance** (PE-3, done) — it needs the embedded `Provenance` value and the
   content-hash utility in `provenance/identity`, plus the `Verdict`/`Episode`
   interfaces. It does **not** depend on `StateSubstrate` (append-only store, separate
   from the substrate — §6.20), nor on `DataContract`, `Observability`, `Budget`,
   `Reference Verifier`, or `Guardrails`.
2. **v1 overstated Episode's dependency on `DataContract`.** `Episode` already carries a
   `schema_version`; the versioning/migration *framework* formalizes evolution but is not
   required to implement the record. That false edge is removed.

Because **Observability and Episode are incomparable in the dependency DAG** (no edge
either way), ordering Observability before Episode was an *importance* choice, not a
dependency one. v1.1 therefore completes the **data spine State → Provenance → Episode**
first, then builds the independent cross-cutting services by first-consumer proximity.

**Change:** Episode `PE-9 → PE-4`. The five independent Tier-1 services shift down one
band and are re-ordered by first consumer: Observability (PE-5), Budget (PE-6),
Data Contract (PE-7), Reference Verifier (PE-8), Guardrails (PE-9). No Tier-2+ change.

---

## Milestone order (v1.1)

| PE | Name | Tier | Hard deps (platform) | First consumer (why here) |
|----|------|------|----------------------|---------------------------|
| 1  | Interface Surface ✅ | 0 | — | all |
| 2  | State Substrate ✅ | 1 | Provenance | all state users |
| 3  | Provenance & Lineage ✅ | 1 | — | State, Episode, Memory |
| **4**  | **Episode & Episode Store** | **2** | **Provenance** | Memory (14), Evaluation (17), Reflection (20) |
| 5  | Observability & Logging | 1 | — | every later mechanism emits; wired into State/Provenance/Episode here |
| 6  | Budget & Meta-control | 1 | — | Router (10), Tool (12), Reasoning (18) |
| 7  | Data Contract & Versioning | 1 | — | Episode/Memory schema evolution; Experience Flow |
| 8  | Reference / Fake Verifier | 1 | — | Evaluation (17); Memory write-filter tests |
| 9  | Guardrails / Safety Engine | 1 | — | Runtime (21) |
| 10 | Model Router | 2 | Budget | Reasoning (18), Runtime (21) |
| 11 | Compute Interface | 2 | Budget | domain adapters, Runtime |
| 12 | Tool Runtime | 2 | Budget | Skill (15), Reasoning (18) |
| 13 | Knowledge Store | 3 | State, Provenance | Context (16) |
| 14 | Memory & Write-Filter | 3 | Episode, Provenance | Context (16), Evaluation (17) |
| 15 | Skill Runtime | 3 | Tool, State | Reasoning (18), Planning (19) |
| 16 | Context Engine | 4 | Memory, Knowledge, State | Reasoning (18) |
| 17 | Evaluation Harness & Held-out Lock | 4 | Memory, Episode, Ref Verifier, State | Velith (arms A0–A4) |
| 18 | Reasoning Runtime | 5 | State, Context, Router, Budget | Planning, Reflection, Runtime |
| 19 | Planning Runtime | 6 | Reasoning, State | Runtime |
| 20 | Reflection | 6 | Reasoning, Episode, State | Runtime |
| 21 | Runtime, Agent Lifecycle & SDK | 7 | PE-2..PE-20 | Velith, Mini Prometheus |

**Gated (unchanged):** PE-G1 World-Model/Twin Engine · PE-G2 Data Lifecycle · PE-G3
Experience Aggregation · PE-G4 Belief/Probabilistic State · PE-G5 Learned Meta-control.

---

## Changed milestones (full detail)

### PE-4 — Episode & Episode Store  *(moved up from PE-9)*
- **Purpose:** the provenance-complete, content-hashed record of one grounded attempt and
  its append-only store — the first-class learning datum; the cohesive continuation of the
  State → Provenance data spine.
- **Constitution:** §7.5; §1.10; §11.7 (identity vs provenance); Law 21 (schema_version).
- **Dependencies (hard):** PE-3 Provenance ONLY (embedded `Provenance` + content-hash
  utility). Not State, not DataContract, not Observability.
- **Consumers:** Memory (PE-14), Evaluation (PE-17), Reflection (PE-20); Velith (produces);
  MiniFlyWire (distilled datasets).
- **Public interfaces implemented:** `EpisodeStore` (+ default `Episode` construction/hash).
- **Verification:** mypy --strict; unit tests; content-hash reproducibility (same identity
  inputs → same hash; volatile fields excluded, §11.7); `schema_version` present (Law 21);
  boundary clean + fail-closed.
- **Out of scope:** domain episode CONTENT; indexed/queryable retrieval (that is Memory);
  the DataContract migration framework (PE-7); observability wiring (retro-wired at PE-5).

### PE-5 — Observability & Logging  *(was PE-4)*
- **Purpose:** structured logging/metrics/traces; the operational-visibility substrate.
- **Constitution:** §6.17; Principle 7; Law 18.
- **Dependencies (hard):** none (interfaces only).
- **Consumers:** every later mechanism; retro-wired into State/Provenance/Episode emission.
- **Public interfaces implemented:** `Observability`.
- **Verification:** mypy --strict; unit tests (event/metric/trace round-trip); boundary.
- **Out of scope:** metrics backends/exporters, dashboards, tracing UIs, domain logic.
- **Note:** placed *after* Episode because it is not a prerequisite of Episode; it is
  cross-cutting and wired into the earlier data-spine mechanisms when it lands (the same
  retro-wiring State and Provenance already require).

### PE-6 — Budget & Meta-control  *(was PE-7)*
- **Purpose/Constitution/Interfaces:** unchanged from v1 (§6.14; `BudgetMeter`).
- **Dependencies (hard):** none. **First consumer:** Model Router (PE-10).
- **Out of scope:** learned meta-control (gated PE-G5); domain cost models.

### PE-7 — Data Contract & Versioning  *(was PE-5)*
- **Purpose/Constitution/Interfaces:** unchanged from v1 (§4.3, Law 21; `DataContract`).
- **Dependencies (hard):** none. **First consumer:** Episode/Memory schema evolution and
  the Experience Flow. (Episode ships before this, carrying only a `schema_version`; the
  framework lands before Memory formalizes experience contracts.)
- **Out of scope:** concrete domain schemas; storage.

### PE-8 — Reference / Fake Verifier  *(was PE-6)*
- **Purpose/Constitution/Interfaces:** unchanged from v1 (§6.11, Law 20; reference `Verifier`).
- **Dependencies (hard):** none. **First consumer:** Evaluation Harness (PE-17); Memory
  write-filter tests.
- **Out of scope:** any real domain oracle (DOMAIN-owned).

### PE-9 — Guardrails / Safety Policy Engine  *(was PE-8)*
- **Purpose/Constitution/Interfaces:** unchanged from v1 (§6.16, Law 17; `Guardrail`).
- **Dependencies (hard):** none. **First consumer:** Runtime (PE-21).
- **Out of scope:** domain safety POLICY (content); action-boundary wiring (PE-21).

*(PE-10..PE-21 and PE-G1..G5 are unchanged from v1 — see that document for full
per-milestone detail; their numbers and dependencies are identical.)*

---

## Dependency graph (v1.1)

```
PE-1 interfaces
  ├─ PE-3 Provenance ──► PE-4 Episode ──► PE-14 Memory ──► PE-16 Context ─┐
  │        └─► PE-2 State ─────────────────────────────────┬─────────────┤
  ├─ PE-5 Observability (cross-cutting; consumed by 10..21)  │             │
  ├─ PE-6 Budget ──► PE-10 Router ──────────────────────────┼──► PE-18 Reasoning ─► PE-19 Planning
  ├─ PE-7 DataContract ──► (Episode schema evol., Memory)    │             │       └─► PE-20 Reflection
  ├─ PE-8 RefVerifier ──────────────► PE-17 Evaluation ◄─────┘             │
  └─ PE-9 Guardrails ───────────────────────────────────────────────────► PE-21 Runtime/SDK
  PE-6 ─► PE-11 Compute ;  PE-6 ─► PE-12 Tool ─► PE-15 Skill
  PE-2,PE-3 ─► PE-13 Knowledge ─► PE-16 Context
```

Adjacency (hard prerequisites):

| PE | deps | PE | deps |
|----|------|----|------|
| 4  | 3 | 13 | 2,3 |
| 5  | — | 14 | 4,3 |
| 6  | — | 15 | 12,2 |
| 7  | — | 16 | 14,13,2 |
| 8  | — | 17 | 14,4,8,2 |
| 9  | — | 18 | 2,16,10,6 |
| 10 | 6 | 19 | 18,2 |
| 11 | 6 | 20 | 18,4,2 |
| 12 | 6 | 21 | 2..20 |

## No circular dependencies (proof)

Every milestone's hard prerequisites carry a strictly lower PE number (verify each row:
4→{3}; 14→{4,3}; 17→{14,4,8,2}; 18→{2,16,10,6}; 21→{2..20}; …). A directed graph whose
every edge points from a higher to a lower number cannot contain a cycle. Hence the v1.1
order is a valid topological sort of the dependency DAG; the graph is acyclic (Law 9).

## Why v1.1 is more correct than v1

- **Removes an importance-based inversion.** Observability↔Episode have no dependency
  edge; v1 ordered them by cross-cutting importance. v1.1 orders by the real edge that
  exists — Provenance → Episode — completing the data spine first.
- **Corrects a false dependency.** Episode does not hard-depend on DataContract; v1.1
  drops that edge, so Episode's true prerequisites (Provenance only) are honored.
- **Consumer-proximity for independent services (Law 8).** The five depth-1 services are
  now ordered by their first real consumer, not by intuition — Budget before Router,
  Reference Verifier before Evaluation, Guardrails before Runtime.
- **No regression:** Tier-2+ numbering, dependencies, acyclicity, and the gated set are
  unchanged; PE-4 remains dependency-ready today (needs only Provenance, done).

## Freeze

This is **Platform Engineering Roadmap v1.1**, FROZEN, superseding v1. **PE-4 is now
Episode & Episode Store.** Any change requires a superseding decision (§11.7).
