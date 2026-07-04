# PROJECT STATE — Noetica

**Project:** Noetica (Layer 2 — Agent Intelligence Platform).
**Authority:** Handbook v1.1 (frozen). **Living status record;** updated at milestone/phase boundaries.
**Current phase:** Platform Engineering — **COMPLETE & FROZEN**.
**HEAD:** `e34975c` · **Freeze tag:** `platform-engineering-v1`.
**Workflow:** Manufacturing Pipeline (Research → Architecture → Manufacturing → QA → Freeze → Gate Review).

---

## 1. What Noetica is
The domain-agnostic platform of the MiniFlyWire → Noetica → Velith → Mini Prometheus ecosystem.
Owns reusable **mechanisms**, typed **interfaces**, and the shared **state substrate**. Owns no
engineering/manufacturing content, no domain oracle, no homunculus (§6 prime directive).

## 2. Journey (what was actually done, in order)

### 2.1 Audit (Research/analysis)
Full evidence-based audit of the original `Noetica-agent-lab` repo. Finding: the repo physically
held **MiniNoetica** (education/fractions tutor) + a **MiniFlyWire** science corpus + tangled
**Velith** docs; **Noetica the platform did not exist in code**. Recorded in
`docs/audits/NOETICA_ARCHITECTURAL_AUDIT_v1.md`. (Velith's `src/` later confirmed to live in a
**separate repo** — the earlier "missing code" finding was retracted.)

### 2.2 Repository Transformation (M0 … M6, + M3.5)
Transformed the tangled repo into the canonical Noetica platform, atomically & history-preserving:
- **M0** reversibility anchor (branch `transform/noetica-canonical`, tag `pre-noetica-transform`).
- **M1** canonical `src/noetica/` skeleton (21 subsystem packages ↔ Part VI) + tests/docs/tools/reference dirs.
- **M2** imported the Constitution; relocated Noetica-owned docs.
- **M3** MiniFlyWire research corpus → `reference/miniflywire/` (ownership retained).
- **M3.5** archived MiniNoetica code → `reference/mininoetica/`; added **CI boundary enforcement** (fail-closed).
- **M5** Velith docs → `reference/velith/`.
- **M6** canonical README/ROADMAP + decision ledger + Primitive Registry; pruned stubs.
- Recorded in `docs/transformation/` (DOCUMENT_CLASSIFICATION + plans v1/v2). Frozen: `repo-transformation-complete`.

### 2.3 Platform Engineering (PE-1 … PE-21) — the platform itself
Built default implementations of every Part VI mechanism, strictly by dependency depth
(Roadmap v1.1). Interface surface frozen at PE-1.

| PE | Subsystem | § |
|----|-----------|---|
| 1 | interfaces (typed contract surface, 21 modules) | Part VI |
| 2 | state (State Substrate) | §6.1 |
| 3 | provenance (Provenance & Lineage) | §6.2 |
| 4 | episodes (Episode & Episode Store) | §7.5 |
| 5 | observability (Logging/metrics/traces) | §6.17 |
| 6 | budget (Budget & Meta-control, hard cost guard) | §6.14 |
| 7 | datacontracts (Data Contract & Versioning) | §4.3/Law 21 |
| 8 | verification (ReferenceVerifier — fake, Law 20) | §6.11 |
| 9 | guardrails (Safety engine, immutable oversight) | §6.16/Law 17 |
| 10 | router (Model Router, deterministic + cost guard) | §6.15 |
| 11 | compute (Compute Interface, vendor-neutral) | §6.21 |
| 12 | tools (Tool Runtime, sandbox + async) | §6.12 |
| 13 | knowledge (Knowledge Store engine) | §6.5 |
| 14 | memory (Memory + Write-Filter, A1/A2/A4) | §6.4/D7 |
| 15 | skills (Skill Runtime) | §6.13 |
| 16 | context (Context Engine, explicit policy) | §6.6 |
| 17 | evaluation (Harness + Held-out Lock, frozen eval) | §6.10 |
| 18 | reasoning (Reasoning Runtime, form only) | §6.7 |
| 19 | planning (Planning Runtime, form only) | §6.8 |
| 20 | reflection (Grounded self-critique) | §6.9 |
| 21 | runtime + sdk (Runtime, Agent Lifecycle & SDK — integrator) | §6.3/§6.18 |

### 2.4 Governance & hardening
- Decisions **DN-1 … DN-8** (`docs/decisions/DECISIONS.md`): Constitution adoption; transformation;
  Amendment A1 (cross-layer ownership); CI enforcement; Roadmap v1 (DN-5) → v1.1 (DN-6, Episode
  reordering); **DN-7** reasoning ownership/injection/blackboard; **DN-8** intra-platform DAG.
- **FIX-1** mechanical intra-Noetica DAG enforcement (fail-closed; prevents reasoning→planning/reflection cycles, Law 9).
- Independent architecture reviews (Gemini/Board) evaluated; only constitutionally-required fixes applied.
- **PE-21 Design Specification** frozen (`docs/specs/PE-21_DESIGN_SPEC.md`) with impossibility proofs.

### 2.5 Freeze
Final report + release notes produced; tagged `platform-engineering-v1`.

## 3. Current status (frozen)
- **Certified:** `mypy --strict` clean (89 files); **181 tests**; **15 architecture tests**;
  boundary + intra-platform DAG clean. 53 commits; `main` pristine.
- **Implemented subsystems:** all 21 (state…runtime/sdk) + 21 interface modules.
- **Enforced constitutionally:** strict acyclic DAG (Law 9/FIX-1); no reference/legacy/domain
  imports (Law 4/5, D11); mechanism-vs-content (Law 3); verifier oracle is domain / self-tests
  use ReferenceVerifier (Law 15/20); immutable oversight (Law 17); versioned data contracts (Law 21);
  experiment integrity A1≡A2 retriever (D7); reasoning ownership/no-homunculus (DN-7).

## 4. Deferred (gated — NOT built, Law 8/§11.8)
- **PE-G1** World-Model / Twin Engine — gate: a real world-model/twin consumer.
- **PE-G2** Data Lifecycle Governance — gate: a store approaching its bound.
- **PE-G3** Experience Aggregation — gate: a credible second consumer.
- **PE-G4** Belief / Probabilistic State — gate: first approximate (PCB/FEA) rung.
- **PE-G5** Learned Meta-control — gate: the compounding result.
**Gate Review status:** PE-G1 gate NOT satisfied → stopped; no gated work opened.

## 5. Out of platform scope (owned elsewhere)
Domain content, concrete verifier oracles, concrete tools/skills/model-providers/infra adapters
— domain-owned (Velith / Mini Prometheus). Reference-only, never imported:
`reference/miniflywire/` (research), `reference/mininoetica/` (education, D11), `reference/velith/` (Velith docs).

## 6. Key artifacts
Constitution `docs/constitution/HANDBOOK_v1.1.md` · Roadmap `docs/roadmap/PLATFORM_ENGINEERING_ROADMAP_v1.1.md`
· Decisions `docs/decisions/DECISIONS.md` · Registry `docs/registry/PRIMITIVE_REGISTRY.md` (empty —
nothing promoted yet) · Spec `docs/specs/PE-21_DESIGN_SPEC.md` · Report `docs/reports/…FINAL_REPORT.md`
· Log `docs/logs/ENGINEERING_LOG.md`.

**Tags:** `pre-noetica-transform` · `repo-transformation-complete` · `pe-roadmap-v1` · `pe-roadmap-v1.1`
· `platform-engineering-v1`.
