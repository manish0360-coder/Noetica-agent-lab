# NOETICA — CONSTITUTIONAL ARCHITECTURAL AUDIT

**Auditor role:** Chief Systems Engineer & Constitutional Reviewer
**Authoritative document:** *Engineering Constitution and Architecture Handbook v1.1* (frozen)
**Repository audited:** `Noetica-agent-lab` (the only repository physically reachable this session)
**Method:** evidence-based inspection of every file. No assumptions. Where the Constitution and the repository disagree, the finding names both.
**Date:** 2026-07-01

---

## PREFACE — THE ONE FINDING THAT REFRAMES EVERYTHING

Before the phase-by-phase audit, one fact must be stated plainly because it governs how every later table reads:

> **The repository named `Noetica-agent-lab` does not contain Noetica.**
> It contains **MiniNoetica** — the education-domain "fractions tutor" that `DECISIONS.md` D11 explicitly classifies as *"a separate, completed reference project — not a dependency, not a layer, to be left behind."* The **Velith** engineering spike (M0/M1) that `PROJECT_STATE.md` certifies as *"complete"* is **physically absent** from this tree. And **Noetica the platform** — the subject of this audit — exists **only as specification**, with **zero implemented mechanisms**.

Everything below is built on that evidence. I did not assume it; I verified it (Phase 1).

---

## PHASE 1 — REPOSITORY UNDERSTANDING

### 1.1 What physically exists (verified, not assumed)

Complete inventory of `Noetica-agent-lab`:

**Python code (≈1,300 LOC across 4 packages):**

| Path | LOC | What it actually is |
|---|---|---|
| `core/agent.py` | ~150 | "Agent Zero" — a JSON status-loop (`{"status":"final"/"continue"}`) with a clean `terminated_reason` vs `success` split and a `check_fn` verifier seam. Logs every run to `data/agent_runs.jsonl`. |
| `core/llm.py` | ~60 | Thin Ollama adapter over `qwen3:4b`; `<think>` block scrubbing; capability guard for `think=`. |
| `core/logger.py` | ~15 | Append-only JSONL run logger. |
| `phase2_memory/knowledge_state.py` | ~180 | SQLite store of a **student's** per-concept `mastery` with deterministic update rules. |
| `phase2_memory/forgetting.py` | ~110 | Pure-function time-decayed recall (`recall = exp(-ln2·days/half_life)`). |
| `phase2_memory/concepts.py` | ~200 | Normalizes messy LLM concept strings to a fixed **fractions** curriculum. |
| `phase2_memory/verdict.py` | ~45 | `Verdict` dataclass with construction-time validation. |
| `phase2_memory/judge.py` | ~55 | **LLM-as-judge** correctness bridge (`qwen3:4b`). Self-labelled "⚠️ BRIDGE CODE. Temporary." |
| `phase2_memory/memory_agent.py` | ~160 | `MemoryAgent` sequencing extraction → normalize → store → recall. |
| `phase2_memory/capstone.py` | ~70 | Day-2 demo script. |
| `phase2_memory/step_judge_probe*.py` | — | Probe scripts. |
| `agent_zero/step1–9*.py` | ~460 | Nine exploratory probe scripts (seam, thinking, JSON-verify, model-compare). A **learning archive**. |
| `tests/*` | ~826 | 8 test modules, **70 `def test_` functions** (2 modules carry `@pytest.mark.live`). |

**Data:** `data/agent_runs.jsonl` — 54 recorded Agent-Zero runs.

**Documents (the bulk of the repository's mass):** `VISION.md`, `DECISIONS.md` (D1–D21), `PROJECT_STATE.md`, `M0_SPEC.md`, `M1_SPEC.md`, `M1_IMPLEMENTATION_HANDOFF.md`, `M2_SPEC.md`, `M2_IMPLEMENTATION_HANDOFF.md`, `README.md`, `NOTES.md`, plus a MiniFlyWire-flavoured science corpus (`research_problem.md`, `ontology.md`, `computational_theory.md`, `00_*`, `01_*`, `10_research_notebook.md`) and several empty placeholder files (`ARCHITECTURE.md`, `RESEARCH.md`, `ROADMAP.md`, `02_…`–`09_…` are 0 bytes).

### 1.2 What the documents claim exists — and does not

`PROJECT_STATE.md` (project header: **"Velith"**, tag `m1-complete`) states that the following are *"complete and certified"*:

```
src/velith/{task,episodes/episode,episodes/store,harness/verifier_sandbox,llm/client,agent/proposer,runner/spike}.py
docker/verifier.Dockerfile, docker-compose.yml, core/config.py
tests/{unit,integration,fixtures/calc_add_bug}/…
```

I searched for every one of these. **Result:**

```
src : ABSENT   velith : ABSENT   docker : ABSENT
docker-compose.yml : ABSENT   core/config.py : ABSENT   Dockerfile : ABSENT
grep -ril "episode|verifier|docker|propose" → only core/agent.py (a comment)
```

**Finding F1 (documentation/code divergence).** The certified M0/M1 Velith spike is not in this repository. The git log (`"Restore Noetica repository"`, `"Remove accidentally nested project directory"`) indicates the Velith and education trees were tangled and the Velith code lives in a different working tree. This is a **Law 18 violation** (documentation must not diverge from code) *within the reachable repository*, and it is the single largest impediment to the audit.

### 1.3 The identity split (three projects wearing one repo)

The repository is a superposition of three of the four constitutional projects, none cleanly separated:

- **README.md** presents the repo as *"Noetica — an Evidence-Based Learning **Intelligence** System … Phase 2 – Memory Agent"* → an **education** product (this is MiniNoetica).
- **DECISIONS.md / PROJECT_STATE.md / M0–M2 specs** are authored under the name **"Velith"** and describe the SWE `propose → verify → log` engineering loop.
- **The science corpus** (`ontology.md`, `computational_theory.md`, `research_problem.md`) is **MiniFlyWire** material (three domains, five functions, five laws, H1–H31).
- **Noetica** — the platform — is named everywhere and **implemented nowhere**.

Per the Constitution's own reconciliation (N.2/N.3), this is expected *history* — but as a *current repository state* it is a boundary hazard: the code present is the very code D11 says to **leave behind**.

---

## PHASE 2 — CONSTITUTION MAPPING (does each subsystem exist?)

Reading the Constitution Part VI (Noetica), IX (matrix) and X (laws), I enumerated every constitutional subsystem and checked the repository for an implementation. Summary before the full evidence table:

- **Noetica platform subsystems (24 mechanisms):** 0 implemented, 0 partial as *Noetica* code. A handful of **seed patterns** exist inside MiniNoetica (a `Verdict` type, a `check_fn` seam, a JSONL episode-shaped logger) but they are education-domain code, not extracted platform mechanisms.
- **Velith (engineering domain):** described as complete; **code absent** from this repo.
- **Mini Prometheus:** documentation-only (no code expected yet — correct).
- **MiniFlyWire:** exists as a **science corpus** (documents) + one legitimately promotable mechanism (`forgetting.py`) and one explicitly-barred anti-pattern (`judge.py`). This is the most constitutionally-aligned part of the repo.

---

## PHASE 3 — EVIDENCE TABLE

Status legend: ✅ Implemented · ⚠ Partially Implemented · ❌ Missing.
"Evidence" cites actual files. "Missing" means: *I searched the repository and found no implementation.*

### 3.1 Noetica platform mechanisms (Constitution Part VI / §9.2)

| Mechanism | Purpose | Const. § | Repo location | Status | Evidence | Owner (const.) | Dependencies | Notes |
|---|---|---|---|---|---|---|---|---|
| State Substrate / blackboard | Persistent typed provenance-tracked shared state; the true core | §6.1 | — | ❌ Missing | Searched repo; no substrate. `knowledge_state.py` is a *student-mastery* SQLite table, not a domain-agnostic substrate | Noetica | — | The single most load-bearing omission (echoes ARCHITECTURE_DECISION STEP 2) |
| Provenance & Lineage | Derivation of every belief; first-class | §6.2 | partial seed | ⚠ | `agent_runs.jsonl` records run traces; `Episode`-style provenance is *specified* (M1_SPEC §9.1) but code absent | Noetica | Substrate | Only run-level logging exists; no belief lineage |
| Runtime & Agent Lifecycle | Owns when cognition proceeds | §6.3 | `core/agent.py` | ⚠ | `run_agent()` is a bounded status-loop with clean termination — a *seed*, education-domain | Noetica | LLM adapter | Not a Noetica mechanism; a MiniNoetica loop |
| Memory Framework | Episodic/experience persistence + write-filter | §6.4 | `phase2_memory/*` | ❌ (as Noetica) | `phase2_memory` persists *student mastery*, not agent episodes; no write-filter policy (A1/A2) | Noetica | Substrate | D11 says leave behind |
| Knowledge Store Engine | Typed semantic/graph store | §6.5 | — | ❌ Missing | No graph/typed knowledge store | Noetica | Substrate | — |
| Context Engine | Working-set assembly / window budgeting | §6.6 | — | ❌ Missing | No context assembler | Noetica | Memory, Knowledge | — |
| Reasoning Runtime (form) | Iterate inference, verification seams, backtrack | §6.7 | `core/agent.py` | ⚠ | The continue/final loop is a primitive reasoning loop; no backtracking/verification seam beyond `check_fn` | Noetica | Runtime | Seed only |
| Planning Runtime (repr+executor) | Express/sequence/execute plans | §6.8 | — | ❌ Missing | No plan representation or executor | Noetica | Runtime | — |
| Reflection | Self-critique loop | §6.9 | — | ❌ Missing | One-shot JSON "repair" retry in `agent.py` is not reflection | Noetica | Reasoning | — |
| Evaluation Harness | Arms, held-out lock, metrics | §6.10 | — | ❌ Missing | No arms, no held-out lock; A0–A4 only specified (D7) | Noetica | Verifier proto | — |
| Verification Protocol | `Verifier`/`Verdict`; oracle stays in domain | §6.11 | `phase2_memory/verdict.py` | ⚠ | A validated `Verdict` dataclass exists (good seed pattern), but no `Verifier` protocol and no held-out harness | Noetica | — | `Verdict` is the correct seed shape |
| Tool Runtime & Interface | Register/invoke/sandbox tools; async | §6.12 | — | ❌ Missing | No `Tool` interface | Noetica | Runtime | — |
| Skill Runtime & Interface | Composable learned competence | §6.13 | — | ❌ Missing | No `Skill` interface | Noetica | Runtime | — |
| Budget / Meta-control | How much to think, when to stop | §6.14 | token counters only | ❌ | `agent.py` counts tokens but no budget policy/cap | Noetica | Router | — |
| Model Abstraction & Routing | Swappable models + cost guard | §6.15 | `core/llm.py` | ⚠ | Thin single-provider (Ollama) adapter with capability guard; **no routing, no cost guard** | Noetica | — | The D16.4 "adapter seed"; not yet a router |
| Guardrails / Safety Engine | Enforce oversight boundary | §6.16 | — | ❌ Missing | No policy engine | Noetica | Runtime | — |
| Observability & Logging | Structured logs/metrics/traces | §6.17 | `core/logger.py` | ⚠ | Append-only JSONL run logger + per-step trace | Noetica | — | Minimal but real; run-level only |
| Developer Surface (SDK/plugin/API) | Stable versioned consumption surface | §6.18 | — | ❌ Missing | No SDK/plugin/public API | Noetica | All | — |
| Internal APIs | Private plumbing + reference/fake verifier | §6.19 | `check_fn` seam | ⚠ | `check_fn(answer)->bool` is a reference-verifier seam pattern | Noetica | — | Right idea, wrong layer |
| Belief / Probabilistic State | Confidence, epistemic/aleatoric | §6.1, §8.3 | `Verdict.confidence` | ❌ | A `confidence` float field exists on `Verdict`; no belief-state substrate | Noetica | Substrate | Gemini/ARCH-DECISION flagged |
| Experience Aggregation | First-class up-flow home | §4.3, §6(evolution) | — | ❌ Missing | No aggregation mechanism | Noetica | Memory | Gated on 2nd consumer (Appendix D) |
| Compute Interface & Budgeting | Abstract request/place/cap compute | §6.21 | — | ❌ Missing | No compute interface | Noetica | Budget | — |
| Experience Data Contracts | Versioned episode/dataset schemas | §4.3, Law 21 | — | ❌ Missing | `agent_runs.jsonl` records are **unversioned** | Noetica | — | Law 21 gap |
| Data Lifecycle Governance | Compression/retention/pruning/bounds | §11.11 | — | ❌ Missing | No retention/pruning/bounded-storage policy declared | Noetica | Data contracts | §11.11 gap |
| Held-out Lock (mechanical) | Code-enforced eval exclusion | §5.6, D8 | — | ❌ Missing | Specified only | Noetica | Eval harness | — |

### 3.2 Velith (engineering intelligence — Constitution Part VII)

| Mechanism | Purpose | Const. § | Repo location | Status | Evidence | Notes |
|---|---|---|---|---|---|---|
| propose→verify→log loop | Engineering core | §7.5 | *claimed* `src/velith/runner/spike.py` | ❌ Missing (in repo) | `PROJECT_STATE.md` certifies it; **file absent** (F1) | Lives in another tree |
| Deterministic SWE Verifier/oracle | Grounded truth (compile+hidden tests) | §7.3, D3 | *claimed* `harness/verifier_sandbox.py` | ❌ Missing (in repo) | Absent | Correctly *domain*-owned when it exists |
| Episode store (content-hash) | Provenance-complete episodes | §7.5, D16.6 | *claimed* `episodes/store.py` | ❌ Missing (in repo) | Absent; `agent_runs.jsonl` is the education analogue | — |
| Migration ladder (SWE→…→mfg) | Generality by registration | §7.7, D5 | docs only | ⚠ (design) | D4/D5 ratified; rung 1 code absent | — |
| Compounding experiment (A0–A4) | Scientific obligation | §7.6, D6–D8 | docs only | ❌ Missing | No harness, no arms | — |

### 3.3 Mini Prometheus (Part VIII) & MiniFlyWire (Part V)

| Mechanism | Purpose | Const. § | Status | Evidence |
|---|---|---|---|---|
| Manufacturing planner / twin / Sim2Real | Top layer | Part VIII | ❌ Missing | Correct — not due yet (built only after Velith proven) |
| Cognitive theory (3 domains / 5 functions) | MiniFlyWire science | §1.6, Part V | ✅ Implemented (as docs) | `computational_theory.md`, `ontology.md`, `research_problem.md` |
| `forgetting` mechanism | Promotable primitive | §5.3, 2.1 good ex. | ✅ (research-grade) | `phase2_memory/forgetting.py` — pure, domain-agnostic, dependency-light |
| `KnowledgeState` update rule | Promotable primitive | 2.1 good ex. | ✅ (research-grade) | `phase2_memory/knowledge_state.py` |
| Promotion gate / Primitive Registry | Certify validated mechanisms | §5.5, §11.5 | ❌ Missing | No registry, no recorded gate pass |
| `judge.py` (LLM-as-judge) | Studied **negative** result | 2.1 bad ex., D11 | ⚠ Present-as-anti-pattern | `phase2_memory/judge.py` — allowed *inside* MiniNoetica, **barred from promotion** (Law 7) |

---

## PHASE 4 — BOUNDARY AUDIT

Each present module judged against the Constitution's mechanism/content and layer boundaries.

| Module | Belongs in Noetica? | Correct location | Verdict | Constitution law engaged |
|---|---|---|---|---|
| `core/agent.py` (Agent-Zero loop) | No | **MiniNoetica** (reference) | *Wrong-label*: sits in a repo called Noetica but is education reference code; a *pattern seed* for the Runtime, not the Runtime | Law 3 (mechanism≠content), Law 8 (extract, don't relabel) |
| `core/llm.py` (Ollama adapter) | Its **pattern** yes; this code no | MiniNoetica | Correct *shape* for the future `ModelRouter` seed (D16.4); must be **re-implemented**, not imported | Law 6, Law 7 |
| `core/logger.py` | Pattern yes | MiniNoetica | Seed for observability/episode-JSONL | Law 8 |
| `phase2_memory/knowledge_state.py` | No | MiniNoetica (student model) | **Content**, not mechanism — models a *student's* knowledge (theory-of-mind), which D15/D11 explicitly defer/exclude | Law 3, Law 5 |
| `phase2_memory/forgetting.py` | As a **spec**, yes (promotion) | MiniFlyWire → Noetica by re-impl | **Promotion candidate** — passes the gate's domain-agnostic/dependency-light bar; must cross as spec, never import | Law 7, Knowledge Flow |
| `phase2_memory/concepts.py` | No | MiniNoetica | Curriculum content (fractions) | Law 5 |
| `phase2_memory/verdict.py` | **Pattern** yes | Seed for Noetica `Verdict` | Construction-time-validated `Verdict` is the *correct seed pattern* the ARCHITECTURE_DECISION praised; re-implement upward | Law 15, Law 14 |
| `phase2_memory/judge.py` | **Never** | MiniNoetica only | **Barred anti-pattern** (LLM-as-judge). Permitted as a studied negative *inside* research; **promotion forbidden** | Law 7 (anti-pattern bar), D3, D11 |
| `agent_zero/step1–9` | No | MiniNoetica learning archive | Exploratory probes; not production; fine where they are | Law 4 (research not shipped) |

**Boundary violations found:**

- **BV1 — Repo-naming / content mismatch.** A repository named `Noetica-agent-lab` whose entire code payload is MiniNoetica education code plus Velith *documents*. Per D11, MiniNoetica must be *"a separate, read-only reference with zero coupling."* Housing it in the "Noetica" repo invites exactly the boundary erosion D11 warns of. *(Repository rule §11.9.)*
- **BV2 — Anti-pattern present in the platform-named repo.** `judge.py` (LLM-as-judge) is the precise thing D3/D11 exist to eliminate. It is legal *as MiniNoetica reference*, but its presence in the "Noetica" tree is a promotion-hazard that must be fenced (Law 7).
- **BV3 — No mechanism/content separation enforced.** There is no package-level DAG, no CI import check, no separation of `noetica/` vs `velith/` vs research (Repository checklist §13.4 all unmet).

**Dependency violations:** none of the *illegal* kind (no upward/cyclic/sibling imports) — because there are no layers to cross. The DAG is trivially clean by virtue of being unbuilt. *This is health-by-absence, not health-by-design.*

**Extraction candidates (legitimate, when Velith code returns):** `Verdict` shape, `check_fn` verifier seam, episode→JSONL pattern, single-owner LLM-call shape, test-discipline. All are **re-implementation** seeds (D11), never imports.

---

## PHASE 5 — REPOSITORY HEALTH

**Architecture quality (of what exists).** The MiniNoetica code is genuinely well-engineered: crisp single-responsibility modules, deterministic math owned by the store (not the LLM), pure-function forgetting, a validated `Verdict`, an honest `terminated_reason` vs `success` split, and documented debt. This is *good craft* — but it is craft on the **wrong layer** for a Noetica audit.

**Code organization.** Flat top-level with ~30 markdown files intermixed with 4 code packages. No `src/`, no package boundaries, 8 empty 0-byte placeholder docs. Organization reflects a learning journal, not a platform.

**Layer separation.** **None enforced.** No `noetica/`, `velith/`, `miniflywire/` packaging; no CI DAG check (§11.9/§13.4 unmet).

**Dependency graph.** Trivial and acyclic (`tests → phase2_memory/core → ollama`). Clean only because nothing is layered.

**Naming consistency.** **Poor at the project level** — "Noetica," "Velith," "MiniNoetica," "PrometheusLite" all refer to overlapping things across docs (the Constitution's N.2 map exists precisely because of this). Module-level naming is good.

**Technical debt (concrete):**

- **TD1 — Broken demo:** `phase2_memory/capstone.py` calls `agent.analyze(...)`, but `MemoryAgent` exposes `update_from_verdict()` / `extract_answer_analysis()` — there is **no `analyze` method**. The capstone cannot run as written.
- **TD2 — Dead/duplicated code:** `memory_agent.py` defines `_flagged_record` **twice** (the first is shadowed and unused).
- **TD3 — Doc/code divergence (F1):** `PROJECT_STATE.md` certifies absent `src/velith/` files (Law 18).
- **TD4 — Unversioned experience records:** `agent_runs.jsonl` has no schema/contract version (Law 21).
- **TD5 — 8 empty spec files** (`ARCHITECTURE.md`, `RESEARCH.md`, `ROADMAP.md`, `02–09_*.md`) — the ROADMAP the ecosystem needs is a 0-byte file.
- **TD6 — Uncommitted drift:** `git status` shows 10+ modified files (README, all `agent_zero/step*`) uncommitted.

**Dead / experimental / reference / production code split.** ~40% exploratory probes (`agent_zero/*`, `step_judge_probe*`), ~50% reference education modules (`phase2_memory/*`, `core/*`), ~0% production platform code, ~10% demo/glue. **Production-ready Noetica code: none.**

**Platform maturity:** pre-implementation. **Scientific maturity:** moderate — the theory corpus is rich and the two promotable primitives are real. **Engineering maturity (of MiniNoetica):** solid for a learning sprint; test count 70 functions (README claims 58 pass / 5 skip — *I could not execute pytest in-session to confirm; the claim is unverified by execution but 70 test functions are statically present*).

---

## PHASE 6 — NOETICA MATURITY ASSESSMENT

**Assessment: Noetica is at the "Documentation-Led / Pre-Skeleton" stage — below Platform Skeleton.**

Reasoning from evidence:

- A **Platform Skeleton** requires at least the state substrate + one interface + a runnable end-to-end path *in the platform*. Noetica has **zero** implemented mechanisms (Phase 3.1: 24 rows, 0 ✅ as Noetica code). It therefore has not reached Skeleton.
- What *is* mature is a **Research Prototype of education cognition (MiniNoetica)** — which the Constitution explicitly rules **out of the Noetica layer** (D11). Crediting it to Noetica's maturity would itself be a boundary violation.
- The **specification** maturity is unusually high: the Constitution, `DECISIONS.md` (D1–D21), and the M0–M2 specs are production-grade *design*. Noetica is **specification-complete and implementation-empty**.

> Verdict: **Noetica = a fully-designed platform with no platform code.** The intellectual scaffolding is arguably at "Reusable Platform" quality on paper; the codebase is at zero. The gap between the two is the entire body of work ahead.

---

## PHASE 7 — GAP ANALYSIS

For each missing mechanism: why it is required, why it belongs in Noetica, which law compels it, and which downstream project depends on it. (Ordered by build-necessity.)

1. **State Substrate (§6.1, Principle 2, D9).** *Required* because intelligence must be *about* persistent state; without it the platform drifts into a "bag of agents" D9 forbids. *Belongs in Noetica* as the true core (matrix: Owner=Noetica). *Depends downstream:* **Velith** (artifact-under-design lives here), **Mini Prometheus** (twin content syncs here). Compels: Law 3, Law 13.
2. **Provenance & Lineage (§6.2, Principle 7, Law 18).** Required so "why did it do that?" is answerable; the compounding experiment is uninterpretable without it. Velith's episodes and Mini Prometheus's telemetry both attach here.
3. **Verification Protocol + `Verdict` (§6.11, Law 15/16).** Required to ground truth externally; the `Verdict` must support *distributions* (Law 16) for the approximate rungs. Velith supplies the SWE oracle; Mini Prometheus the manufacturing checks. The repo already has the correct **seed** (`verdict.py`).
4. **Episode Store + Data Contract (§7.5, Law 21).** Required as first-class learning data; must be versioned (Law 21). Velith produces episodes; MiniFlyWire consumes distilled datasets.
5. **Memory Framework + write-filter (§6.4, D7).** The write-filter is *the single manipulated variable* of the compounding experiment (A1 vs A2). Without it, §1.7 cannot be tested — the program's spine. Velith depends on it directly.
6. **Model Router + cost guard (§6.15, Principle 3, D16.4).** Guarantees LLM-swappability and bounds spend. Seed exists (`llm.py`); must grow into routing. All layers depend.
7. **Evaluation Harness + mechanical held-out lock (§6.10, §5.6, D8).** Owned once, reused every rung; makes results comparable across the decade. Velith configures it.
8. **Reasoning / Planning / Reflection runtimes (§6.7–6.9).** The *forms* every domain reuses; Velith expresses engineering plans as Noetica plans.
9. **Tool / Skill runtimes (§6.12–6.13).** "Wrap, don't rebuild" — Velith's CAD/solvers and Mini Prometheus's MES/robots implement these.
10. **Belief/Probabilistic State (§6.1 evolution, §8.3, Law 16).** Required *before the first approximate (PCB/FEA) rung*; Mini Prometheus's probabilistic reality (Gemini review §3) depends on it. Gated (Appendix D) — not built speculatively.
11. **Experience Aggregation (§4.3), Compute Interface (§6.21), Data Lifecycle (§11.11), Guardrails (§6.16), Context/Knowledge engines (§6.5–6.6).** Each required by its cited section; each **extraction-gated** on a real second consumer (Law 8) — i.e., *not* to be built now.

**Downstream dependency chain (as the prompt frames it):**
`MiniFlyWire` (validated primitives: `forgetting`, `KnowledgeState`-rule) **→** `Noetica` (substrate/provenance/verifier/memory/router — all missing) **→** `Velith` (SWE loop — code absent) **→** `Mini Prometheus` (not yet due). Every arrow above the first is currently **broken at the Noetica node.**

---

## PHASE 8 — NOETICA ROADMAP v1

Derived **only** from (1) the Constitution, (2) repository gaps found above, (3) existing repository seeds. No invented features. Every item traces to a cited section/decision. The roadmap obeys the Roadmap checklist (§13.6): every milestone yields a *running system*, each is a *hardening of the prior*, interfaces are built only as the loop exercises them, and the migration ladder is respected.

> **Governing constraint (Law 8):** Noetica grows **by extraction from Velith**, not speculative design. Therefore Roadmap v1 does **not** build 24 mechanisms up front. It re-establishes the Velith spike, then extracts the 3–4 mechanisms that spike actually exercises. This is the Constitution's own prescription (N.3, §11.4).

### Milestone N0 — Repository Honesty & Boundary Separation
- **Objective:** make the repository's physical state match the Constitution before any new code.
- **Build:** split the tree into enforced packages — `miniflywire/` (move `phase2_memory/*`, `agent_zero/*`, science corpus, mark read-only per D11), and a clean `noetica/` empty package with a package-DAG CI check (§11.9, §13.4). Recover or re-clone the absent `src/velith/` tree (F1); if unrecoverable, mark `PROJECT_STATE.md` claims as *aspirational* to cure the Law 18 divergence. Write the 0-byte `ROADMAP.md`/`ARCHITECTURE.md`/`RESEARCH.md`. Fix TD1/TD2 (broken `capstone.analyze`, duplicate `_flagged_record`).
- **Dependencies:** none. **Verification:** CI fails on any cross-package/upward import (Law 9/12/19/20); no doc certifies an absent file. **Done when:** a fresh clone goes green with one command (§13.4) and every certified file exists.
- **Why first:** you cannot audit, extract, or grow a platform whose repository lies about what it contains. Cures BV1–BV3, F1, TD1–TD6.

### Milestone N1 — Re-establish the Velith Spike (extraction source)
- **Objective:** a real, reproducible `propose → verify → log` engineering episode (Constitution §7.5; the M1 spec already exists).
- **Build (in `velith/`, not Noetica):** the deterministic containerized SWE verifier, the content-hashed `Episode`, the thin LLM client, the `spike` orchestrator — **from the existing M1_SPEC**, re-implementing (not importing) the MiniNoetica seeds (`Verdict`, `check_fn`, episode-JSONL, LLM-call shape) per D11.
- **Dependencies:** N0. **Verification:** D16.1 record/replay (same proposal → same verdict + content hash); all five verdict states reachable (D16.7); hermetic CI (D13). **Done when:** one grounded episode survives container exit with a verifying hash.
- **Why before N2:** Law 8 forbids extracting a platform mechanism that has no real consumer. N1 *is* the consumer. Nothing is extracted upward until it runs here first.

### Milestone N2 — First Extraction: State Substrate + Provenance + Episode Store
- **Objective:** extract the substrate, provenance, and episode store from the N1 spike into `noetica/` behind versioned interfaces (§6.1, §6.2, §7.5; §11.4 extraction process).
- **Build:** `StateSubstrate` + `Provenance` + `EpisodeStore` interfaces with default impls; a **versioned episode data contract** (Law 21); Velith refactored to *consume* them.
- **Dependencies:** N1 (real consumer exists). **Verification:** reproducibility test (content-hash identity, §11.10); data-contract version + migration present (Law 21); Velith imports Noetica only (Law 9). **Done when:** the N1 episode is written *through Noetica's store* with unchanged hashes.
- **Why now:** these three are the mechanisms the spike unavoidably exercises — the highest-confidence, lowest-speculation extractions (§6.1 "the true core").

### Milestone N3 — Verification Protocol + Reference Verifier + Model Router
- **Objective:** extract the `Verifier` **protocol** and `Verdict` (leaving the SWE oracle in Velith, Law 15), and the `ModelRouter` seed (§6.11, §6.15, D16.4).
- **Build:** `Verifier` protocol + closed-taxonomy `Verdict` (distribution-*capable*, Law 16) in Noetica; Velith's `SweVerifier` implements it; `ModelRouter` with a hard cost guard; **Noetica self-tests use a reference/fake verifier only** (Law 20).
- **Dependencies:** N2. **Verification:** boundary test (no domain oracle in Noetica self-tests, §11.10); router swaps providers; cost guard caps spend. **Done when:** Velith runs end-to-end against Noetica's protocol with a fake verifier passing Noetica's own tests.
- **Why now:** verification-ownership is the boundary the repo's history got wrong (§6.11); fixing it early prevents the leak recurring.

### Milestone N4 — Memory Framework + Write-Filter + Eval Harness (enables §1.7)
- **Objective:** stand up the memory write-filter (A1 unfiltered vs A2 verified) and the evaluation harness with a mechanical held-out lock (§6.4, §6.10, D7, D8).
- **Build:** `MemoryStore` + write-filter policies; `EvalHarness` with arms A0/A1/A2 and code-enforced held-out exclusion; the A1≡A2-retriever integrity test (§11.10).
- **Dependencies:** N3 (episodes + verifier + router). **Verification:** experiment-integrity test (A1/A2 share retriever); held-out lock provable in code; effect-size reporting (§5.6). **Done when:** a Stage-1 A0-vs-A2 go/no-go can run (D12 M9/M10 analogue).
- **Why last of the core:** this is the machinery that finally tests the program's falsifiable spine (§1.7). It depends on everything N1–N3 and must not precede them.

### Milestone N5+ — Gated / Postponed (do NOT build before their gate)
Per Appendix D and Law 8, the following are **recorded as postponed**, each gated on a validation result, and must not be built early: belief/probabilistic substrate (gated on reaching the PCB/FEA rung), experience-aggregation (gated on a credible 2nd consumer), learned meta-control (gated on the compounding result), context/knowledge-graph engines, guardrails engine, compute interface, data-lifecycle framework. Building any before its gate is a §11.8 deviation requiring a recorded justification.

**Ordering rationale (why each precedes the next):** N0 makes the repo honest (precondition for all); N1 creates the *consumer* Law 8 requires; N2–N3 extract only what N1 exercises (substrate→verifier→router, in dependency order); N4 assembles those into the experiment that justifies the whole program (§1.7). No milestone builds a mechanism lacking a live consumer — the roadmap *is* platform-by-extraction.

---

## PHASE 9 — FINAL EXECUTIVE REPORT

### 1. Repository summary
`Noetica-agent-lab` is a **specification-complete, implementation-empty** platform project. Physically it contains **MiniNoetica** (a well-crafted education/fractions-tutor reference codebase, ~1,300 LOC, 70 test functions) plus a **large, high-quality document corpus** describing three other things: the **Velith** SWE engineering spike (certified "complete" but whose code is **absent** from this tree), the **MiniFlyWire** cognitive science, and the **Noetica** platform (designed in full, coded not at all). The intellectual architecture is excellent and frozen; the platform codebase does not yet exist.

### 2. Constitutional Compliance Score: **58 / 100**
*Design compliance is near-perfect; repository-state compliance is weak.* The Constitution, `DECISIONS.md`, and `ARCHITECTURE_DECISION.md` conform to and even author the frozen laws (+). Against them the *repository* shows: doc/code divergence certifying absent files (Law 18, −), an LLM-as-judge anti-pattern sitting in the platform-named repo (Law 7 hazard, −), no package-DAG/boundary enforcement (§11.9/§13.4, −), unversioned experience records (Law 21, −), no data-lifecycle policy (§11.11, −), and no Primitive Registry (§11.5, −). Few *hard* violations exist only because most mechanisms are unbuilt — compliance-by-absence, not by design.

### 3. Platform Maturity Score: **9 / 100**
Zero of 24 Noetica mechanisms implemented as platform code. Points awarded only for genuine **seed patterns** (`Verdict`, `check_fn` seam, LLM adapter, JSONL logger) and world-class specifications. (MiniNoetica *as a research prototype* would score ~60, but it is out-of-layer.)

### 4. Strengths
Verification-first, state-centric, compounding-as-the-test philosophy is rigorously specified and internally consistent. The mechanism/content and interface/implementation invariants are textbook. Platform-by-extraction (Law 8) is the correct growth model. The `Verdict` dataclass, the `terminated_reason`↔`success` split, and pure-function `forgetting` are exactly the right seed patterns. The decision record (D1–D21) is disciplined and append-only. MiniFlyWire yields two legitimately promotable primitives.

### 5. Weaknesses
No platform code exists. Repository physically conflates three projects. Documentation certifies code that is absent (Law 18). An anti-pattern (`judge.py`) lives in the tree. No package boundaries or CI enforcement. Broken demo (`capstone.analyze`), duplicated dead code, 8 empty spec files, uncommitted drift. Experience records unversioned; no lifecycle governance.

### 6. Missing mechanisms (highest-impact first)
State Substrate · Provenance · Verification Protocol · Episode Store + Data Contract · Memory write-filter · Model Router · Evaluation Harness + held-out lock · Reasoning/Planning/Reflection runtimes · Tool/Skill runtimes · Belief state · Experience Aggregation · Compute Interface · Data Lifecycle · Guardrails · Context/Knowledge engines · Primitive Registry.

### 7. Boundary violations
**BV1** repo-name/content mismatch (MiniNoetica inside "Noetica," §11.9/D11). **BV2** LLM-as-judge present in the platform repo (promotion hazard, Law 7). **BV3** no mechanism/content separation or CI DAG (§13.4).

### 8. Dependency violations
None of the illegal kind (no upward/cyclic/sibling imports) — the DAG is clean **only because there are no layers to cross**. Health-by-absence.

### 9. Technical debt
TD1 broken `capstone.analyze`; TD2 duplicate `_flagged_record`; TD3 doc/code divergence (F1, Law 18); TD4 unversioned `agent_runs.jsonl` (Law 21); TD5 eight empty spec files incl. `ROADMAP.md`; TD6 uncommitted modified files.

### 10. Highest-priority work
**N0 (repository honesty & boundary separation)** then **N1 (re-establish the Velith spike)**. Nothing else is auditable or extractable until the repo tells the truth and a real consumer exists.

### 11. Lowest-priority work
Belief/probabilistic substrate, experience-aggregation, learned meta-control, compute interface, data-lifecycle framework, context/knowledge-graph engines — all **extraction- or validation-gated** (Appendix D, Law 8) and must **not** be built before their gates.

### 12. Recommended next milestone
**N0 — Repository Honesty & Boundary Separation.** Split into enforced `miniflywire/`, `velith/`, `noetica/` packages with a CI package-DAG check; recover or honestly re-label the absent `src/velith/` tree (cure Law 18); fence `judge.py` as read-only research; fix TD1/TD2; write the empty `ROADMAP.md`. It is small, unblocks everything, and converts the repository from *documentation-led* to *evidence-led* — the precondition the Constitution's own Decision Protocol (Part XII) demands before any feature is built.

### 13. Noetica Roadmap v1
`N0` Repository honesty & boundaries → `N1` Re-establish Velith spike (consumer) → `N2` Extract Substrate + Provenance + Episode Store → `N3` Verification Protocol + Reference Verifier + Model Router → `N4` Memory write-filter + Eval Harness + held-out lock (enables §1.7) → `N5+` gated/postponed mechanisms (belief state, experience aggregation, learned meta-control, …). Every item derives from the Constitution, a repository gap, or an existing seed. None is invented.

---

### Auditor's closing note (Law 22)
This is an **AI review**. Per Law 22 it may **reject and recommend** but **never ratifies**. Every finding above names its evidence and the constitutional section engaged; nothing missing was inferred — where code was absent I searched and said so. The roadmap changes **no** boundary, introduces **no** fifth project (the Gemini review's "Physis" layer is correctly declined — the Constitution folds physical grounding into Velith content + Noetica belief-state), and merges nothing. Any architectural change it implies still requires a ratified CAP and explicit project-owner approval (Law 23).
