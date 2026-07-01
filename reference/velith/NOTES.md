Phase 0: Development environment ready (Git, WSL2, Docker, Ollama)

## M2-C2 — verifier network-isolation capability (CAP_SYS_ADMIN)

The verifier isolates the Phase-2 hidden-test step from the network with `unshare -n`
(M2_SPEC §10, D19 / Fallback B), granted via `cap_add: [SYS_ADMIN]` in
`docker-compose.yml`. The R3 feasibility prototype confirmed unprivileged `unshare -rn`
is blocked by the Docker Desktop / WSL2 seccomp profile, so the capability is mandatory.

Capability-gating is permanent and honest: isolation-dependent tests **run** where
CAP_SYS_ADMIN is present and **skip-with-reason** where it is not — never silently
passed. The verifier refuses to run untrusted code unisolated: if isolation is required
but the capability is absent, `verify` raises `SandboxExecutionError` (→ `INFRA_ERROR`).

Environment support — record for future contributors:

- Local Docker Desktop / WSL2: **SUPPORTED** (R3 prototype, Fallback B passed).
- GitHub Actions CI: **TO BE CONFIRMED from the first M2-C2 CI run.** Inspect the CI log
  for `tests/unit/test_verifier_sandbox.py::test_phase2_blocks_network_egress`: if it
  RUNS, CI grants CAP_SYS_ADMIN; if it is SKIPPED with the capability reason, CI does
  not (isolation is then a documented local-acceptance gate). Update this line with the
  observed result after the run.
