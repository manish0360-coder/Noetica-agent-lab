# Platform Engineering Roadmap v1 — FROZEN

**Status:** RATIFIED / FROZEN. The implementation order below is fixed; it changes only
by a recorded decision (§11.7) that supersedes this document.
**Authority:** `docs/constitution/HANDBOOK_v1.1.md`. This roadmap conforms to it and
does not redesign it.
**Derivation rule:** every milestone and its order come strictly from (1) the Constitution
(Part VI subsystems, §9.2 matrix) and (2) the existing dependency graph implied by the
frozen PE-1 interface surface. No invented mechanisms; no feature-popularity ordering.
**Ordering principle:** lowest dependency depth first (longest path from the interface
layer). A mechanism is implemented only after every mechanism it consumes already exists
and is verified — no stubs for missing lower layers (Law 8, Principle 4, §13.6).

**Completed:** PE-1 (interfaces), PE-2 (State Substrate), PE-3 (Provenance & Lineage).

---

## Dependency tiers (depth from the interface layer)

- **Tier 0 — contracts:** PE-1 interface surface.
- **Tier 1 — foundational (deps = interfaces only):** Provenance (PE-3), Observability
  (PE-4), Data Contract (PE-5), Reference Verifier (PE-6), Budget (PE-7), Guardrails (PE-8).
  State (PE-2) is Tier 1→2 (uses Provenance).
- **Tier 2:** Episode (PE-9), Model Router (PE-10), Compute (PE-11), Tool (PE-12).
- **Tier 3:** Knowledge (PE-13), Memory (PE-14), Skill (PE-15).
- **Tier 4:** Context (PE-16), Evaluation Harness (PE-17).
- **Tier 5:** Reasoning (PE-18).
- **Tier 6:** Planning (PE-19), Reflection (PE-20).
- **Tier 7 — integrator:** Runtime / Agent Lifecycle / SDK (PE-21).
- **Gated (Law 8 / Appendix D):** PE-G1..PE-G5.

---

## Milestones

### PE-1 — Interface Surface  ✅ DONE
Typed public contracts for all Part VI subsystems. Deps: none. Consumers: all.
Implements: the interface catalog. Out of scope: any implementation.

### PE-2 — State Substrate  ✅ DONE
Persistent, typed, provenance-tracked shared state (the core). Deps: PE-1, PE-3.
Implements: `StateSubstrate`. §6.1.

### PE-3 — Provenance & Lineage  ✅ DONE
Derivation record + lineage ledger + content-hash identity. Deps: PE-1.
Implements: `Provenance`/`Provenanced` (+ ledger). §6.2.

---

### PE-4 — Observability & Logging
- **Purpose:** structured logging, metrics, traces so every later mechanism is auditable
  from its first commit; the substrate on which provenance and evaluation are trusted.
- **Constitution:** §6.17; Principle 7; Law 18.
- **Dependencies:** PE-1 (interfaces). (Tier 1.)
- **Consumers:** every subsequent PE milestone; Velith; Mini Prometheus (emit).
- **Public interfaces implemented:** `Observability`.
- **Verification:** mypy --strict; unit tests; boundary clean + fail-closed; structured
  event/metric/trace round-trip; no other subsystem implemented.
- **Out of scope:** metrics backends/exporters (vendor adapters), dashboards, tracing UIs,
  any domain logic.

### PE-5 — Data Contract & Versioning
- **Purpose:** the versioning + migration framework every experience schema (episode,
  dataset, derived-question) must satisfy; makes the Experience Flow contract-governed.
- **Constitution:** §4.3; Law 21; §11.7; §11.10 (data-contract check).
- **Dependencies:** PE-1. (Tier 1.)
- **Consumers:** Episode (PE-9), Memory (PE-14), Data Lifecycle (PE-G2); Velith; Mini Prometheus.
- **Public interfaces implemented:** `DataContract` (+ version registry/migration helpers).
- **Verification:** mypy --strict; unit tests (version bump requires migration; unversioned
  change rejected); boundary clean; the §11.10 data-contract check runs green.
- **Out of scope:** concrete domain schemas; storage; the episode schema itself (PE-9).

### PE-6 — Reference / Fake Verifier
- **Purpose:** a deterministic reference/fake verifier so Noetica can self-test the
  verification protocol and (later) the eval harness WITHOUT any domain oracle (Law 20).
- **Constitution:** §6.11; Law 15/16; Law 20.
- **Dependencies:** PE-1 (`Verifier`, `Verdict`). (Tier 1.)
- **Consumers:** Evaluation Harness (PE-17); platform self-tests; Memory write-filter tests.
- **Public interfaces implemented:** `Verifier` (reference impl returning `Verdict`).
- **Verification:** mypy --strict; unit tests; deterministic verdicts; a boundary/self-test
  proving Noetica never imports a real domain oracle (Law 20).
- **Out of scope:** any real oracle (SWE/FEA/SPICE/mfg) — those are DOMAIN-owned (Velith,
  Mini Prometheus), never here.

### PE-7 — Budget & Meta-control
- **Purpose:** meter and cap the cost of computation (how much to think, when to stop) —
  bounded rationality as a first-class mechanism.
- **Constitution:** §6.14; Principle 5.
- **Dependencies:** PE-1 (+ soft PE-4). (Tier 1.)
- **Consumers:** Model Router (PE-10), Compute (PE-11), Tool (PE-12), Reasoning (PE-18),
  Runtime (PE-21).
- **Public interfaces implemented:** `BudgetMeter`.
- **Verification:** mypy --strict; unit tests (spend/remaining/exceeded; hard cap); boundary.
- **Out of scope:** a LEARNED meta-control policy (gated PE-G5); domain cost models.

### PE-8 — Guardrails / Safety Policy Engine
- **Purpose:** the engine that enforces policy, including the immutable human-oversight
  boundary the system may never modify.
- **Constitution:** §6.16; Principle 6 / Law 17.
- **Dependencies:** PE-1 (+ soft PE-4). (Tier 1.)
- **Consumers:** Runtime (PE-21); Velith/Mini Prometheus supply domain policy content.
- **Public interfaces implemented:** `Guardrail` (+ `Decision`).
- **Verification:** mypy --strict; unit tests; a test proving no self-modification path can
  alter the oversight boundary (Law 17); boundary clean.
- **Out of scope:** domain-specific safety POLICY (content, domain-owned); enforcement at
  the action boundary (wired at PE-21).

### PE-9 — Episode & Episode Store
- **Purpose:** the provenance-complete, content-hashed record of one grounded attempt and
  its append-only store — the first-class learning datum.
- **Constitution:** §7.5; §1.10; §11.7 (identity vs provenance); Law 21.
- **Dependencies:** PE-3 (Provenance/content-hash), PE-5 (Data Contract). (Tier 2.)
- **Consumers:** Memory (PE-14), Evaluation (PE-17), Reflection (PE-20); Velith (produces);
  MiniFlyWire (distilled datasets).
- **Public interfaces implemented:** `EpisodeStore` (+ default `Episode` construction/hash).
- **Verification:** mypy --strict; unit tests; content-hash reproducibility (same identity
  inputs → same hash; volatile fields excluded); versioned schema (Law 21); boundary.
- **Out of scope:** domain episode CONTENT; indexed/queryable store beyond append-only
  (added by extraction when a consumer needs it); retrieval (that is Memory).

### PE-10 — Model Router
- **Purpose:** make any model provider swappable behind one seam, with a hard cost guard —
  the system's identity depends on no single model or vendor.
- **Constitution:** §6.15; Principle 3; D16.4.
- **Dependencies:** PE-7 (Budget cost guard); soft PE-4. (Tier 2.)
- **Consumers:** Reasoning (PE-18); Runtime (PE-21); Velith; Mini Prometheus.
- **Public interfaces implemented:** `ModelRouter` (+ `ModelRequest`/`ModelResponse`).
- **Verification:** mypy --strict; unit tests (provider swap; cost-guard trip); boundary.
- **Out of scope:** concrete vendor clients (wrapped adapters added when needed); routing
  POLICY learning; prompt content.

### PE-11 — Compute Interface
- **Purpose:** vendor-neutral request / placement / cap of compute work; infrastructure
  stays external to the four layers.
- **Constitution:** §6.21 (Amendment 3).
- **Dependencies:** PE-7 (Budget). (Tier 2.)
- **Consumers:** Velith / Mini Prometheus implement concrete adapters; Runtime.
- **Public interfaces implemented:** `ComputeInterface`.
- **Verification:** mypy --strict; unit tests; boundary; a check that no cloud/K8s/GPU
  vendor logic enters the platform (§6.21).
- **Out of scope:** concrete infra adapters (DOMAIN-owned); the running of containers/pods
  (external infrastructure).

### PE-12 — Tool Runtime
- **Purpose:** register, invoke, and sandbox tools; async/non-blocking so the loop never
  blocks on a long-running solve. "Wrap, don't rebuild."
- **Constitution:** §6.12; Principle 9.
- **Dependencies:** PE-7 (Budget); soft PE-4. (Tier 2.)
- **Consumers:** Skill (PE-15); Reasoning (PE-18); Velith/Mini Prometheus implement tools.
- **Public interfaces implemented:** Tool runtime around `Tool`/`ToolResult`.
- **Verification:** mypy --strict; unit tests (register/invoke/sandbox; async non-block);
  boundary.
- **Out of scope:** concrete tools (CAD/solver/MES/robot — DOMAIN-owned); external kernels.

### PE-13 — Knowledge Store
- **Purpose:** the typed, provenance-tracked semantic/graph store ENGINE (schema-agnostic);
  domains populate it with content.
- **Constitution:** §6.5; §6.20; Law 3.
- **Dependencies:** PE-2 (State), PE-3 (Provenance). (Tier 3.)
- **Consumers:** Context (PE-16); Velith (engineering ontology); Mini Prometheus (mfg concepts).
- **Public interfaces implemented:** `KnowledgeStore`.
- **Verification:** mypy --strict; unit tests (upsert/get/query; provenance retained);
  distinctness from Memory/Context (§6.20); boundary.
- **Out of scope:** domain ontology CONTENT; a specific graph DB backend (extraction-gated).

### PE-14 — Memory Framework & Write-Filter
- **Purpose:** episodic/experience persistence and the write-filter policy — the SINGLE
  manipulated variable of the compounding experiment (verified-only vs unfiltered).
- **Constitution:** §6.4; §6.20; D7 (A0–A4); Law 13.
- **Dependencies:** PE-9 (Episode), PE-3 (Provenance). (Tier 3.)
- **Consumers:** Context (PE-16), Evaluation (PE-17); Velith; Mini Prometheus.
- **Public interfaces implemented:** `MemoryStore`, `WriteFilter`.
- **Verification:** mypy --strict; unit tests; the experiment-integrity invariant that A1
  (unfiltered) and A2 (verified) share an identical retriever/embedder/top-k — only the
  write-filter differs (D7; §11.10 permanent test); boundary.
- **Out of scope:** retrieval-ranking research; forgetting/retention algorithm content
  (promoted from MiniFlyWire by re-implementation, Law 7); domain memory content.

### PE-15 — Skill Runtime
- **Purpose:** composable, learned units of competence — how verified experience
  crystallizes into reusable competence.
- **Constitution:** §6.13; Law 3.
- **Dependencies:** PE-12 (Tool), PE-2 (State). (Tier 3.)
- **Consumers:** Reasoning (PE-18), Planning (PE-19); Velith/Mini Prometheus implement skills.
- **Public interfaces implemented:** Skill runtime around `Skill`.
- **Verification:** mypy --strict; unit tests (compose/apply); boundary.
- **Out of scope:** concrete engineering/mfg skills (DOMAIN-owned).

### PE-16 — Context Engine
- **Purpose:** working-set assembly + window budgeting for a SINGLE inference — select the
  causally-relevant subset from memory and knowledge.
- **Constitution:** §6.6; §6.20.
- **Dependencies:** PE-14 (Memory), PE-13 (Knowledge), PE-2 (State). (Tier 4.)
- **Consumers:** Reasoning (PE-18); Runtime (PE-21).
- **Public interfaces implemented:** `ContextAssembler` (+ `Context`).
- **Verification:** mypy --strict; unit tests (assembly under token budget; relevance not
  mere similarity); distinctness from Memory/Knowledge (§6.20); boundary.
- **Out of scope:** domain relevance heuristics; embedding models (wrapped when needed).

### PE-17 — Evaluation Harness & Held-out Lock
- **Purpose:** the experiment machinery — arms, mechanically-enforced held-out lock,
  frozen evaluation, metrics — owned once and reused by every vertical/rung.
- **Constitution:** §6.10; §5.6; D8; §11.10; Law 20.
- **Dependencies:** PE-14 (Memory), PE-9 (Episode), PE-6 (Reference Verifier), PE-2 (State). (Tier 4.)
- **Consumers:** Velith (configures arms A0–A4); Mini Prometheus.
- **Public interfaces implemented:** `EvalHarness` (+ `EvalResult`).
- **Verification:** mypy --strict; unit tests; held-out lock provable in code (held-out data
  can never enter any arm's memory); effect-size + seed-spread reporting; self-tests use the
  reference verifier only (Law 20); boundary.
- **Out of scope:** the domain benchmark/dataset CONTENT; running the full compounding
  experiment (that needs the agent, PE-21, and Velith).

### PE-18 — Reasoning Runtime
- **Purpose:** the FORM of reasoning — iterate inference, apply verification seams,
  backtrack — never a mind, never domain reasoning content.
- **Constitution:** §6.7; Law 3/5 (no homunculus).
- **Dependencies:** PE-2 (State), PE-16 (Context), PE-10 (Router), PE-7 (Budget). (Tier 5.)
- **Consumers:** Planning (PE-19), Reflection (PE-20), Runtime (PE-21).
- **Public interfaces implemented:** `ReasoningLoop`.
- **Verification:** mypy --strict; unit tests (step/run; verification seam; backtrack);
  a test that NO domain reasoning content is present (form only); boundary.
- **Out of scope:** domain reasoning CONTENT (Velith/Mini Prometheus); a "Reasoner" that
  understands the world (forbidden homunculus).

### PE-19 — Planning Runtime
- **Purpose:** plan representation + executor (form), with a reflection seam; domains
  express their plans AS Noetica plans.
- **Constitution:** §6.8; Law 3.
- **Dependencies:** PE-18 (Reasoning), PE-2 (State). (Tier 6.)
- **Consumers:** Runtime (PE-21); Velith/Mini Prometheus (plan content).
- **Public interfaces implemented:** `Planner`, `Executor` (+ `Plan`/`Step`).
- **Verification:** mypy --strict; unit tests (represent/sequence/execute; reflection seam);
  form-only test; boundary.
- **Out of scope:** engineering/mfg plan CONTENT (DOMAIN-owned).

### PE-20 — Reflection
- **Purpose:** the self-critique loop that turns a failed episode into a revised approach —
  a re-implementation of MiniFlyWire's validated reflection primitive (Law 7).
- **Constitution:** §6.9; §4.1 (promotion by re-implementation).
- **Dependencies:** PE-18 (Reasoning), PE-9 (Episode), PE-2 (State). (Tier 6.)
- **Consumers:** Runtime (PE-21); Velith; Mini Prometheus.
- **Public interfaces implemented:** `Reflector`.
- **Verification:** mypy --strict; unit tests (attempt+outcome → revision); a Primitive
  Registry entry (§11.5) if promoted from a validated MiniFlyWire spec; boundary.
- **Out of scope:** importing MiniFlyWire code (re-implementation only, Law 4/7); domain
  critique content.

### PE-21 — Runtime, Agent Lifecycle & SDK
- **Purpose:** the integrator — set up an episode, drive condition-driven activation, tear
  down cleanly; the stable public SDK surface domains build on. Owns operation order, not
  the thinking (no homunculus).
- **Constitution:** §6.3; §6.18; Law 3; Law 17 (guardrail wiring).
- **Dependencies:** ALL of PE-2..PE-20. (Tier 7, top.)
- **Consumers:** Velith; Mini Prometheus (build agents via the SDK).
- **Public interfaces implemented:** `Runtime`, `Agent` (developer surface / plugin mount).
- **Verification:** mypy --strict; unit tests; an end-to-end platform run over the reference
  verifier producing a provenance-complete episode (Law 20); guardrail + budget enforced in
  the loop; boundary; a fresh-clone green run (§13.4).
- **Out of scope:** domain agents/content; a real domain verifier in the loop; premature
  scale infrastructure.

---

## Gated / Postponed milestones (Law 8 / §11.8 / Appendix D)

Recorded so the ecosystem knows what it has NOT yet decided; each is gated on a specific
result and must not be built before its gate.

- **PE-G1 — World-Model / Twin Engine** (§8.4): state-sync/versioning/provenance engine.
  Deps: State, Provenance. **Gate:** a real Mini Prometheus (or Velith world-model) consumer.
- **PE-G2 — Data Lifecycle Governance** (§11.11): compression/summarization/archival/
  pruning/retention/bounded-storage. Deps: Episode, Memory, Data Contract. **Gate:** an
  experience store approaching its declared bound.
- **PE-G3 — Experience Aggregation** (§4.3): first-class home for the upward loop. **Gate:**
  a credible second consumer (extraction discipline, Law 8).
- **PE-G4 — Belief / Probabilistic State** (§6.1 evolution, §8.3): confidence + epistemic/
  aleatoric separation. **Gate:** reaching the first approximate (PCB/FEA) rung.
- **PE-G5 — Learned Meta-control** (§6.14 evolution): budget policy moves from hand-tuned to
  learned. **Gate:** the compounding result (§1.7).

---

## Dependency graph

Arrows point from a milestone to each mechanism it depends on (code-import direction).
Only platform mechanisms shown; every milestone also depends on PE-1 interfaces.

```
PE-1 interfaces
  ├─ PE-3 Provenance ──────────────┐
  │     └─ PE-2 State ──────┐       │
  ├─ PE-4 Observability     │       │
  ├─ PE-5 DataContract ─────┼───┐   │
  ├─ PE-6 RefVerifier       │   │   │
  ├─ PE-7 Budget ──┬────────┼─┐ │   │
  └─ PE-8 Guardrails│        │ │ │   │
                    │        │ │ │   │
PE-9  Episode      ←─────────┘ │ │ ← PE-3, PE-5
PE-10 Router       ← PE-7      │ │
PE-11 Compute      ← PE-7      │ │
PE-12 Tool         ← PE-7      │ │
PE-13 Knowledge    ← PE-2, PE-3
PE-14 Memory       ← PE-9, PE-3
PE-15 Skill        ← PE-12, PE-2
PE-16 Context      ← PE-14, PE-13, PE-2
PE-17 Evaluation   ← PE-14, PE-9, PE-6, PE-2
PE-18 Reasoning    ← PE-2, PE-16, PE-10, PE-7
PE-19 Planning     ← PE-18, PE-2
PE-20 Reflection   ← PE-18, PE-9, PE-2
PE-21 Runtime/SDK  ← PE-2..PE-20 (integrator)
```

Adjacency (hard prerequisites), used for the acyclicity proof:

| PE | depends on (hard) |
|----|-------------------|
| 4  | — |
| 5  | — |
| 6  | — |
| 7  | — |
| 8  | — |
| 9  | 3, 5 |
| 10 | 7 |
| 11 | 7 |
| 12 | 7 |
| 13 | 2, 3 |
| 14 | 9, 3 |
| 15 | 12, 2 |
| 16 | 14, 13, 2 |
| 17 | 14, 9, 6, 2 |
| 18 | 2, 16, 10, 7 |
| 19 | 18, 2 |
| 20 | 18, 9, 2 |
| 21 | 2..20 |

## No circular dependencies (proof)

For every milestone, all hard prerequisites carry a STRICTLY LOWER PE number (verify each
row above: 9→{3,5}; 14→{9,3}; 16→{14,13,2}; 18→{2,16,10,7}; 21→{2..20}; etc.). A directed
graph in which every edge points from a higher number to a lower number **cannot contain a
cycle** (a cycle would require an edge from a lower to a higher number). Therefore the PE
ordering is a valid topological sort of the dependency DAG, and the graph is acyclic. This
also mirrors the ecosystem's own Code-Flow invariant: a strict acyclic dependency DAG (Law 9).

## Why this ordering beats the alternatives

1. **vs. feature-popularity / top-down (build Memory or Runtime first):** every high-tier
   mechanism (Runtime, Reasoning, Memory) depends on lower mechanisms that would not yet
   exist, forcing mocks/stubs that are guessed wrong and reworked when the real foundation
   lands. Dependency-depth ordering means each milestone stands on *verified* code, never a
   stub — directly honoring Law 8 (grow by extraction, not speculation) and Principle 4.
2. **vs. breadth-first / all-cross-cutting-first:** we DO front-load the genuinely
   foundational cross-cutting services (Observability PE-4, Data Contract PE-5, Reference
   Verifier PE-6, Budget PE-7, Guardrails PE-8) because they are Tier-1 and needed by nearly
   everything — so every later mechanism ships with provenance + observability from its first
   commit (Principle 7) and is self-testable with the fake verifier (Law 20). But we do NOT
   build Context/Reasoning before Memory/Episode, which breadth-first would wrongly allow.
3. **vs. experiment-first (build the Eval Harness immediately to chase §1.7):** the harness
   (PE-17) hard-depends on Memory + Episode + Reference Verifier + State; building it earlier
   means stubbing exactly the mechanisms whose real behavior the experiment must measure —
   which would make a null result uninterpretable (the very failure D6/D8 guard against).
   This ordering reaches the harness as early as its dependencies allow, and the full run
   only after the integrating Runtime (PE-21) exists.
4. **Blast-radius & reviewability:** a strict DAG with one owner per capability makes each
   milestone's change radius knowable and keeps "who/what depends on this?" always
   answerable for a decade (Law 2, Law 9, §9.3).

---

## Freeze

This is **Platform Engineering Roadmap v1**, FROZEN. The milestone set and order are fixed.
Any change requires a recorded, superseding decision in `docs/decisions/DECISIONS.md`
(§11.7). Gated milestones (PE-G1..G5) are built only when their stated gate is met (§11.8).
