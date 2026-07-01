# M2 — Implementation Handoff

**Project:** Velith
**Milestone:** M2 — Deterministic, hardened verifier
**Audience:** The implementation team executing M2.
**Authority:** Execution contract. Subordinate to, and must not contradict, the immutable contracts:
`VISION.md`, `DECISIONS.md` (D1–D21), the M0/M1 specifications, and the **frozen** `M2_SPEC.md`. Where this
document and a frozen contract appear to differ, the frozen contract wins and the discrepancy is raised,
not silently resolved.
**Status:** Authorized against frozen `M2_SPEC.md` (R1–R5 / D17–D21). Ratified mechanism: Fallback B
(`cap_add: SYS_ADMIN` + `unshare -n`).
**Preconditions:** M1 complete, merged, tagged `m1-complete`, all gates green. M0/M1 application logic is
frozen and must not change except the M2-permitted files (§4).

---

## 1. Objective

**What M2 accomplishes.** It hardens the single `VerifierSandbox.verify` seam so the verdict is
trustworthy as the program's exact ground truth: a **two-phase** execution (Phase 1 network ON for prep,
Phase 2 network OFF for tests via `unshare -n` under `CAP_SYS_ADMIN`), a **pinned environment** reaching
**Determinism Level 4**, **flake detection** recording a provenance `flaky` flag, and a populated
**held-out secondary** model-gap signal (`secondary_passed`).

**What M2 does NOT accomplish.** No proposer, LLM-client, or store changes; no episode/orchestrator change
beyond the sanctioned `flaky` field + one-line passthrough; no new `FLAKY` verdict; `flaky` never enters
the content hash; no property-based testing, resource profiling, streaming, richer prompts, or git
provenance (R4); no memory/arms/dataset/indexing (M3–M7).

---

## 2. Engineering philosophy — inherited invariants (non-negotiable)

1. **The verdict is produced inside the container** (D3, M0 §2). M2 strengthens this to a pinned,
   network-isolated Phase 2.
2. **No model judges correctness — ever** (D3). M2 adds no model anywhere in `verify`.
3. **Outcome vs. error is sacred** (D16.7/D2). The five-state taxonomy is unchanged (R1/D17); a flaky
   primary is *not* an error — it is a nominal verdict with `flaky=True`. Missing isolation capability
   *is* an infra error (`SandboxExecutionError → INFRA_ERROR`); untrusted code is never run unisolated.
4. **Provenance is conserved** (I2). `flaky` is persisted as provenance (R5/D21), **excluded from the
   content hash**; `secondary_passed` is identity, **inside** the hash.
5. **Determinism lives in the verifier** (R2/D18). M2 targets **Level 4** (pinned environment).
6. **Hardening, not rewrite** (RK8). Changes confined to `verifier_sandbox.py`, `task.py`, `config.py`,
   the fixture, tests, `docker-compose.yml`, and the minimal `episode.py`/`spike.py` `flaky` touch.
7. **Strict gates from the first commit** — `ruff`, `ruff format`, `mypy --strict`, `pytest`, all green in
   the container; CI hermetic (isolation tests capability-gated, never silently passed).
8. **Anti-wireheading** (ratified, §9): the held-out secondary is re-materialized from the pristine
   fixture **after** patch application.

---

## 3. Dependency graph (M2 deltas)

```
core/config (extended)         used by: verifier_sandbox
task (extended: secondary_test_command)   used by: verifier_sandbox (+ loader)
verifier_sandbox (hardened)    depends on: task, config, episodes.episode (VerdictState), core/logging
                               produces:   Verdict(state, output, secondary_passed, flaky, duration)
episodes/episode (flaky field, excluded from hash)   used by: store, runner/spike (unchanged store)
runner/spike (one-line flaky passthrough)   depends on: all (unchanged otherwise)
docker-compose (cap_add SYS_ADMIN)   enables: unshare -n in verifier
fixtures/calc_add_bug (secondary + flaky test files)   consumed by: verifier_sandbox at verify time
```

The orchestrator already maps `secondary_passed` (C7). `flaky` adds one mapping line. No other module's
order-of-operations changes.

### Implementation order (leaves/low-risk first, isolation isolated, semantics last)

1. **M2-C1** pinned deterministic environment (config + verify env injection) — no capability, lowest risk.
2. **M2-C2** two-phase network isolation (`cap_add` + `unshare -n`) — the RM-CI/RM5 commit, prototype-proven.
3. **M2-C3** flake detection + provenance (`Verdict.flaky`, N-rerun loop, `Episode.flaky` excluded-from-hash,
   `spike` passthrough).
4. **M2-C4** held-out secondary + `secondary_passed` (the most semantically complex; anti-wireheading).
5. **M2-C5** docs.

---

## 4. Permitted modifications (exhaustive)

`harness/verifier_sandbox.py`, `task.py`, `core/config.py`, `docker-compose.yml`,
`episodes/episode.py` (only the `flaky` field + hash-exclusion), `runner/spike.py` (only the `flaky`
passthrough), `tests/unit/test_verifier_sandbox.py`, `tests/unit/test_episode.py`,
`tests/fixtures/calc_add_bug/*` (new secondary + flaky files), `README.md`. Optionally
`docker/verifier.Dockerfile` only if `unshare` proves absent (it is present). **Anything else is a
boundary violation.**

---

## 5. Commit plan (atomic; each leaves the gates green)

### Pre-C2 — CI capability check (not a commit; a gate decision)
Before M2-C2, confirm whether the CI runner permits `cap_add: SYS_ADMIN` (run a one-off `unshare -n`
probe in CI). Record the result. If unsupported, the isolation-dependent tests are capability-skipped in
CI (with an explicit reason) and isolation becomes a documented local-acceptance gate (like the M1 live
run). This decision is recorded before C2 lands.

### M2-C1 — `feat: pinned deterministic execution environment`
- **Scope:** `core/config.py` (determinism env settings; flake-rerun count placeholder), `verifier_sandbox.py`
  (inject `PYTHONHASHSEED=0`, `TZ=UTC`, `LC_ALL=C`, `PYTHONDONTWRITEBYTECODE=1` into the test subprocess
  env), `tests/unit/test_verifier_sandbox.py` (determinism test: same patch → identical normalized output).
- **Verification:** four gates; a determinism test asserts repeated `verify` of a fixed patch yields
  identical `Verdict.output`/state. No capability needed.
- **DoD:** pinned env injected; Level-1/3 stability for a fixed patch demonstrated.
- **Rollback:** non-deterministic output remains; env not applied to the test subprocess.

### M2-C2 — `feat: two-phase network-isolated test execution`
- **Scope:** `docker-compose.yml` (`cap_add: [SYS_ADMIN]`), `verifier_sandbox.py` (Phase 1 prep / Phase 2
  wrap the test command in `unshare -n`; raise `SandboxExecutionError` if isolation required but
  unavailable), `core/config.py` (isolation toggle, default ON), `tests/unit/test_verifier_sandbox.py`
  (no-egress control test, capability-gated/skip-with-reason).
- **Verification:** four gates; the Phase-2 process cannot open an outbound socket; the container without
  `unshare` retains network (Phase 1); missing-capability-with-isolation-ON raises.
- **DoD:** Phase-2 egress blocked under `CAP_SYS_ADMIN`; never runs untrusted code unisolated.
- **Rollback:** egress reachable in Phase 2; silent fallback to unisolated execution; isolation test
  silently passes where the capability is absent.

### M2-C3 — `feat: flake detection and provenance`
- **Scope:** `verifier_sandbox.py` (`Verdict.flaky`; run primary N times; reconcile; loud log on
  divergence), `core/config.py` (`flake_rerun_count`, default ≥3), `episodes/episode.py` (add `flaky`
  field default `False`; add to `HASH_EXCLUDED_FIELDS`), `runner/spike.py` (one-line
  `flaky=verdict.flaky`), `tests/fixtures/calc_add_bug/<flaky test>`, `tests/unit/test_verifier_sandbox.py`
  (flaky fixture → `flaky=True`; deterministic → `flaky=False`), `tests/unit/test_episode.py` (varying
  `flaky` leaves `content_hash` unchanged).
- **Verification:** four gates; flake detection works both ways; **R5 hash-exclusion test passes**.
- **DoD:** flakiness detected, recorded as provenance, excluded from the hash; no `FLAKY` state.
- **Rollback:** `flaky` enters the hash (breaks Level 2); a flaky run logged silently as clean; a new
  verdict state introduced.

### M2-C4 — `feat: held-out secondary suite and model-gap signal`
- **Scope:** `task.py` (`secondary_test_command`, default empty; loader populates it for the fixture),
  `tests/fixtures/calc_add_bug/<secondary suite>`, `verifier_sandbox.py` (after a primary PASSED/FAILED,
  re-materialize the secondary from the pristine fixture, run it isolated+pinned, set
  `Verdict.secondary_passed`), `tests/unit/test_verifier_sandbox.py` (model-gap test: a primary-passing
  but secondary-failing patch → `secondary_passed=False`; the secondary cannot be tampered by the patch).
- **Verification:** four gates; `secondary_passed` populated correctly; anti-wireheading proven (a patch
  that edits the secondary file does not change the held-out result); `secondary_passed` is inside the
  content hash.
- **DoD:** model-gap signal reachable and recorded; held-out integrity guaranteed.
- **Rollback:** the patch can tamper with the secondary; `secondary_passed` not populated; secondary shown
  to the proposer (it must not be — proposer reads nothing, so this is structurally satisfied).

### M2-C5 — `docs: M2 hardened-verifier usage`
- **Scope:** `README.md` — two-phase isolation, `CAP_SYS_ADMIN` requirement, Determinism Level 4,
  `flaky` provenance, `secondary_passed`/model-gap.
- **Verification:** four gates; a reader can understand and reproduce M2 behavior from the README.
- **Rollback:** README omits the `CAP_SYS_ADMIN` requirement or the isolation/flake/secondary behavior.

---

## 6. Verification gates (per commit)

After **every** commit, the four M0 gates in the container plus the commit-specific check:
- `docker compose run --rm --build verifier ruff check .`
- `docker compose run --rm verifier ruff format --check .`
- `docker compose run --rm verifier mypy src tests`
- `docker compose run --rm verifier pytest -q`
Failure = any non-green output. **From C2 on, `pytest` runs under the `cap_add: SYS_ADMIN` compose, so the
isolation tests execute where the capability is granted and skip-with-reason otherwise — never silent pass.**

---

## 7. Integration order

- **Checkpoint A (after C1):** pinned environment proven via the determinism test — no capability yet.
- **Checkpoint B (after C2):** isolation proven (no Phase-2 egress) under `CAP_SYS_ADMIN`; the
  mandatory-isolation raise-path verified. This is the highest-risk checkpoint (RM-CI/RM5); it is isolated
  in its own commit so a failure is contained.
- **Checkpoint C (after C3–C4):** flake provenance and the held-out secondary wired into the now-pinned,
  isolated execution; the D16.1/Level-2 hash reproducibility (with `flaky` excluded) re-verified.
- Re-run M1's live acceptance once (real Ollama) after C4 to confirm the hardened verifier still produces
  and logs a real verdict end to end.

---

## 8. Risk register

| ID | Risk | Mitigation |
|---|---|---|
| RM-CI | CI cannot grant `cap_add: SYS_ADMIN`. | Pre-C2 capability check; capability-skip isolation tests in CI with explicit reason (never silent pass); isolation as local-acceptance gate if needed. |
| RM2 | Residual nondeterminism breaks Level 4. | Pin env; assert Level 2/3; retain M1 normalization. |
| RM3 | Patch tampers with the held-out secondary. | Re-materialize from the pristine fixture after patch apply (C4). |
| RM4 | `flaky` hashed → breaks Level 2. | `HASH_EXCLUDED_FIELDS` + the C3 `test_episode` assertion. |
| RM5 | `CAP_SYS_ADMIN` over-broadens privilege. | Verifier container only; documented; minimal `unshare -n` use. |
| RM6 | Drift beyond the permitted files (RK8). | §4 exhaustive list; reviewer rejects out-of-scope edits. |
| RM7 | Silent unisolated execution if `unshare` fails. | Mandatory-isolation invariant: raise `SandboxExecutionError`, never run unisolated (C2). |

## 9. Common failure modes

1. **`flaky` slips into the hash.** Detect: a varying `flaky` changes `content_hash`. Recover: add to
   `HASH_EXCLUDED_FIELDS`; the C3 test must assert exclusion.
2. **Silent unisolated run.** Detect: `verify` succeeds with isolation configured but capability absent.
   Recover: raise `SandboxExecutionError` (RM7).
3. **Patch games the secondary.** Detect: a patch editing the secondary file changes the held-out result.
   Recover: re-materialize the secondary post-patch (C4).
4. **A `FLAKY` verdict appears.** Detect: a sixth state in `VerdictState`. Recover: remove — flakiness is
   the `flaky` boolean (R1).
5. **Drift into proposer/store or a verdict-schema rewrite.** Detect: edits outside §4. Recover: revert;
   M2 is verifier-confined hardening.
6. **Isolation test silently passes in CI without the capability.** Detect: the test "passes" where
   `unshare -n` is impossible. Recover: capability-detect and skip-with-reason instead.

## 10. Definition of Done

Mirrors `M2_SPEC` §3 and §14. M2 is complete only when: two-phase isolation works under `CAP_SYS_ADMIN`
with a passing no-egress control; Determinism Level 4 holds (identical hash + normalized output; varying
`flaky` does not change the hash); flake detection records `flaky` as provenance (excluded from the hash,
no new state); `secondary_passed` is populated with the secondary re-materialized post-patch; the taxonomy
is unchanged; all gates green in container and CI (isolation tests capability-gated); proposer/client/store
unmodified and episode/orchestrator touched only by the `flaky` field + passthrough; README updated; `main`
green; tag-ready `m2-complete`.

## 11. Boundaries — belongs to M3+ (must NOT appear in M2)

- **M3:** indexed/DB episode store; query; full-record integrity digest; promotion of `flaky` into the
  episode-consumer pathways beyond simple persistence.
- **M4:** dataset loader; real SWE-bench tasks; held-out train/test split; multiple tasks.
- **M5+:** batch runner; arms; memory; routing; cost guard; second model.
- **Anywhere later:** property-based testing, resource profiling, streaming generation, richer prompts,
  git provenance (R4).

Any of the above in an M2 commit is a boundary violation and must be removed before M2 is declared
complete.

*End of M2 Implementation Handoff. Build strictly within it and the frozen `M2_SPEC.md`. Do not begin the
first commit until it is explicitly authorized.*
