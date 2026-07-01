# DOCUMENT CLASSIFICATION — Permanent Migration Record

**Purpose.** The permanent, append-only historical record of every documentation
migration performed while transforming `Noetica_agent_lab` into the canonical Noetica
platform (Transformation Plan v2). One row per document. Never rewritten; each
milestone appends a new section.

**Legend.** *Owner* = the layer/authority that owns the document per the Constitution.
*Constitution Reference* = the section/law justifying its placement. *Git Commit* =
the commit in which the migration landed on branch `transform/noetica-canonical`.

Operation key: **MOVE** = history-preserving rename (git `R100`) · **IMPORT** = copied
into the repo from an external session source (new file) · **ARCHIVE** = relocated
read-only to `reference/` (later milestones).

---

## M2 — Relocate Noetica-owned docs + import Constitution — commit `e27bab4`

| # | Op | Original Path | New Path | Owner | Constitution Reference | Reason | Git Commit |
|---|----|---------------|----------|-------|------------------------|--------|-----------|
| 1 | MOVE | `VISION.md` | `docs/vision/VISION.md` | Ecosystem (governs Noetica) | P.2 (Authority #3); Appendix B | Ecosystem vision (the why / toward-what); belongs in canonical `docs/vision/`, not repo root. | `e27bab4` |
| 2 | MOVE | `NOETICA_ARCHITECTURAL_AUDIT_v1.md` | `docs/audits/NOETICA_ARCHITECTURAL_AUDIT_v1.md` | Noetica | §11.2 (architecture review); §13.8 | Architectural audit deliverable; canonical home is `docs/audits/`. | `e27bab4` |
| 3 | MOVE | `NOETICA_TRANSFORMATION_PLAN_v1.md` | `docs/transformation/NOETICA_TRANSFORMATION_PLAN_v1.md` | Noetica | Part XII (implementation workflow) | Superseded plan; retained as history. | `e27bab4` |
| 4 | MOVE | `NOETICA_TRANSFORMATION_PLAN_v2.md` | `docs/transformation/NOETICA_TRANSFORMATION_PLAN_v2.md` | Noetica | Part XII (implementation workflow) | Active (scope-frozen) plan governing this work. | `e27bab4` |
| 5 | IMPORT | *(session upload)* `ENGINEERING_CONSTITUTION_AND_ARCHITECTURE_HANDBOOK.md` | `docs/constitution/HANDBOOK_v1.1.md` | Ecosystem / Constitutional Architect | P.1; Law 23 | The repo must physically hold its own highest authority (RATIFIED Handbook v1.1). | `e27bab4` |
| 6 | IMPORT | *(session upload)* `ARCHITECTURE_CONSTITUTION_v1.0.pdf` | `docs/constitution/ARCHITECTURE_CONSTITUTION_v1.0.pdf` | Ecosystem | Appendix B; Part X | Frozen v1.0 source of the four-layer model and the eleven canonical laws. | `e27bab4` |
| 7 | IMPORT | *(session upload)* `ARCHITECTURE_DECISION.md` | `docs/constitution/ARCHITECTURE_DECISION.md` | Ecosystem / Noetica | Appendix B; N.3 | First-principles architecture review absorbed by the Handbook; kept for provenance. | `e27bab4` |
| 8 | IMPORT | *(session upload)* `Gemini_Review.txt` | `docs/constitution/reviews/Gemini_Review.txt` | Ecosystem | §11.6 (item 11, independent review) | Independent architecture review used at ratification; amendment provenance. | `e27bab4` |

**Housekeeping in `e27bab4` (not documents):** 5 placeholder `.gitkeep` removed from
directories that now hold real docs (`docs/vision/`, `docs/audits/`,
`docs/transformation/`, `docs/constitution/`, `docs/constitution/reviews/`).

**Integrity note:** during M2 the git index on the FUSE mount corrupted mid-operation
("bad signature"); it was rebuilt from HEAD with no working-tree or object-store loss,
and all four moves were re-verified as `R100` renames before commit.

---

*Future milestones (M3 MiniFlyWire corpus -> `docs/miniflywire/`; M5 Velith docs ->
`reference/velith/`) append their own sections below when executed.*

---

## M3 — Archive MiniFlyWire research corpus to reference/miniflywire — commit `62d7af5`

> **Ownership ruling:** these are **reference / synchronized copies**. Canonical owner
> remains **MiniFlyWire** (§11.9). Noetica never owns this research; no implementation
> may import `reference/miniflywire`; promotion only by validated re-implementation
> (§4.1 Knowledge Flow, Law 4, Law 7). See `reference/miniflywire/README.md`.

| # | Op | Original Path | New Path | Owner | Constitution Reference | Reason | Git Commit |
|---|----|---------------|----------|-------|------------------------|--------|-----------|
| 9  | ARCHIVE (ref) | `research_problem.md` | `reference/miniflywire/research_problem.md` | MiniFlyWire | §4.1; Law 4; Law 7; §11.9; §9.2 | Research corpus; owner MiniFlyWire; held as reference for re-implementation. | `62d7af5` |
| 10 | ARCHIVE (ref) | `ontology.md` | `reference/miniflywire/ontology.md` | MiniFlyWire | §4.1; Law 4; §9.2 | Cognitive ontology (computational objects/operators). | `62d7af5` |
| 11 | ARCHIVE (ref) | `computational_theory.md` | `reference/miniflywire/computational_theory.md` | MiniFlyWire | §1.6; §4.1; §9.2 | Three domains / five functions / five laws. | `62d7af5` |
| 12 | ARCHIVE (ref) | `computational_mechanisms.md` | `reference/miniflywire/computational_mechanisms.md` | MiniFlyWire | §4.1; §9.2 | Mechanism notes. | `62d7af5` |
| 13 | ARCHIVE (ref) | `engineering_cognition_synthesis.md` | `reference/miniflywire/engineering_cognition_synthesis.md` | MiniFlyWire | §4.1; §7.2 | Engineering-as-cognition synthesis (H3). | `62d7af5` |
| 14 | ARCHIVE (ref) | `00_project_definition.md` | `reference/miniflywire/00_project_definition.md` | MiniFlyWire | §4.1; Appendix B | Research framing. | `62d7af5` |
| 15 | ARCHIVE (ref) | `00_research_axioms.md` | `reference/miniflywire/00_research_axioms.md` | MiniFlyWire | Part V; Appendix B | Candidate axioms / evaluation framework. | `62d7af5` |
| 16 | ARCHIVE (ref) | `00_research_vision.md` | `reference/miniflywire/00_research_vision.md` | MiniFlyWire | §4.1; Appendix B | Research vision. | `62d7af5` |
| 17 | ARCHIVE (ref) | `00_research_vision_v2_draft.md` | `reference/miniflywire/00_research_vision_v2_draft.md` | MiniFlyWire | §4.1; Appendix B | Research vision (draft v2). | `62d7af5` |
| 18 | ARCHIVE (ref) | `01_cognitive_ontology.md` | `reference/miniflywire/01_cognitive_ontology.md` | MiniFlyWire | §1.6; Part V | Cognitive ontology (early). | `62d7af5` |
| 19 | ARCHIVE (ref) | `01_core_question.md` | `reference/miniflywire/01_core_question.md` | MiniFlyWire | Part V | Core research question. | `62d7af5` |
| 20 | ARCHIVE (ref) | `10_research_notebook.md` | `reference/miniflywire/10_research_notebook.md` | MiniFlyWire | Part V; Appendix D | Laboratory notebook (H1–H31, R1–R7). | `62d7af5` |
| 21 | ARCHIVE (ref) | `idea_backlog.md` | `reference/miniflywire/idea_backlog.md` | MiniFlyWire | Part V | Research idea backlog. | `62d7af5` |
| 22 | ADD | *(new)* | `reference/miniflywire/README.md` | Noetica (about MiniFlyWire) | §4.1; Law 4; Law 7; §11.9 | Ownership + no-import + promotion-by-re-implementation declaration. | `62d7af5` |

**Deletions in `62d7af5` (not documents):** 8 empty research stubs `02_hypotheses.md`…`09_decisions.md`; stray diagnostic artifact `_rentest2`; unused `docs/miniflywire/.gitkeep` scaffold (superseded by `reference/miniflywire/`).

---

## M3.5 Task 1 — Archive MiniNoetica legacy code to reference/mininoetica — commit `918f4b0`

> **Ownership:** canonical owner **MiniNoetica** (D11). Reference/read-only; Noetica
> never owns or imports; promotion only by validated re-implementation. LLM-as-judge
> (`judge.py`) permanently barred from promotion (Law 7). See `reference/mininoetica/README.md`.

| # | Op | Original Path | New Path | Owner | Constitution Reference | Reason | Git Commit |
|---|----|---------------|----------|-------|------------------------|--------|-----------|
| 23 | ARCHIVE (ref) | `core/` (agent.py, llm.py, logger.py) | `reference/mininoetica/core/` | MiniNoetica | D11; Law 3/4/9 | Education Agent-Zero loop + adapters; seeds re-implemented upward only. | `918f4b0` |
| 24 | ARCHIVE (ref) | `phase2_memory/` (10 modules) | `reference/mininoetica/phase2_memory/` | MiniNoetica | D11; Law 5; Law 7 | Student-modeling memory; `judge.py` = barred anti-pattern. | `918f4b0` |
| 25 | ARCHIVE (ref) | `agent_zero/` (step1–9) | `reference/mininoetica/agent_zero/` | MiniNoetica | D11; Law 4 | Learning-archive probe scripts. | `918f4b0` |
| 26 | ARCHIVE (ref) | `tests/test_*.py`, `tests/__init__.py` | `reference/mininoetica/tests/` | MiniNoetica | D11; §11.9 | Education tests; excluded from platform suite. | `918f4b0` |
| 27 | ARCHIVE (ref) | `data/agent_runs.jsonl` | `reference/mininoetica/data/agent_runs.jsonl` | MiniNoetica | D11; Law 21 | Education run logs (unversioned). | `918f4b0` |
| 28 | ARCHIVE (ref) | `docs/project_state.md` | `reference/mininoetica/docs/project_state.md` | MiniNoetica | D11; Amendment A1 | Education-era state; other-layer doc out of Noetica `docs/`. | `918f4b0` |
| 29 | ADD | *(new)* | `reference/mininoetica/README.md` | Noetica (about MiniNoetica) | D11; §4.1; Law 4/7 | Ownership + no-import + promotion-by-re-implementation declaration. | `918f4b0` |
| 30 | MODIFY | `pytest.ini` | `pytest.ini` | Noetica | §11.9; Law 4/9 | testpaths=tests; norecursedirs=reference (reference not executable platform code). | `918f4b0` |

---

## M3.5 Task 2 — CI Boundary Enforcement (enforcement tooling, not migrations)

New files (constitutional enforcement per §11.10 — NOT platform mechanisms):

| Op | Path | Purpose | Constitution Reference |
|----|------|---------|------------------------|
| ADD | `tools/check_boundaries.py` | Static import/packaging checks; fail-closed (exit 1) on violation. | Law 4/9/12; §11.10; D11 |
| ADD | `tests/architecture/test_constitution_boundaries.py` | Pytest wrappers so the suite fails on any boundary violation. | §11.10 |
| ADD | `.github/workflows/constitution.yml` | CI gate: runs the checker + architecture tests on push/PR. | §11.9/§11.10 |
| ADD | `tools/README.md` | Declares these are enforcement, not platform features. | §11.10 |

Enforced: (1) `src/noetica` imports nothing from `reference/`; (2) no legacy/domain
import (`core`, `phase2_memory`, `agent_zero`, `velith`, `mini_prometheus`); (3) package
DAG holds (platform + platform tests never import reference); (4) `reference/` is
excluded from the pytest suite (reference is not executable platform code). Verified
fail-closed against injected violations.

---

## M5 — Archive Velith-owned documentation to reference/velith — commit `068e63c`

> **Ownership:** canonical owner **Velith** (separate repository, Layer 3). Reference
> copies only; Noetica never owns or imports; mechanisms enter Noetica by extraction
> (Law 8, N.3), never by import. See `reference/velith/README.md`.

| # | Op | Original Path | New Path | Owner | Constitution Reference | Reason | Git Commit |
|---|----|---------------|----------|-------|------------------------|--------|-----------|
| 31 | ARCHIVE (ref) | `DECISIONS.md` (D1–D21) | `reference/velith/DECISIONS.md` | Velith | §2.3; N.3; §4.2 | Velith ADR ledger; mechanisms extracted to Noetica, not imported. | `068e63c` |
| 32 | ARCHIVE (ref) | `PROJECT_STATE.md` | `reference/velith/PROJECT_STATE.md` | Velith | §2.3; §13.7 | Velith milestone state. | `068e63c` |
| 33 | ARCHIVE (ref) | `M0_SPEC.md` | `reference/velith/M0_SPEC.md` | Velith | §2.3; §13.7 | Velith M0 spec. | `068e63c` |
| 34 | ARCHIVE (ref) | `M1_SPEC.md` | `reference/velith/M1_SPEC.md` | Velith | §2.3; §7.5 | Velith M1 spec (propose->verify->log). | `068e63c` |
| 35 | ARCHIVE (ref) | `M1_IMPLEMENTATION_HANDOFF.md` | `reference/velith/M1_IMPLEMENTATION_HANDOFF.md` | Velith | §2.3 | Velith M1 handoff. | `068e63c` |
| 36 | ARCHIVE (ref) | `M2_SPEC.md` | `reference/velith/M2_SPEC.md` | Velith | §2.3 | Velith M2 spec (hardened verifier). | `068e63c` |
| 37 | ARCHIVE (ref) | `M2_IMPLEMENTATION_HANDOFF.md` | `reference/velith/M2_IMPLEMENTATION_HANDOFF.md` | Velith | §2.3 | Velith M2 handoff. | `068e63c` |
| 38 | ARCHIVE (ref) | `NOTES.md` | `reference/velith/NOTES.md` | Velith | §2.3; §13.4 | Velith M2 capability-gating notes. | `068e63c` |
| 39 | ADD | *(new)* | `reference/velith/README.md` | Noetica (about Velith) | §4.2; Law 8; Amendment A1 | Ownership + no-import + extraction-only declaration. | `068e63c` |
