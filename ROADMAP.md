# Noetica Roadmap v1

**Derivation rule.** Every item traces to (1) the Constitution, (2) a repository gap, or
(3) an existing seed. No invented features. Mechanisms grow **by extraction**, each gated
on a real consumer (Law 8, §11.4, §13.6). Governing authority: `docs/constitution/`.

## Phase 0 — Repository Transformation  ✅ COMPLETE (M0–M6)

Transformed the repository into the canonical Noetica platform: reversibility anchor
(M0); canonical `src/noetica/` skeleton mapped 1:1 to Part VI (M1); Constitution +
Noetica docs consolidated (M2); MiniFlyWire corpus → `reference/miniflywire/` (M3);
MiniNoetica legacy code → `reference/mininoetica/` + CI boundary enforcement (M3.5);
Velith docs → `reference/velith/` (M5); README/ROADMAP/ledger/registry + cleanup (M6).
Full record: `docs/transformation/DOCUMENT_CLASSIFICATION.md`.

## Phase 1 — Platform Engineering (post-transformation)

> Interfaces are designed early; depth is added on a schedule; only the interfaces the
> current consumer exercises are built (§13.6). Noetica publishes interfaces; the
> **Velith** repository (Layer 3) is the first consumer and the extraction source (N.3).

- **PE-1 — Interface surface.** Typed `Protocol`/dataclass contracts in
  `src/noetica/interfaces/` (Verifier + Verdict, MemoryStore, Plan, Tool, Skill,
  ModelRouter, BudgetMeter, Provenance, State). Signatures only, no implementations
  (Law 8). Verified by `mypy --strict` + the architecture tests.
- **PE-2 — State Substrate + Provenance + Episode Store.** Extract behind interfaces
  once the Velith consumer exercises them (§6.1, §6.2, §7.5). Versioned episode data
  contract (Law 21).
- **PE-3 — Verification Protocol + reference/fake verifier + Model Router.** Noetica
  owns the `Verifier` protocol and `Verdict` (distribution-capable, Law 16); the SWE
  oracle stays in Velith (Law 15). Noetica self-tests use a fake verifier (Law 20).
  Model routing + hard cost guard (§6.15, D16.4 seed).
- **PE-4 — Memory write-filter + Evaluation harness + held-out lock.** Enables the
  compounding experiment (§1.7, D6–D8): A0/A1/A2 arms, mechanical held-out lock,
  A1≡A2-retriever integrity test (§11.10).

## Gated / postponed (do NOT build before their gate — Appendix D, Law 8)

Belief/probabilistic substrate (gated on the first approximate rung), experience
aggregation (gated on a credible second consumer), learned meta-control (gated on the
compounding result), context/knowledge-graph engines, guardrails engine, compute
interface, data-lifecycle framework. Each is recorded as postponed; building any before
its gate is a §11.8 deviation requiring a recorded justification.

## Invariants across the roadmap

Strict acyclic dependency DAG (Law 9); mechanism vs content (Law 3); no homunculus;
provenance/observability from the first commit (Principle 7); every milestone yields a
running system (§13.6); each milestone hardens the last, never a rewrite.

---

## Platform Engineering Roadmap v1 (FROZEN)

The Phase-1 sketch above is superseded by the complete, dependency-ordered, frozen
roadmap: **`docs/roadmap/PLATFORM_ENGINEERING_ROADMAP_v1.md`** (PE-1..PE-21 + gated
PE-G1..G5, with dependency graph, acyclicity proof, and ordering justification).

Done: **PE-1** interfaces, **PE-2** State Substrate, **PE-3** Provenance & Lineage.
Next by dependency depth: **PE-4** Observability. The order is frozen; changes require a
superseding decision (§11.7).
