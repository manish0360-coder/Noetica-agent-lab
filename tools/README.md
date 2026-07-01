# tools/ — Constitutional Enforcement (not platform features)

Scripts here **mechanically enforce the Constitution** (§11.10). They are enforcement
tooling, never platform mechanisms — they contain no runtime, memory, planner, router,
or any Noetica capability.

- `check_boundaries.py` — static import + packaging checks. Fails (exit 1) if the
  platform (`src/noetica`, `tests/`) imports `reference/`, MiniNoetica legacy
  (`core`, `phase2_memory`, `agent_zero`), or a domain layer (`velith`,
  `mini_prometheus`); or if `reference/` is not excluded from the pytest suite.
  Enforces Law 4, Law 9, D11, §11.9.

Run locally: `python tools/check_boundaries.py`. Run in CI via
`.github/workflows/constitution.yml` (plus `pytest tests/architecture`).
