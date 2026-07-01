# M2 — Engineering Specification

**Project:** Velith
**Milestone:** M2 — Deterministic, hardened verifier
**Document type:** Engineering contract. **RATIFIED AND FROZEN** (R1–R5 → `DECISIONS.md` D17–D21).
Conformant with `VISION.md`, `DECISIONS.md` (D1–D16), and the ratified M0–M10 roadmap (D12).
**Depends on:** M1 (frozen, tagged `m1-complete`).
**Status:** Frozen for implementation. The R3 network-isolation feasibility prototype is **complete**;
the supported mechanism is **Fallback B — `cap_add: SYS_ADMIN` + `unshare -n`** (§10/§16). The M2
Implementation Handoff is authorized against this frozen specification.
**Estimated effort:** 4–6 focused engineering days.

---

## 0. Ratified architectural decisions (R1–R5 → D17–D21)

Binding. Recorded in `DECISIONS.md` as D17–D21.

- **R1 (→D17) — Verdict taxonomy unchanged; flakiness is metadata, not an outcome.** No `FLAKY` verdict.
  The closed taxonomy remains exactly: `PASSED`, `FAILED`, `PATCH_APPLY_FAILED`, `NO_PATCH`,
  `INFRA_ERROR`. Flakiness is *measurement quality*, recorded as a boolean `flaky` on the `Verdict` and
  **persisted into the episode as provenance** (§9), never as a verdict state.
- **R2 (→D18) — Determinism Levels; M2 targets Level 4.** Reproducibility is graded (§7). M2 must reach
  **Level 4 (same execution environment)** — making Levels 1–3 hold structurally rather than incidentally.
- **R3 (→D19) — Two-phase sandbox; ratified mechanism is Fallback B.** Phase 1: network ON, dependency
  preparation. Phase 2: network OFF, test execution. The feasibility prototype determined that
  unprivileged `unshare -rn` is **blocked** by the Docker Desktop/WSL2 default seccomp profile
  (`Operation not permitted`), while **`cap_add: SYS_ADMIN` + `unshare -n` works**. The supported
  mechanism is therefore **`cap_add: [SYS_ADMIN]` in `docker-compose.yml` + `unshare -n` wrapping the
  Phase-2 test process** (§10/§16). The two-phase architecture is unchanged; only the mechanism is fixed.
- **R4 (→D20) — Explicit out-of-scope set.** Property-based testing, resource profiling, streaming
  generation, richer proposer prompts, and git-ref provenance are **out of scope for M2** (§13).
- **R5 (→D21) — `flaky` is provenance, not identity: persisted but excluded from the content hash.**
  `flaky` is a reproducibility-breaking measurement-quality sample. It is **recorded in the episode for
  analysis** but **excluded from the canonical content-hash boundary** (§7.1), as the volatile timing
  fields are. End-to-end record integrity over provenance, if ever required, is a *separate* record-level
  digest (an M3 storage concern), never the content hash.

---

## 1. Purpose of M2

M1 proved the `propose → verify → log` loop is connected and that the verdict is deterministic *at the
verdict level* given a fixed patch. M2 makes the verifier **trustworthy as the program's exact ground
truth**: the verdict becomes reproducible to **Determinism Level 4** under a **pinned, network-isolated
two-phase execution environment**, **flaky tests are detected and flagged**, and the **held-out secondary
("model-gap") signal** is populated.

If the grounding signal is not exact and reproducible, the compounding experiment (D6) is uninterpretable.
M2 removes the noise.

M2 is a **hardening of the single `VerifierSandbox.verify` seam, not a rewrite** (M1 §16, handoff §11,
RK8). The `secondary_passed` plumbing already runs through the orchestrator (C7); persisting the
measurement-quality `flaky` flag (R1/R5) requires a minimal, sanctioned episode field plus a one-line
orchestrator passthrough — a field addition, not a redesign.

---

## 2. Engineering goals

1. **Network-isolate the test-execution phase** (Phase 2) so untrusted generated code cannot reach the
   network and tests cannot depend on it — closing the accepted M1 risk R3.
2. **Pin the execution environment** to reach Determinism Level 4 (R2): fixed interpreter/locale/time
   settings, no dependency fetch during test execution.
3. **Detect flaky tests** by re-running the primary test and reconciling; record `flaky` as provenance.
4. **Populate `secondary_passed`** from a held-out secondary suite distinct from the primary tests.
5. **Preserve the seam** (RK8): no proposer or store redesign; episode/orchestrator touched only by the
   minimal `flaky`-provenance field + passthrough.

---

## 3. Definition of Done

1. `VerifierSandbox.verify` executes the hidden tests in **two phases (R3)**: Phase 1 (network ON)
   prepares the workspace/dependencies; Phase 2 (network OFF, via `unshare -n` under `CAP_SYS_ADMIN`) runs
   the tests. A control test proves the Phase-2 process has **no network egress** in-container.
2. The verify→log path reaches **Determinism Level 4 (R2)**: under the pinned environment, the same
   recorded proposal verified twice yields the **identical `content_hash` (Level 2)** and identical
   normalized output (Level 3), because the execution environment is fixed (Level 4) — `PYTHONHASHSEED`,
   `TZ`, `LC_ALL`, no Phase-2 network, pinned image. A determinism test asserts this, **including that a
   varying `flaky` value does not change the `content_hash`** (R5).
3. **Flake detection (R1/R5):** the verifier runs the primary test **N times** (config; default ≥ 3). All
   agree → that verdict, `flaky = False`. Divergence → `flaky = True`, loud structured log, nominal verdict
   per §8 (no `FLAKY` state). `flaky` is **persisted in the episode** but **outside the content-hash
   boundary**. A deliberately flaky fixture test is detected and recorded, not silently treated as clean.
4. **`secondary_passed` populated:** after a primary `PASSED`/`FAILED`, the verifier runs the **held-out
   secondary** suite and sets `Verdict.secondary_passed` (`None` for `PATCH_APPLY_FAILED`/`NO_PATCH`). The
   secondary suite is **re-materialized after patch application** so a patch cannot tamper with it (§9). A
   model-gap case (primary passes, secondary fails) is reachable; the episode carries
   `secondary_passed = False` **inside** the content hash (it is reproducible identity), via the C7 mapping.
5. The closed verdict taxonomy is unchanged (R1); `INFRA_ERROR` semantics unchanged. **If isolation is
   configured-on but the mechanism is unavailable, `verify` raises `SandboxExecutionError` — it never runs
   untrusted code unisolated** (§10).
6. `ruff check`, `ruff format --check`, `mypy src tests` (strict), and `pytest` all pass in the container
   and CI over M0 + M1 + M2 code.
7. **CI stays hermetic and deterministic:** no model server; the integration test touches no network. The
   isolation-dependent tests run where `CAP_SYS_ADMIN` is available and are capability-skipped (with a
   clear reason) where it is not — never silently passed (§11 / RM-CI).
8. The proposer (`agent/proposer.py`), LLM client (`llm/client.py`), and store (`episodes/store.py`) are
   **unmodified**. The episode schema (`episodes/episode.py`) and orchestrator (`runner/spike.py`) are
   touched **only** by the sanctioned `flaky`-provenance field and its one-line passthrough (R5).
9. `README.md` documents the hardened-verifier behavior; mergeable to green `main`, tag-ready
   (`m2-complete`), with M0/M1 application logic intact.

---

## 4. Exact repository changes

```
velith/
├── README.md                                   (MODIFIED: M2 hardened-verifier behavior)
├── docker-compose.yml                          (MODIFIED: add `cap_add: [SYS_ADMIN]` for Phase-2 unshare -n; R3/§16)
├── docker/verifier.Dockerfile                  (MODIFIED ONLY IF PROBE 1a shows `unshare` absent — it is present)
├── src/velith/
│   ├── task.py                                 (MODIFIED: optional `secondary_test_command` field +
│   │                                            loader populates it; default keeps M1 constructions valid)
│   ├── core/config.py                          (MODIFIED: flake-rerun count, determinism env, isolation toggle)
│   ├── episodes/episode.py                     (MODIFIED, MINIMAL: add provenance field `flaky` (default
│   │                                            False), add it to HASH_EXCLUDED_FIELDS — outside the hash, R5)
│   ├── runner/spike.py                         (MODIFIED, MINIMAL: one-line `flaky=verdict.flaky` passthrough)
│   └── harness/verifier_sandbox.py             (MODIFIED: two-phase exec, pinned env, `unshare -n` isolation,
│                                                flake loop, held-out secondary run; `Verdict` gains `flaky`)
└── tests/
    ├── fixtures/calc_add_bug/
    │   ├── <secondary suite file>              (NEW: held-out secondary tests; §9)
    │   └── <flaky fixture file>                (NEW: a deliberately flaky test for the flake test; §8)
    ├── unit/test_verifier_sandbox.py           (MODIFIED: isolation, determinism-L4, flake, secondary tests)
    └── unit/test_episode.py                    (MODIFIED: assert `flaky` is excluded from the hash, R5)
```

**Explicitly NOT modified:** `agent/proposer.py`, `llm/client.py`, `episodes/store.py`. The proposer reads
nothing from the repo (M1), so the secondary suite is held out by construction (R4). RK8 holds: a field
addition + passthrough is not a redesign.

---

## 5. Public interfaces (contracts)

`VerifierSandbox.verify(task, patch) -> Verdict` — **signature unchanged**:

- `Verdict.state` decided by the **primary** hidden test, run in Phase 2 (network OFF via `unshare -n`)
  under the pinned environment; reproducible to Determinism Level 4 for a fixed patch.
- `Verdict.secondary_passed` **populated** from the held-out secondary suite, or `None` when no code ran.
  **Inside** the content hash (identity).
- `Verdict.flaky` (NEW, default `False`) — `True` iff the primary test's N reruns disagreed (R1).
  **Provenance**, persisted in the episode but **outside** the content hash (R5/§7.1).
- `Verdict.output` normalized and reproducible (M1 normalization retained as defense in depth).

`Task` gains an **optional** `secondary_test_command: tuple[str, ...]` (default empty → "no secondary").
Existing M1 `Task` constructions remain valid. The orchestrator maps `Verdict.secondary_passed` (existing,
C7) **and now `Verdict.flaky`** (one new line) into the episode; `Episode` gains a `flaky` field added to
the hash-excluded set.

---

## 6. Internal interface & data flow (hardened, two-phase `verify`)

```
verify(task, patch):
  ensure disposable git workspace                 [M1, unchanged]
  reset --hard; clean -fd  (CWD-guarded)           [M1, unchanged]
  git apply patch -> PATCH_APPLY_FAILED on fail    [M1, unchanged]
  --- M2, all inside this method ---
  PHASE 1 (network ON):  prepare workspace/deps    [R3]   (no-op for the M1 fixture; deps in image)
  re-materialize held-out secondary suite          [§9]   (so the patch cannot have tampered with it)
  PHASE 2 (network OFF via `unshare -n`, pinned env §7):
     run PRIMARY test N times                       [§8]  -> reconcile -> state, flaky
     if PASSED/FAILED: run SECONDARY suite          [§9]  -> secondary_passed = bool
  build Verdict(state, normalized output, secondary_passed, flaky, duration)
```

---

## 7. Determinism model — Determinism Levels (R2)

- **Level 1 — Same verdict.** Re-verification yields the same `verdict_state`.
- **Level 2 — Same content hash.** The episode `content_hash` is identical (M1/D16.1).
- **Level 3 — Same verifier output.** Raw output identical, save the single normalized wall-clock token.
- **Level 4 — Same execution environment.** The environment is fixed and isolated, so Levels 1–3 hold
  **structurally**.

**M2 targets Level 4** via: Phase-2 network isolation (§10); a pinned interpreter env (`PYTHONHASHSEED=0`,
`TZ=UTC`, `LC_ALL=C`, `PYTHONDONTWRITEBYTECODE=1`); the pinned base image (M0); and retained M1
normalization. Scope: **same-machine bit-for-bit on the pinned image**; asserted same-machine in CI.

### 7.1 Identity vs. provenance — the content-hash boundary (R5)

The `content_hash` is the **reproducible identity of a grounded result**: a field is **inside** iff it is a
reproducible function of `(task, patch, environment)`; a field that can vary across re-verifications is
**provenance** and stays **outside**.

- **Identity (in the hash):** `task_id, seed, arm, model, model_version, prompt, patch, verdict_state,
  verdict_output, secondary_passed, prompt_tokens, completion_tokens, velith_version`. `secondary_passed`
  is identity — the secondary suite is deterministic (M1 §23), hence reproducible.
- **Provenance (excluded):** `timestamp, latency_seconds, verify_seconds`, **and `flaky`** (R5) — the
  observed output of a non-deterministic sampling process; including it would make Level 2 unsatisfiable for
  the flaky episodes it flags.

Full-record tamper-evidence, if ever required, is a **separate record-level digest**, distinct from
`content_hash`.

---

## 8. Flake detection model (R1/R5)

Phase 2 runs the primary test **N times** (config; default ≥ 3). If all agree on `verdict_state` and
normalized output → that verdict, `flaky = False`. If any disagree → `flaky = True`, loud structured
WARNING, nominal `verdict_state` from the first run (untrustworthy, not silently clean). No new verdict
state (R1). `flaky` is **persisted in the episode** (provenance) but **excluded from the content-hash
boundary** (§7.1). The M1 fixture's primary test must remain deterministic (M1 §23); flakiness is exercised
by a dedicated controlled flaky fixture used only in the flake-detection test.

---

## 9. Held-out secondary suite / model-gap model

A **held-out secondary** suite, never shown to the proposer (held out by construction, R4), run only after
a primary `PASSED`/`FAILED`. Model-gap: a patch that makes the *primary* pass but the *secondary* fail has
overfit the visible signal. For `calc_add_bug`, the secondary adds explicit cases a "cheating" patch cannot
satisfy (`add(-1, 1) == 0`, `add(0, 0) == 0`, further pairs — **example-based, not property-based**, R4).
`secondary_passed` is **identity** (in the hash); the primary still decides `verdict_state`.

**Anti-wireheading invariant (ratified):** the secondary suite is **re-materialized into the workspace from
the pristine fixture after the patch is applied**, so a candidate patch cannot tamper with the held-out
check. `Task.secondary_test_command` defines how it is run.

---

## 10. Network isolation model — two-phase, mechanism B (R3)

Only the **test-execution phase** is isolated; the container remains network-enabled so the proposal step
(before `verify`) reaches Ollama. Single-container — no orchestrator/compose split.

- **Phase 1 (network ON):** workspace/dependency preparation (no-op for the M1 fixture).
- **Phase 2 (network OFF):** the primary and secondary test commands are wrapped in **`unshare -n`**, which
  requires **`CAP_SYS_ADMIN`** — granted via **`cap_add: [SYS_ADMIN]`** in `docker-compose.yml` (the
  prototype-selected mechanism; unprivileged `unshare -rn` is blocked by the Docker Desktop seccomp
  profile). A control test asserts the Phase-2 process cannot open an outbound socket. If `lo` is required
  by a future test, it is brought up inside the namespace.

**Mandatory-isolation invariant:** isolation is required; if `unshare -n` fails (capability absent),
`verify` raises `SandboxExecutionError` (mapped to `INFRA_ERROR`) — it **never** runs untrusted code
unisolated. A config toggle exists only for explicitly-sanctioned non-production contexts and defaults to
isolation ON.

---

## 11. Error handling, logging, CI, security

- **Error handling** unchanged in shape; a flaky primary does not raise (returns nominal verdict +
  `flaky=True`). Missing isolation capability with isolation-on raises `SandboxExecutionError` (§10).
- **Logging** extends M1's events: per-rerun verdicts, flake decision, secondary result, Phase-2 isolation
  confirmation. No model output at INFO.
- **CI (RM-CI):** the isolation-dependent tests detect capability availability — they **run and pass** where
  `CAP_SYS_ADMIN` is granted (local Docker Desktop, and CI if the runner permits `cap_add`), and **skip with
  an explicit reason** where it is not. They are **never silently passed**. Confirm GitHub Actions permits
  `cap_add: SYS_ADMIN` early (handoff pre-C2 check); if not, the isolation gate is local-acceptance like the
  M1 live run, and CI runs the capability-independent surface.
- **Security:** M2 **closes R3** — untrusted generated code executes with no network in Phase 2. Trade-off:
  `CAP_SYS_ADMIN` is broad; it is granted to the verifier container only, which already executes untrusted
  code in a disposable workspace, and is the minimum that makes `unshare -n` work under Docker Desktop. The
  held-out secondary is tamper-proofed by re-materialization (§9).

## 12. Risks

| ID | Risk | Severity | Mitigation |
|---|---|---|---|
| RM-CI | CI runner does not permit `cap_add: SYS_ADMIN`; isolation tests cannot run there. | **High** | Capability-detect and skip-with-reason in CI (never silent pass); confirm GitHub Actions support pre-C2; isolation remains a local-acceptance gate if CI cannot. |
| RM2 | Hidden nondeterminism beyond timing breaks Level 4. | Med | Pin `PYTHONHASHSEED`/`TZ`/`LC_ALL`; assert Level 2/3; retain M1 normalization. |
| RM3 | A patch tampers with the held-out secondary, defeating the model-gap signal. | Med | Re-materialize the secondary from the pristine fixture after patch application (§9). |
| RM4 | `flaky` accidentally hashed, breaking Level 2 for flaky episodes. | Med | R5: `flaky` in `HASH_EXCLUDED_FIELDS`; `test_episode` asserts a varying `flaky` leaves the hash unchanged. |
| RM5 | `CAP_SYS_ADMIN` broadens the container's privilege. | Med | Granted only to the disposable verifier container; documented; `unshare -n` is the minimal use. |
| RM6 | M2 drifts into proposer/store, or beyond the sanctioned `flaky` field. | Med | RK8/R1/R5: confined to verifier + `Task` + config + the single `flaky` field/passthrough. |

## 13. Explicit non-goals (R4 and inherited)

- **Property-based testing**, **resource profiling**, **streaming generation**, **richer proposer
  prompts**, **git-ref provenance** — out of scope (R4).
- No proposer or store changes; no episode/orchestrator change beyond the sanctioned `flaky` field +
  passthrough (RK8/R5); no new `FLAKY` verdict (R1); `flaky` never enters the content hash (R5).
- No memory, retrieval, arms, multiple tasks, dataset loader (M4–M7); no indexed/DB store (M3); no
  model-based judging (D3); no second model/routing (M5); no new compose services.

## 14. Milestone & verification checklist

- [ ] Two-phase execution (network ON prep → network OFF test via `unshare -n` under `CAP_SYS_ADMIN`);
      Phase-2 no-egress control test passes.
- [ ] Determinism Level 4: identical `content_hash` and normalized output across re-verification; pinned env;
      a varying `flaky` does not change the hash (R5).
- [ ] Flake detection: N reruns; deliberately flaky fixture → `flaky = True`, logged and persisted; no
      `FLAKY` state.
- [ ] `secondary_passed` populated (in the hash); secondary re-materialized post-patch; model-gap case
      reachable and logged via C7.
- [ ] Verdict taxonomy unchanged; missing-isolation-capability raises (never runs unisolated).
- [ ] `ruff`, `ruff format`, `mypy --strict`, `pytest` green in container and CI; CI hermetic; isolation
      tests skip-with-reason where `CAP_SYS_ADMIN` is unavailable.
- [ ] Proposer / client / store unmodified; episode/orchestrator changed only by the `flaky` field +
      passthrough.
- [ ] README documents M2 behavior; `main` green; tag-ready `m2-complete`.

## 15. Future compatibility (M3+)

M3 extends episode storage/indexing without altering identity (content-hash) fields. Full-record
tamper-evidence, if required, is a separate record-level digest (§7.1). M5–M7 add arms/memory with no
verifier change and may consume the persisted `flaky` provenance. The two-phase, pinned, isolated verifier
is the durable substrate every later rung reuses.

## 16. R3 feasibility prototype — RESOLVED

The prototype (executed during ratification) established: `unshare` is present in the verifier image;
unprivileged `unshare -rn` is **blocked** by the Docker Desktop/WSL2 default seccomp profile
(`Operation not permitted`); **`cap_add: SYS_ADMIN` + `unshare -n` succeeds** and isolates Phase-2 egress;
the container without `unshare` retains network (Phase 1). **Selected mechanism: Fallback B.** No
architectural amendment was required — the two-phase model (R3) stands; the `docker-compose.yml`
`cap_add: [SYS_ADMIN]` is the anticipated conditional modification now made concrete.

## 17. Ratification status

**FROZEN.** R1–R5 are recorded as `DECISIONS.md` D17–D21. The R3 mechanism is resolved (Fallback B). The M2
Implementation Handoff is authorized against this specification. Implementation begins only after the
handoff is reviewed and the first commit is explicitly authorized.

*End of M2 Engineering Specification — ratified and frozen.*
