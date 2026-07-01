# NOETICA REPOSITORY TRANSFORMATION PLAN v2 — SCOPE-FROZEN (Noetica only)

**Supersedes:** `NOETICA_TRANSFORMATION_PLAN_v1.md` (kept for history).
**Scope freeze (per owner directive):** transform **only** `Noetica_agent_lab` into the canonical **Noetica** platform. **Velith and Mini Prometheus are out of scope.** Velith is a **separate repository** (confirmed: `E:\Velith`, with its own `.git`, `src/`, `docker/`, `docs/`, `pyproject.toml`). It is treated as **documentation-only / a future downstream dependency** — never recreated, merged, restored, or modified here.
**Authority:** *Engineering Constitution & Architecture Handbook v1.1* (RATIFIED, frozen).
**Constraints:** incremental · history-preserving · reversible · no architecture redesign · no new layers · no fifth project · Law 8 (no speculative mechanisms).

---

## WHAT CHANGED FROM v1 (the delta)

1. **Audit finding F1 retracted.** `src/velith/` is **not absent** — it lives in the standalone `E:\Velith` repo. `PROJECT_STATE.md` was truthful about *its own* repo; the copies inside `Noetica_agent_lab` are accidentally-tangled duplicates (git log: *"Remove accidentally nested project directory"*).
2. **Milestone M8 (restore Velith) is DELETED.** Velith is never built or restored in this repo.
3. **`src/velith/` is removed from the target tree.** The canonical Noetica repo contains **only `src/noetica/`**. Velith consumes Noetica later, from its own repo, via published interfaces (Code Flow, §4.2).
4. **Velith-owned documents now in this repo → ARCHIVED to `reference/velith/`** (documentation-only), not adopted as Noetica governance. Velith already owns the canonical copies. This is the "future dependency, not current work" ruling.
5. **Extraction-from-Velith (Law 8) becomes a future cross-repo activity**, explicitly out of this transformation's scope.

Everything else from v1 (MiniNoetica → `reference/`, MiniFlyWire corpus → `docs/miniflywire/`, canonical `src/noetica/` structure, boundary CI, interface stubs) stands.

---

## REVISED RULINGS

- **R1 Packaging (§11.9).** `Noetica_agent_lab` becomes the **Noetica platform repo** (single layer, Layer 2). It does **not** co-package Velith. The four-layer boundary is still enforced *within* this repo by CI: `src/noetica/` may import nothing domain-specific and nothing from `reference/`.
- **R2 MiniNoetica (D11).** Education code (`core/*`, `phase2_memory/*`, `agent_zero/*`, their tests + `data/`) → **ARCHIVE** to `reference/mininoetica/`, read-only, CI-fenced, never imported. Patterns re-implemented upward later.
- **R3 MiniFlyWire (Part V).** Science corpus → **MOVE** to `docs/miniflywire/` (research docs; consumed by re-implementation only).
- **R4 Velith docs (out of scope).** `DECISIONS.md`, `PROJECT_STATE.md`, `M0/M1/M2` specs + handoffs, `NOTES.md` (all authored `Project: Velith`) → **ARCHIVE** to `reference/velith/` as documentation-only reference for a future dependency. Noetica starts its **own** decision ledger at `docs/decisions/DECISIONS.md`.
- **R5 Constitution.** The ecosystem Handbook is imported into `docs/constitution/` — it governs Noetica directly (P.1). `VISION.md` (ecosystem vision) → `docs/vision/`.
- **R6 No speculative platform (Law 8 / §13.6).** Scaffold the full canonical namespace and design the **interface surface**; implement a mechanism only when a real consumer exists. Empty subsystem packages are honest placeholders.

---

## PHASE 1 (revised) — FILE ACTIONS AFFECTING ONLY THIS REPO

Actions: KEEP · MOVE (`git mv`) · REIMPLEMENT · ARCHIVE (`reference/`, read-only) · DELETE (recoverable via pre-transform tag).

### Noetica-owned (KEEP / import / author)
| File | Action | Destination | Why |
|---|---|---|---|
| Constitution handbook + v1.0 pdf + ARCHITECTURE_DECISION + Gemini review (session uploads) | IMPORT | `docs/constitution/` (+ `reviews/`) | Repo must hold its own authority (P.1). |
| `VISION.md` | MOVE | `docs/vision/VISION.md` | Ecosystem vision, governs Noetica (Authority #3). |
| `NOETICA_ARCHITECTURAL_AUDIT_v1.md`, `NOETICA_TRANSFORMATION_PLAN_v1.md`, this v2 | MOVE | `docs/audits/`, `docs/transformation/` | Noetica deliverables. |
| `README.md` (education) | REIMPLEMENT | new Noetica `README.md`; old → `reference/mininoetica/` | Platform README (Law 18 parity). |
| `ROADMAP.md` (0 B) | REIMPLEMENT | `ROADMAP.md` | Author Noetica Roadmap v1 (N0→N4 + gated). |
| new | AUTHOR | `docs/decisions/DECISIONS.md` | Noetica's own ADR ledger (transformation decisions). |
| new | AUTHOR | `docs/registry/PRIMITIVE_REGISTRY.md` | Primitive Registry (§11.5), declared-empty. |
| `.gitignore` | KEEP+extend | — | add caches, `/data/`, coverage. |
| `pytest.ini` | REIMPLEMENT | — | repoint testpaths (noetica, architecture, archived tests). |

### MiniFlyWire → `docs/miniflywire/` (MOVE)
`research_problem.md`, `ontology.md`, `computational_theory.md`, `computational_mechanisms.md`, `engineering_cognition_synthesis.md`, `00_project_definition.md`, `00_research_axioms.md`, `00_research_vision.md`, `00_research_vision_v2_draft.md`, `01_cognitive_ontology.md`, `01_core_question.md`, `10_research_notebook.md`, `idea_backlog.md`. — Empty `02_…09_*.md` (8×0 B) → **DELETE**.

### MiniNoetica → `reference/mininoetica/` (ARCHIVE, D11)
`core/agent.py`, `core/llm.py`, `core/logger.py`, all `phase2_memory/*`, all `agent_zero/step*`, all `tests/test_*`+`tests/__init__.py`, `data/agent_runs.jsonl`, `docs/project_state.md` (education-era). `judge.py` archived **fenced/non-promotable** (Law 7).

### Velith docs → `reference/velith/` (ARCHIVE, documentation-only — R4)
`DECISIONS.md`, `PROJECT_STATE.md`, `M0_SPEC.md`, `M1_SPEC.md`, `M1_IMPLEMENTATION_HANDOFF.md`, `M2_SPEC.md`, `M2_IMPLEMENTATION_HANDOFF.md`, `NOTES.md`.

### DELETE (empty/superseded; tag-recoverable)
`ARCHITECTURE.md`, `RESEARCH.md` (0 B), `02_…09_*.md` (0 B).

*All 73 present files assigned exactly one action.*

---

## PHASE 2 (revised) — CANONICAL TREE (Noetica only; no `src/velith/`)

```
Noetica_agent_lab/
├── README.md  ROADMAP.md  pyproject.toml  pytest.ini  .gitignore
├── src/noetica/                 # LAYER 2 ONLY — domain-agnostic, imports nothing upward/domain/reference
│   ├── interfaces/              # typed public contracts (designed early)
│   ├── state/ provenance/ runtime/ memory/ knowledge/ context/
│   ├── reasoning/ planning/ reflection/ evaluation/ verification/
│   ├── tools/ skills/ budget/ router/ guardrails/ observability/
│   ├── sdk/ compute/ datacontracts/
├── tests/
│   ├── noetica/                 # reference/fake verifier only (Law 20)
│   └── architecture/            # import-DAG, no-reference-import, fake-verifier, data-contract, parity (§11.10)
├── docs/
│   ├── constitution/ decisions/ registry/ vision/
│   ├── miniflywire/ audits/ transformation/
├── examples/  tools/  configs/  plugins/
└── reference/                   # READ-ONLY, zero-coupling (CI forbids src/→reference)
    ├── mininoetica/             # archived education code + tests + data
    └── velith/                  # archived Velith docs (future dependency; documentation only)
```

Velith (Layer 3) lives in **its own repo** and will `import noetica` via published interfaces — a **future dependency**, no work here.

---

## PHASE 3 (revised) — MIGRATION STEPS (each atomic · reversible · green · Noetica-only)

| Step | Title | Effect | Verification |
|---|---|---|---|
| **M0** | Reversibility anchor | clear stale `.git/index.lock`; tag `pre-noetica-transform`; branch `transform/noetica-canonical`. No content change. | tag+branch exist; baseline recorded |
| **M1** | Scaffold `src/noetica/` skeleton + tests/docs/examples/tools/configs/plugins/reference dirs | additive only | `import noetica` works; nothing else touched |
| **M2** | Import Constitution; relocate Noetica docs (VISION, audit, plans) | docs only | links resolve |
| **M3** | Move MiniFlyWire corpus → `docs/miniflywire/` | `git mv` | tree clean |
| **M4** | Archive MiniNoetica code+tests+data → `reference/mininoetica/`; repoint `pytest.ini` | `git mv` | archived tests still pass from new path |
| **M5** | Archive Velith docs → `reference/velith/` | `git mv` | tree clean |
| **M6** | Prune empties; author Noetica `README`, `ROADMAP`, `docs/decisions/DECISIONS.md`, `docs/registry/` | delete+author | docs render |
| **M7** | Boundary-enforcement CI: `pyproject.toml`+import-linter+`tools/`+`tests/architecture/*` | add | architecture tests pass; fail on injected violation then revert |
| **M8** | Interface surface: typed `Protocol` stubs in `src/noetica/interfaces/` (signatures only, Law 8) | add | `mypy --strict` clean; DAG green |

Post-M8: canonical Noetica platform with enforced boundaries and a designed interface surface. Mechanism *implementations* are added later, each gated on a real consumer (extraction, Law 8) — future work, out of this scope.

---

## APPROVAL / EXECUTION

Per owner directive I now **execute M0**, report, and **wait**. One step per turn thereafter. Law 22: I build and recommend; you ratify.
