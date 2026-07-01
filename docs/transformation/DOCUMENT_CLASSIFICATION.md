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
