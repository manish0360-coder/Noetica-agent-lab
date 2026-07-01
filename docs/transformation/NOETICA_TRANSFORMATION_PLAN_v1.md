# NOETICA REPOSITORY TRANSFORMATION PLAN v1

**Owner:** Chief Systems Engineer (this transformation is mine to execute; ownership decided from the Constitution, not asked of you)
**Authority:** *Engineering Constitution & Architecture Handbook v1.1* (RATIFIED, frozen)
**Target:** transform `Noetica-agent-lab` **in place** into the canonical **Noetica** platform repository (Layer 2), co-packaging **Velith** (Layer 3) behind an enforced package DAG, per §11.9.
**Constraints honored:** incremental · history-preserving · reversible · no architecture redesign · no new layers · no fifth project · Law 8 (grow by extraction, no speculative mechanisms).
**Status:** AWAITING APPROVAL. No files have been changed. Phase 4 executes one step at a time, only after you approve.

---

## GUIDING RULINGS (decided from the Constitution before any file moves)

1. **Packaging (§11.9).** "Noetica + Velith may begin as one repository with enforced internal package boundaries." → This repo becomes the **Noetica+Velith monorepo**. The boundary is enforced as a **package-level DAG in CI**, not by splitting Git repos now.
2. **MiniNoetica (D11).** The education/fractions code (`core/*`, `phase2_memory/*`, `agent_zero/*`, their tests + `data/`) is a **separate, completed, read-only reference with zero coupling** — explicitly "left behind." → **ARCHIVE** it to `reference/mininoetica/` (history preserved via `git mv`), fenced by a CI rule that `src/` may never import `reference/`. It is never deleted (it is the extraction/pattern source), never imported.
3. **MiniFlyWire (§11.9, Part V).** The cognitive-science corpus is **research documents**, owner = MiniFlyWire, consumed by Noetica only via **re-implementation** (Knowledge Flow), never import. → **MOVE** to `docs/miniflywire/`. No code, so no coupling risk.
4. **Velith code is ABSENT (audit finding F1).** `PROJECT_STATE.md` certifies `src/velith/` (M0/M1) as complete, but the tree is not in this repo — a Law 18 divergence. → The plan **restores it by re-implementation from `M1_SPEC`** as the final milestone (it is the first real *consumer* Law 8 requires before any platform mechanism is extracted).
5. **No speculative platform (Law 8, §13.6).** I will **scaffold the full canonical directory structure and design the interface surface**, but **implement only** mechanisms exercised by a real consumer. Empty subsystem packages are honest placeholders ("interfaces designed early; depth added on a schedule"), not fake implementations.
6. **The anti-pattern is fenced, not promoted (Law 7).** `phase2_memory/judge.py` (LLM-as-judge) is archived as a *studied negative* and marked non-promotable. It never enters `src/`.

---

## PHASE 1 — FILE-BY-FILE TRANSFORMATION PLAN

Action set: **KEEP** (stays, canonical) · **MOVE** (relocate, `git mv`, history preserved) · **REIMPLEMENT** (pattern re-created cleanly in `src/`; original archived, never imported) · **ARCHIVE** (to `reference/`, read-only) · **DELETE** (empty/superseded; recoverable via the pre-transform tag).

### 1A — Governance & authority documents

| File | Action | Destination | Why / Constitution | Owner | Platform mechanism? | Historical ref? |
|---|---|---|---|---|---|---|
| `DECISIONS.md` (D1–D21) | MOVE | `docs/decisions/DECISIONS.md` | Authority #2 (P.2); append-only ledger (§11.7). Kept verbatim. | Ecosystem governance | No | Yes (living) |
| `VISION.md` | MOVE | `docs/vision/VISION.md` | Authority #3 (P.2). | Ecosystem | No | Yes |
| `PROJECT_STATE.md` (Velith) | MOVE | `docs/velith/PROJECT_STATE.md` | Velith milestone state (§13.7). | Velith | No | Yes (living) |
| `M0_SPEC.md`,`M1_SPEC.md`,`M1_IMPLEMENTATION_HANDOFF.md`,`M2_SPEC.md`,`M2_IMPLEMENTATION_HANDOFF.md` | MOVE | `docs/velith/milestones/` | Velith milestone specs; `M1_SPEC` is the restoration source (Ruling 4). | Velith | No | Yes |
| `NOTES.md` | MOVE | `docs/velith/NOTES.md` | M2 capability-gating notes. | Velith | No | Yes |
| `NOETICA_ARCHITECTURAL_AUDIT_v1.md` | MOVE | `docs/audits/` | Prior audit deliverable. | Noetica | No | Yes |
| `README.md` (education) | REIMPLEMENT | new `README.md` (Noetica platform) + archive old | Current README is the "Evidence-Based Learning" product (MiniNoetica). Canonical repo needs a platform README (Law 18 parity). Old copy → `reference/mininoetica/README.md`. | Noetica | No | Old: yes |

### 1B — Constitution (currently uploaded, not yet in repo) — IMPORT (new to repo)

| File (source: session uploads) | Action | Destination | Why |
|---|---|---|---|
| `ENGINEERING_CONSTITUTION_AND_ARCHITECTURE_HANDBOOK.md` | IMPORT | `docs/constitution/HANDBOOK_v1.1.md` | The repo must physically contain its own highest authority (P.1). |
| `ARCHITECTURE_CONSTITUTION_v1.0.pdf` | IMPORT | `docs/constitution/` | Frozen v1.0 source (Appendix B). |
| `ARCHITECTURE_DECISION.md` | IMPORT | `docs/constitution/` | Ratification-stage review (Appendix B). |
| `Gemini_Review.txt` | IMPORT | `docs/constitution/reviews/` | Independent review (§11.6.11). |

### 1C — MiniFlyWire research corpus → `docs/miniflywire/` (MOVE)

Owner: **MiniFlyWire** (Part V). Consumed by re-implementation only (Law 7). No coupling risk (documents).

| File | Action | Note |
|---|---|---|
| `research_problem.md`, `ontology.md`, `computational_theory.md`, `computational_mechanisms.md`, `engineering_cognition_synthesis.md` | MOVE | Core science (§1.6). |
| `00_project_definition.md`, `00_research_axioms.md`, `00_research_vision.md`, `00_research_vision_v2_draft.md`, `01_cognitive_ontology.md`, `01_core_question.md`, `10_research_notebook.md`, `idea_backlog.md` | MOVE | Notebook + framing (Appendix B). |
| `02_hypotheses.md`…`09_decisions.md` (8 files, **0 bytes**) | DELETE | Empty placeholders; superseded by `10_research_notebook.md`. Recoverable via pre-transform tag. |

### 1D — MiniNoetica education code → `reference/mininoetica/` (ARCHIVE; D11)

Read-only. Never imported by `src/` (CI-enforced). Patterns re-implemented upward, never moved as code.

| File(s) | Action | Re-implementation target (later, by extraction/promotion) | Law |
|---|---|---|---|
| `core/agent.py` (Agent-Zero loop, `check_fn` seam) | ARCHIVE | seeds `src/noetica/runtime/` + reference/fake verifier (`src/noetica/verification/`) | Law 6/8 |
| `core/llm.py` (Ollama adapter) | ARCHIVE | seeds `src/noetica/router/` (D16.4) | Law 3/7 |
| `core/logger.py` (JSONL logger) | ARCHIVE | seeds `src/noetica/observability/` + episode store | Law 8 |
| `phase2_memory/verdict.py` (validated `Verdict`) | ARCHIVE | seeds `src/noetica/verification/` `Verdict` (Law 15/16) | Law 15 |
| `phase2_memory/forgetting.py`, `knowledge_state.py` | ARCHIVE | **MiniFlyWire promotion candidates** → re-implemented into `src/noetica/memory/` from spec (Law 7) | Law 7 |
| `phase2_memory/concepts.py` | ARCHIVE | none (curriculum **content**, Law 5) | Law 5 |
| `phase2_memory/judge.py` (LLM-as-judge) | ARCHIVE (fenced) | **NEVER promoted** — studied negative (Law 7 anti-pattern bar) | Law 7 |
| `phase2_memory/memory_agent.py`, `capstone.py`, `step_judge_probe*.py`, `__init__.py` | ARCHIVE | none (education glue; `capstone.py` also carries bug TD1) | D11 |
| `agent_zero/step1–9*.py` | ARCHIVE | none (learning archive) | Law 4 |
| `tests/test_*.py` (8 files, education) + `tests/__init__.py` | ARCHIVE → `reference/mininoetica/tests/` | move *with* their code so they still run in isolation | D11 |
| `data/agent_runs.jsonl` (54 unversioned records) | ARCHIVE | none (education telemetry; Law 21 non-compliant) | Law 21 |
| `docs/project_state.md` (older education state) | ARCHIVE → `reference/mininoetica/docs/` | distinct from the Velith `PROJECT_STATE.md`; MiniNoetica-era | D11 |

### 1E — Build / config / placeholders

| File | Action | Why |
|---|---|---|
| `.gitignore` | KEEP + extend | add `reference/**/__pycache__`, `/data/episodes/`, coverage. |
| `pytest.ini` | REIMPLEMENT | repoint `testpaths` to `tests/` (Noetica/Velith) + `reference/mininoetica/tests/`; keep the `live` marker. |
| `ARCHITECTURE.md` (0 B) | DELETE | Constitution is the architecture; a stub invites drift (Law 18). |
| `RESEARCH.md` (0 B) | DELETE | research lives in `docs/miniflywire/`. |
| `ROADMAP.md` (0 B) | REIMPLEMENT | author **Noetica Roadmap v1** (from the audit): N0→N1→N2→N3→N4→gated. |

**Coverage check:** all 73 present files above are assigned exactly one action. Nothing is left unclassified.

---

## PHASE 2 — FINAL CANONICAL REPOSITORY STRUCTURE

Directories map **1:1 to Constitution Part VI subsystems** and §9.2 matrix rows. Empty packages are honest placeholders (Law 8 / §13.6) — created now so the boundary and namespace exist, implemented only when a consumer exists.

```
Noetica-agent-lab/                      # the Noetica+Velith monorepo (§11.9)
├── README.md                           # Noetica platform README (reimplemented)
├── ROADMAP.md                          # Noetica Roadmap v1 (N0..N4 + gated)
├── pyproject.toml                      # packaging + import-linter config (NEW)
├── pytest.ini
├── .gitignore
│
├── src/
│   ├── noetica/                        # LAYER 2 — platform. Domain-agnostic. Imports nothing upward.
│   │   ├── interfaces/                 # ALL typed public contracts (designed early, §13.6)
│   │   │   ├── verifier.py  memory.py  knowledge.py  context.py
│   │   │   ├── plan.py  tool.py  skill.py  router.py  budget.py
│   │   │   ├── provenance.py  state.py  guardrail.py  worldmodel.py
│   │   ├── state/                      # §6.1 State Substrate  (THE CORE)
│   │   ├── provenance/                 # §6.2 Provenance & lineage
│   │   ├── runtime/                    # §6.3 Agent runtime & lifecycle
│   │   ├── memory/                     # §6.4 Memory framework + write-filter
│   │   ├── knowledge/                  # §6.5 Knowledge store engine
│   │   ├── context/                    # §6.6 Context assembly
│   │   ├── reasoning/                  # §6.7 Reasoning runtime (form)
│   │   ├── planning/                   # §6.8 Plan representation + executor
│   │   ├── reflection/                 # §6.9 Reflection loop
│   │   ├── evaluation/                 # §6.10 Eval harness + held-out lock
│   │   ├── verification/               # §6.11 Verifier PROTOCOL + Verdict + reference/fake verifier (Law 20)
│   │   ├── tools/                      # §6.12 Tool runtime + interface
│   │   ├── skills/                     # §6.13 Skill runtime + interface
│   │   ├── budget/                     # §6.14 Meta-control / bounded rationality
│   │   ├── router/                     # §6.15 Model abstraction & routing + cost guard
│   │   ├── guardrails/                 # §6.16 Safety policy engine (immutable oversight)
│   │   ├── observability/              # §6.17 Logging / metrics / traces
│   │   ├── sdk/                        # §6.18 Developer surface (Agent/Runtime SDK, public API)
│   │   ├── compute/                    # §6.21 Compute interface & budgeting
│   │   └── datacontracts/              # §4.3 / Law 21 versioned experience contracts + §11.11 lifecycle
│   │
│   └── velith/                         # LAYER 3 — engineering domain. Imports noetica ONLY.
│       ├── task.py                     # EngineeringTask (restored from M1_SPEC)
│       ├── episodes/                   # Episode schema + content hash (impl over noetica store)
│       ├── verifier/                   # SweVerifier — implements noetica.interfaces.Verifier (Law 15)
│       ├── harness/                    # deterministic sandbox (M2 hardening seam)
│       ├── agent/                      # ProposerAgent
│       └── runner/                     # spike orchestrator + CLI (propose→verify→log)
│
├── tests/
│   ├── noetica/                        # platform tests — reference/fake verifier ONLY (Law 20)
│   ├── velith/                         # domain tests (unit + hermetic integration)
│   └── architecture/                   # CONSTITUTION-ENFORCEMENT tests (§11.10)
│       ├── test_import_dag.py          # Law 9/12/19 — no upward/cyclic/sibling imports
│       ├── test_no_reference_import.py # D11 — src/ never imports reference/
│       ├── test_selftest_fake_verifier.py # Law 20
│       ├── test_data_contract_versioned.py # Law 21
│       └── test_docs_code_parity.py    # Law 18
│
├── docs/
│   ├── constitution/                   # HANDBOOK_v1.1.md, v1.0 pdf, ARCHITECTURE_DECISION.md, reviews/
│   ├── decisions/                      # DECISIONS.md (append-only ADR ledger)
│   ├── registry/                       # Primitive Registry (§11.5) — PRIMITIVE_REGISTRY.md
│   ├── vision/                         # VISION.md
│   ├── velith/                         # PROJECT_STATE.md, NOTES.md, milestones/
│   ├── miniflywire/                    # research corpus (MOVE target)
│   └── audits/                         # NOETICA_ARCHITECTURAL_AUDIT_v1.md
│
├── examples/                           # runnable usage examples (added as loop matures)
├── tools/                              # CI/boundary scripts: check_import_dag.py, importlinter contracts
├── configs/                            # runtime + model + budget configs
├── plugins/                            # §6.18 plugin system mount point
└── reference/                          # READ-ONLY, zero-coupling (D11). CI forbids src/→reference imports.
    └── mininoetica/                    # ARCHIVED education code + tests + data + old README/state
```

> The prompt's suggested folders (`runtime, memory, planning, reasoning, verification, provenance, evaluation, router, state, interfaces, …`) are **all present**, placed under `src/noetica/` because the Constitution names them platform subsystems (Part VI). `docs/ tests/ examples/ tools/ configs/ plugins/` sit at repo root as requested.

---

## PHASE 3 — ORDERED MIGRATION PLAN

Every step: **atomic** (one concern), **reversible** (git-tracked; revert = one `git revert`/`git mv` back), **compiles/green** (test suite runs after each step), **history-preserving** (`git mv`, never delete-then-add for moved files). One step per response in Phase 4; I stop and wait after each.

| Step | Title | Changes | Verification | Reversible by |
|---|---|---|---|---|
| **M0** | Reversibility anchor | Clear the stale `.git/index.lock` (sandbox precondition); create tag `pre-noetica-transform` + branch `transform/noetica-canonical`. **No file content changes.** | tag exists; `git status` clean; suite green (baseline) | delete tag/branch |
| **M1** | Scaffold canonical skeleton | Create `src/noetica/<subsystems>/`, `src/velith/`, `tests/{noetica,velith,architecture}/`, `docs/*`, `examples/ tools/ configs/ plugins/ reference/` with `__init__.py`, `.gitkeep`, package `README.md`. **Additive only.** | `python -c "import noetica"` succeeds; existing education tests still green | `git rm` new dirs |
| **M2** | Relocate governance + import Constitution | `git mv` DECISIONS/VISION/PROJECT_STATE/M*_SPEC/NOTES/audit into `docs/`; import Constitution files from session into `docs/constitution/`. Docs only. | links resolve; suite green (no code touched) | `git mv` back |
| **M3** | Relocate MiniFlyWire corpus | `git mv` the science `.md` set → `docs/miniflywire/`. | suite green | `git mv` back |
| **M4** | Archive MiniNoetica code | `git mv` `core/ phase2_memory/ agent_zero/ tests/test_* data/ docs/project_state.md` → `reference/mininoetica/`; update `pytest.ini` testpaths so archived tests still run. | **all education tests still pass from new path** (proves nothing broke) | `git mv` back + revert pytest.ini |
| **M5** | Prune + author top-level docs | DELETE empty placeholders (`02–09_*`, `ARCHITECTURE.md`, `RESEARCH.md`); REIMPLEMENT `README.md` (Noetica) + `ROADMAP.md` (Roadmap v1); create `docs/registry/PRIMITIVE_REGISTRY.md` (§11.5, initially empty-but-declared). | docs render; suite green | tag restores deleted; revert commit |
| **M6** | Install boundary enforcement (CI) | Add `pyproject.toml` + import-linter contracts + `tools/check_import_dag.py` + `tests/architecture/*` (Laws 9/12/18/19/20/21, D11). | architecture tests **pass** (green) and **fail** on an injected violation (proven, then reverted) | `git rm` added files |
| **M7** | Design the interface surface | Add typed `Protocol`/dataclass stubs in `src/noetica/interfaces/` (Verifier, Verdict, MemoryStore, Plan, Tool, Skill, ModelRouter, BudgetMeter, Provenance, State) — **signatures only, no impls** (Law 8/§13.6). | `mypy --strict src/noetica/interfaces` clean; import-DAG green | revert commit |
| **M8** | Restore the Velith spike (N1 consumer) | Re-implement `src/velith/` propose→verify→log from `M1_SPEC` (Ruling 4): Episode+content-hash, thin LLM client, SweVerifier implementing the interface, orchestrator. Cures F1 / Law 18. *(May run as approved sub-steps M8a…M8n, each atomic & green.)* | D16.1 record/replay reproducibility; five verdict states reachable; velith imports noetica only | revert per sub-step |

After M8 the repository is the canonical Noetica platform with one real consumer (Velith), enforced boundaries, and the extraction pipeline (Laws 7/8) ready. Deeper mechanisms (memory write-filter, eval harness, belief state, …) are **extracted later, each gated on a consumer** — not part of this structural transformation (Law 8).

---

## RISKS / PRECONDITIONS (surfaced honestly)

- **Git writability in this sandbox.** A stale `.git/index.lock` is present and could not be removed this session (`Operation not permitted`), and 69 files show uncommitted. **M0 must clear the lock and commit/stash the working tree before anything else**; if the environment blocks git writes, execution pauses there and I report it rather than proceeding non-atomically.
- **Velith source truly gone.** If the absent `src/velith/` tree cannot be recovered from history/another location, M8 rebuilds from `M1_SPEC` (slower but Constitution-clean). Your earlier answer on "restore vs rebuild" feeds this.
- **`reference/` vs a fully separate repo.** I keep MiniNoetica in `reference/` (history-preserving, CI-fenced) rather than forcing you to create a second GitHub repo. It can be split out later with `git filter-repo` if you ever want true physical separation (D11 ideal); not required for compliance given the CI coupling-guard.

---

## APPROVAL GATE

This is the plan only — **nothing has been changed.** On approval I execute **M0 alone**, report (files changed · reason · verification · commit message · progress), and **wait** for your go-ahead before M1. Per Law 22 I may build and recommend but not ratify; you are the approving authority.
