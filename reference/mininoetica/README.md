# reference/mininoetica — MiniNoetica Education Code (Reference, Read-Only)

> **Canonical owner: MiniNoetica** (a separate, completed education project).
> Noetica does **not** own this code and never imports it.

## What this directory is

The archived **MiniNoetica** codebase: an education / learning-intelligence system (a
fractions tutor that models a *student's* knowledge). It is a **completed, read-only
reference** kept for its reusable engineering *patterns*, not its domain. It is not
part of the Noetica platform and is never on the platform import path.

Contents: `core/` (Agent-Zero JSON loop, Ollama adapter, JSONL logger),
`phase2_memory/` (student `KnowledgeState`, `forgetting`, `concepts`, `verdict`,
`judge`, `memory_agent`), `agent_zero/` (probe scripts), `tests/` (education tests),
`data/` (education run logs), `docs/` (education-era project state).

## Ownership and boundary rules (from the Constitution)

- **Canonical owner: MiniNoetica.** A separate, completed reference project — *"not a
  dependency, not to be extended"* (**`DECISIONS.md` D11**). Ownership does not transfer
  to Noetica by these files living in the repo.
- **Noetica never owns this code and no implementation may import
  `reference/mininoetica`.** *"If a Velith/Noetica file ever imports from MiniNoetica,
  the boundary has been crossed and must be reverted"* (**D11**; **Law 4** — research /
  reference is never imported; **Law 9** — strict dependency DAG). A CI boundary check
  (`tools/check_boundaries.py`) fails the build on any `src/ -> reference/` import.
- **Promotion happens only through validated re-implementation**, never by import or
  copy (**§4.1 Knowledge Flow**, **Law 7**). Patterns are *re-typed* cleanly into
  `src/noetica/` behind interfaces, with provenance from the first commit.
- **The LLM-as-judge anti-pattern stays here and is permanently barred from promotion.**
  `phase2_memory/judge.py` is the exact anti-pattern deterministic verification exists
  to eliminate (**D3, D11, Law 7**). It may be studied as a negative result; it may
  never enter `src/noetica/`.

## Promotable seeds (by re-implementation only)

`verdict.py` (construction-validated `Verdict`) → seeds `noetica/verification`;
`core/llm.py` (single-owner model call) → seeds `noetica/router` (D16.4);
`core/logger.py` (episode→JSONL) → seeds `noetica/observability`;
`forgetting.py` / `knowledge_state.py` → **MiniFlyWire** promotion candidates
re-implemented into `noetica/memory` from a validated spec.

## Constitution references

- **`DECISIONS.md` D11** — MiniNoetica is a separate, completed, read-only reference
- **§4.1 — Knowledge Flow** (transfer by re-implementation, never import)
- **Law 4 / Law 7** — reference never imported; promotion requires re-implementation
- **Law 3 / Law 5** — mechanism vs content; no domain/education content in the platform
- **Law 9 / §11.9** — strict dependency DAG; reference is not a package dependency

*Read-only. Not executable platform code. Excluded from the platform test suite
(`pytest.ini norecursedirs`).*
