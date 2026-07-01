# M1 — Implementation Handoff

**Project:** Velith
**Milestone:** M1 — propose → verify → log episode (the spike)
**Audience:** The implementation team (Claude Opus Cowork) executing M1.
**Authority:** This document is the execution contract. It is subordinate to, and must not contradict, the immutable contracts: `VISION.md`, `ARCHITECTURE.md`, `DECISIONS.md` (D1–D16), `ROADMAP.md`, `PROJECT_STATE.md`, the M0 Engineering Specification, and the M1 Engineering Specification. Where this document and a frozen contract appear to differ, the frozen contract wins and the discrepancy is raised, not silently resolved.
**Status:** Ratified for implementation (M1 approved; D16 governs the open-question resolutions).
**Preconditions:** M0 complete, merged to `main`, tagged `m0-complete`, all gates green. M0 is frozen and must not be modified except the four files M1 is explicitly permitted to touch (§4).

---

## 1. Objective

**What M1 accomplishes.** M1 delivers one runnable command that takes a single fixture engineering task, has a local model **propose** a candidate patch, has a containerized verifier **dispose** of it against a hidden test suite, and **logs** the outcome as a provenance-complete, content-hashed episode that survives container exit. It proves Velith's central loop is real end to end, on the ground, for one task.

Concretely, M1 is done when `python -m velith.runner.spike --task <id> --seed 0`, run through the container, produces one JSON episode record on the host containing every field in the M1 spec §9.1, with a verifying content hash, and the verify→log path is reproducible given a recorded proposal (D16.1).

**What M1 explicitly does NOT accomplish.** No memory, no retrieval, no experiment arms (A0–A4), no multiple tasks, no dataset loader, no held-out lock, no batch runner, no statistics, no frozen evaluation, no model routing, no cost guard beyond a recorded timeout/token count, no network isolation, no bit-for-bit determinism hardening, no indexed/DB store, no model-based judging anywhere. M1 runs one task, with one model, writes append-only JSONL, and stops. (Full boundary list in §11.)

---

## 2. Engineering philosophy — inherited invariants

These are inherited from D1–D16 and the M0/M1 specs. They are **non-negotiable**; violating any one is a stop-and-escalate condition, not an implementation judgment call.

1. **The verdict is produced inside the container.** The host is never the source of truth for a verdict (D3, M0 §2). Orchestration runs in-container; Ollama is reached from the container via `host.docker.internal` (D16.2).
2. **No model judges correctness — ever.** The verifier is deterministic and zero-model-gap (D3, D16.7). The model's only role is *proposing*. An LLM-as-judge anywhere in the verify path is a hard violation (this is the MiniNoetica anti-pattern, D11).
3. **Outcome vs. error is sacred.** A test failure, a non-applying patch, or no patch are *valid logged grounded outcomes* (exit 0). Only infrastructure faults are errors (`INFRA_ERROR`, non-zero exit) (D16.7, D2). `FAILED` episodes are first-class learning data; treating them as exceptions corrupts the future compounding signal.
4. **Provenance is conserved.** Every episode carries its full derivation and a content hash; no orphan state (I2). The schema is provenance-complete now because retrofitting provenance is the failure this program exists to avoid.
5. **LLMs are replaceable components, not the architecture.** The proposer depends on a model *capability* through a thin adapter, not on Ollama directly (D9, D16.4). The adapter must not grow into routing in M1.
6. **State-centric, single source of truth.** Components hold beliefs about state through defined contracts; no private global mutable state (D9, M0 §7).
7. **Determinism lives in the verifier, not the model.** M1's blocking reproducibility is the verify→log path given a recorded proposal; proposal-level determinism is attempted and recorded, not gated (D16.1).
8. **Fail fast, fail loud; no silent except.** Config and infra errors raise immediately with actionable messages (M0 §10).
9. **Structured logging only.** No `print` except the single human-facing CLI summary line (M0 §9).
10. **Strict gates hold from the first commit.** `ruff`, `ruff format`, `mypy --strict`, `pytest`, all green, all in the container; CI stays hermetic with no Ollama (M0 §7, D16, M1 §14).
11. **M1 minimalism.** Each milestone produces a running system; nothing is built ahead of its milestone. Scope creep across a boundary is a violation, not initiative.

---

## 3. Dependency graph

### 3.1 Module dependencies

```
config (M0, extended)
  └─ used by: llm/client, harness/verifier_sandbox, episodes/store, runner/spike

llm/client (Ollama adapter)
  └─ depends on: config, core/logging
  └─ used by: agent/proposer

agent/proposer (ProposerAgent)
  └─ depends on: llm/client, task, core/logging
  └─ used by: runner/spike

task (Task value type)
  └─ depends on: (nothing internal)
  └─ used by: agent/proposer, harness/verifier_sandbox, runner/spike

harness/verifier_sandbox (VerifierSandbox)
  └─ depends on: task, config, core/logging
  └─ used by: runner/spike

episodes/episode (Episode schema + content hash)
  └─ depends on: (nothing internal beyond stdlib/pydantic)
  └─ used by: episodes/store, runner/spike

episodes/store (EpisodeStore, JSONL)
  └─ depends on: episodes/episode, config, core/logging
  └─ used by: runner/spike

runner/spike (orchestrator + CLI)
  └─ depends on: task, agent/proposer, harness/verifier_sandbox,
                 episodes/episode, episodes/store, config, core/logging
```

The orchestrator (`runner/spike`) is the only module that knows the order of operations; every other module is a leaf or near-leaf depending only on its declared inputs.

### 3.2 Implementation order

Build leaves first, the orchestrator last, value types and the verifier before the model path:

1. `episodes/episode` (pure value type + hashing — no internal deps)
2. `episodes/store` (depends only on episode + config)
3. `task` + the fixture (pure value type + test data)
4. `harness/verifier_sandbox` (real, deterministic given a fixed patch — depends on task + config)
5. `llm/client` (thin Ollama adapter — depends on config)
6. `agent/proposer` (depends on llm/client + task)
7. `runner/spike` (orchestrator — depends on all)
8. integration test (hermetic, mocked proposer, real verify→log)
9. Docker/compose volume + config wiring
10. README

### 3.3 Why this order minimizes integration risk

The two deterministic, model-free components — the **store** and the **verifier** — are built and unit-tested *before* the stochastic model path. This means by the time the proposer (the only nondeterministic component) is introduced, the verify→log path it feeds into is already proven and reproducible. Integration therefore connects a *new* uncertain component to a *known-good* deterministic spine, not two unknowns at once. The orchestrator is built last, when all its dependencies already satisfy their contracts, so its only new risk is wiring order — which the hermetic integration test (step 8) catches before any live model run.

---

## 4. File creation order

Additions only, except the four M1-permitted modifications to frozen M0 files. **No other M0 file may be modified.**

> Permitted M0 modifications: `core/config.py` (extend `Settings`), `docker-compose.yml` (episode volume + network for Ollama), `.gitignore` (ignore episodes), `README.md` (M1 usage). Optionally `docker/verifier.Dockerfile` may add `git` if patch-apply requires it — confirm need before touching it.

For each file: purpose · responsibilities · public API (contract, not code) · dependencies · what must NOT be implemented yet.

### 4.1 `src/velith/episodes/episode.py` — NEW
- **Purpose:** define the `Episode` record and its canonical content hash.
- **Responsibilities:** hold all M1 spec §9.1 fields; compute a deterministic content hash over a canonical serialization; expose a build/construction path used by the orchestrator.
- **Public API (contract):** an `Episode` value type carrying the §9.1 fields; a content-hash operation that is stable given identical content; a verification operation that confirms a record's hash.
- **Dependencies:** stdlib + pydantic only (no internal deps).
- **NOT yet:** no storage I/O, no querying, no indexing, no arm logic (the `arm` field exists, fixed to one baseline value; no behavior keys off it).
- **Must define and freeze (this commit):** the canonical-serialization rule (`sort_keys=True, ensure_ascii=False, separators=(",", ":")`, UTF-8, SHA-256) and the **hash-boundary field set** — content fields only, **excluding** `timestamp`, `latency_seconds`, `verify_seconds`, and `content_hash` itself (M1 spec §9.1.1, protecting D16.1). `episode.py` is the single authority for this boundary.

### 4.2 `src/velith/episodes/store.py` — NEW
- **Purpose:** append-only JSONL persistence of episodes.
- **Responsibilities:** durably append one episode to the configured JSONL path before returning; read all episodes back, verifying each hash on read (I2).
- **Public API (contract):** `append(episode) -> written location`; `read_all() -> sequence of Episode`.
- **Dependencies:** `episodes/episode`, `config`, `core/logging`.
- **NOT yet:** no indexed/DB store, no query-by-arm/seed/checkpoint, no integrity scans beyond per-record hash verify on read (M3 owns those).

### 4.3 `src/velith/task.py` + `tests/fixtures/<task_id>/` — NEW
- **Purpose:** the M1 fixture task descriptor and its data.
- **Responsibilities:** describe one task — id, working repo path/ref, prompt material, hidden-test invocation; the fixture provides a minimal buggy repo + a hidden test (D16.3).
- **Public API (contract):** a `Task` value type exposing the above; a loader for the single fixture task.
- **Dependencies:** none internal.
- **NOT yet:** no dataset loading, no multiple tasks, no SWE-bench integration (M4); the fixture is **not a benchmark** and must never be used as one (D16.3, D8).

### 4.4 `src/velith/harness/verifier_sandbox.py` — NEW
- **Purpose:** the deterministic verifier — apply a candidate patch, run the hidden tests in-container, return a `Verdict`. The single seam M2 hardens.
- **Responsibilities:** operate on a **disposable copy** of the fixture repo (never the committed fixture under `tests/fixtures/`); **before each verification**, restore clean state via `git reset --hard` then `git clean -fd`, preceded by an **asserted working-directory guard** that refuses to run if the CWD is not inside the disposable copy; apply the candidate patch with the **pinned `git apply`** mechanism, mapping a clean non-apply to `PATCH_APPLY_FAILED`; execute the hidden test suite inside the container; classify the result into a verdict state (§Verdict taxonomy, D16.7); enforce a wall-clock timeout on test execution.
- **Public API (contract):** `verify(task, patch) -> Verdict`. Deterministic given a fixed patch and task. Raises only on infra fault; test failure / bad patch are verdict states, never exceptions.
- **Dependencies:** `task`, `config`, `core/logging`; `git` in the image if patch-apply needs it.
- **NOT yet:** no network isolation, no flake detection, no bit-for-bit determinism guarantees beyond reset-before-run, no `secondary_passed` population (all M2 — leave the field `null`); no model anywhere in this module. A post-run reset is optional, not required.

### 4.5 `src/velith/llm/client.py` — NEW
- **Purpose:** a **thin** Ollama adapter (the M5 routing seam, kept thin in M1).
- **Responsibilities:** given prompt + model + sampling params, return completion text plus call metadata (model+version, prompt/completion token counts, latency); raise a typed `ModelUnavailableError` on infra failure.
- **Public API (contract):** `generate(prompt, model, seed, temperature) -> completion + metadata`.
- **Dependencies:** `config`, `core/logging`; reaches Ollama via `host.docker.internal` (D16.2).
- **NOT yet:** no routing, no model selection policy, no cost guard, no retry beyond a single bounded attempt (M5). Must not grow into a framework (D16.4).

### 4.6 `src/velith/agent/proposer.py` — NEW
- **Purpose:** turn a `Task` into a candidate `Proposal`.
- **Responsibilities:** construct the exact prompt from the task; call `llm/client`; perform minimal extraction of a diff-shaped patch from the completion; return a `Proposal` (patch, exact prompt, token counts, latency, model+version). If no usable patch, return a `Proposal` carrying a `NO_PATCH` marker — do not raise.
- **Public API (contract):** `propose(task, seed) -> Proposal`.
- **Dependencies:** `llm/client`, `task`, `core/logging`.
- **NOT yet:** no memory/retrieval, no multiple attempts, no self-critique, no elaborate patch parsing (minimal extraction only — elaborate parsing is the MiniNoetica `analyze()` debt to avoid).

### 4.7 `src/velith/runner/spike.py` — NEW
- **Purpose:** orchestrate proposer → verifier → store for one task; expose the CLI.
- **Responsibilities:** load the fixture task; call `proposer.propose`; call `verifier.verify`; assemble the `Episode` (proposal + verdict + run context); `store.append`; print/log the written path + a one-line summary; own the control flow and the only knowledge of operation order; map outcomes to exit codes (0 for any logged grounded outcome, non-zero only on `INFRA_ERROR`).
- **Public API (contract):** `python -m velith.runner.spike --task <id> --seed <int>`.
- **Dependencies:** all M1 modules + `config` + `core/logging`.
- **NOT yet:** no loops over tasks, no arms, no statistics, no memory.

### 4.8 `src/velith/core/config.py` — MODIFIED
- **Purpose:** extend `Settings` with Ollama host/model and episode output path.
- **Responsibilities:** validated settings for Ollama endpoint, default model, episode JSONL path, verifier timeout.
- **NOT yet:** nothing beyond validated config.

### 4.9 `docker-compose.yml` — MODIFIED
- **Purpose:** persist episodes; enable Ollama reachability.
- **Responsibilities:** bind-mount host `./data/episodes/` into the container; ensure the run path can reach `host.docker.internal`; keep the default `verifier` `command` (pytest) unchanged; the spike runs via command override.
- **NOT yet:** no new services, no databases/queues, no network isolation.

### 4.10 `.gitignore` — MODIFIED
- Ignore `data/episodes/`.

### 4.11 `README.md` — MODIFIED
- Document the M1 run command, the `host.docker.internal` mechanism, and record/replay reproducibility behavior (D16.1, D16.2).

### 4.12 Tests — NEW
- `tests/unit/test_episode.py`, `tests/unit/test_store.py`, `tests/unit/test_verifier_sandbox.py` (real local execution against fixture patches), `tests/unit/test_proposer.py` (mocked client), `tests/integration/test_spike_episode.py` (mocked proposer, real verify→log, hermetic — no Ollama).

---

## 5. Commit plan

Atomic commits. No commit mixes unrelated concerns. Each leaves lint/type/test green where feasible. (This sequence matches M1 spec §18; it is the binding order.)

### C1 — `feat: episode schema + content hash`
- **Scope:** `episodes/episode.py` + `tests/unit/test_episode.py`.
- **Verification:** unit tests pass in container; schema carries all §9.1 fields; hash stable + verifiable.
- **DoD:** `Episode` constructs, hashes deterministically, verifies; gates green.
- **Rollback condition:** hash not stable across identical content, or any §9.1 field missing.

### C2 — `feat: episode store (jsonl, append-only)`
- **Scope:** `episodes/store.py` + `tests/unit/test_store.py`.
- **Verification:** append then read-all returns the record; hash verified on read; append-only (no mutation).
- **DoD:** durable append + read with integrity check; gates green.
- **Rollback condition:** writes not durable before return, or prior records mutated.

### C3 — `feat: task type + minimal fixture`
- **Scope:** `task.py` + `tests/fixtures/<task_id>/`.
- **Verification:** the fixture is a minimal buggy repo + hidden test; `Task` exposes repo ref, prompt material, hidden-test invocation.
- **DoD:** fixture task loads; hidden test runs and fails on the unpatched repo (proving it's a real check).
- **Rollback condition:** fixture has no failing hidden test (nothing to verify against), or `Task` leaks dataset-loader concerns.

### C4 — `feat: verifier sandbox`
- **Scope:** `harness/verifier_sandbox.py` + `tests/unit/test_verifier_sandbox.py`; Dockerfile `git` if needed.
- **Verification:** apply a known-good patch → `PASSED`; known-bad patch → `FAILED`; malformed patch → `PATCH_APPLY_FAILED`; timeout enforced; runs in container. **Determinism check:** run the *same* patch through `verify()` twice with a deliberate intervening filesystem mutation (e.g. leave stray files / modify a tracked file between calls) and assert identical verdicts — proving reset-before-run isolates state. **Fixture check:** confirm the unpatched fixture repo fails its hidden test **consistently** across repeated runs (fixture determinism).
- **DoD:** all four verdict paths produced from real execution; deterministic given fixed patch; no model used.
- **Rollback condition:** any test failure surfaces as an exception instead of a verdict; non-determinism given a fixed patch (including state bleed between runs); the destructive commands run without the CWD guard; the patch-apply tool is anything but the pinned `git apply`; network isolation accidentally introduced (that's M2).

### C5 — `feat: ollama client (thin adapter)`
- **Scope:** `llm/client.py` + `tests/unit/test_proposer.py` scaffolding for mocking (client unit-tested with a mock transport).
- **Verification:** `generate` returns completion + metadata under a mocked transport; raises `ModelUnavailableError` on simulated infra failure.
- **DoD:** adapter contract honored under mock; no routing/cost logic present.
- **Rollback condition:** adapter contains routing, selection policy, or cost-guard logic (D16.4 violation).

### C6 — `feat: proposer agent`
- **Scope:** `agent/proposer.py` + `tests/unit/test_proposer.py` (mocked client).
- **Verification:** given a mocked completion containing a diff → `Proposal` with that patch; completion with no diff → `Proposal` with `NO_PATCH` marker (no raise).
- **DoD:** proposer returns a `Proposal` for both cases; minimal extraction only.
- **Rollback condition:** proposer raises on no-patch; elaborate parsing introduced; any memory/retrieval present.

### C7 — `feat: spike orchestrator + CLI`
- **Scope:** `runner/spike.py`; `core/config.py` extension.
- **Verification:** CLI parses `--task/--seed`; orchestrates proposer→verifier→store; maps outcomes to exit codes (0 for grounded outcomes, non-zero only on `INFRA_ERROR`).
- **DoD:** end-to-end orchestration runs under a mocked proposer to a written episode; gates green.
- **Rollback condition:** orchestrator embeds operation-order knowledge anywhere but here; a `FAILED` verdict yields non-zero exit.

### C8 — `test: hermetic spike integration`
- **Scope:** `tests/integration/test_spike_episode.py` (mocked proposer, real verify→log).
- **Verification:** mocked proposer with a known-good patch → episode with `PASSED`, hash verifies; known-bad → `FAILED`; malformed → `PATCH_APPLY_FAILED`; no Ollama touched.
- **DoD:** the full pipe proven hermetically; reproducible verify→log given the recorded (mocked) proposal (D16.1).
- **Rollback condition:** the test reaches Ollama or the network; non-reproducible verdict/hash on a fixed proposal.

### C9 — `build: episode volume + gitignore`
- **Scope:** `docker-compose.yml`, `.gitignore`.
- **Verification:** an episode written inside the container appears on the host under `./data/episodes/` and survives `--rm`.
- **DoD:** persistence proven across container exit; `data/episodes/` gitignored.
- **Rollback condition:** episodes lost on container exit; generated data tracked by git.

### C10 — `docs: M1 run + record/replay usage`
- **Scope:** `README.md`.
- **Verification:** a fresh reader can run the M1 command and reproduce a logged episode from the README alone.
- **DoD:** command, `host.docker.internal` mechanism, and record/replay behavior documented.
- **Rollback condition:** README omits the run command or the reachability mechanism.

---

## 6. Verification gates (per commit)

After **every** commit, the four M0 gates must pass in the container; the commit-specific check is additional. Failure of any = the commit is not done.

**Always-run gates (all commits), in the container:**
- `docker compose run --rm verifier ruff check .` → expect `All checks passed!`
- `docker compose run --rm verifier ruff format --check .` → expect `N files already formatted`
- `docker compose run --rm verifier mypy src tests` → expect `Success: no issues found`
- `docker compose run --rm verifier pytest -q` → expect all tests passed
- **Failure** = any non-green output, any error, any reduction in strictness.

**Commit-specific checks:**
- **C1–C2:** the new unit tests pass; episode round-trips with hash verification.
- **C3:** the fixture's hidden test **fails on the unpatched repo** (run it directly to confirm there's a real check to satisfy).
- **C4:** all four verdict states produced from real patch execution; re-running verification on a fixed patch yields the identical verdict (determinism given fixed input).
- **C5–C6:** mocked-transport/mocked-client tests prove contracts; `ModelUnavailableError` path exercised.
- **C7:** orchestration under a mocked proposer writes a complete episode; exit-code mapping correct.
- **C8:** the hermetic integration test is green and touches no network.
- **C9:** `docker compose run --rm verifier python -m velith.runner.spike --task <id> --seed 0` (with a mocked or recorded proposal) writes an episode visible on the host that **survives container exit**; hash verifies.
- **C10:** README reproduction walkthrough succeeds.

**Live acceptance (once, after C9/C10, local only — not a CI gate):** run the spike against **real Ollama** and confirm a real verdict is produced and logged. This satisfies DoD's live criterion; CI never runs it.

---

## 7. Integration order

Modules are connected in three checkpoints, each proving a wider slice before the next is added:

- **Checkpoint A — deterministic spine (after C2, C4).** `episode` + `store` + `verifier_sandbox` are wired by a unit/integration test that runs a fixed patch through the verifier and logs the resulting episode. This proves the **verify→log path** — the reproducible, model-free core — before any model exists. The test must assert that (i) re-running `verify()` on the same patch after an intervening filesystem mutation yields the identical verdict (reset-before-run isolation), and (ii) re-logging the same recorded proposal yields the **same content hash** under the §9.1.1 hash boundary. This is the D16.1 reproducibility surface.
- **Checkpoint B — model path in isolation (after C6).** `llm/client` + `proposer` are wired and proven against a **mocked** transport/client. The stochastic path is validated without touching the deterministic spine or the network.
- **Checkpoint C — full pipe, hermetic (C7–C8).** `spike` connects B's output (a `Proposal`) into A's input (the verifier), with the proposer **mocked**. This proves the assembled machine end to end with no Ollama. Only after Checkpoint C is green is the **live** Ollama run performed (§6 live acceptance).

Integrating in this order means the only moment a live, nondeterministic model touches the system is the very last step, against an already-proven hermetic pipe — so any failure there is isolated to the model boundary, not the wiring.

---

## 8. Risk register

| ID | Class | Risk | Mitigation |
|---|---|---|---|
| RK1 | Determinism | LLM nondeterminism makes proposal-level "same seed → same verdict" unachievable. | Per D16.1, gate only the **verify→log path on a recorded proposal**; record/replay the proposal. Do not chase proposal determinism. |
| RK2 | Technical | Model emits prose/markdown around a diff; patch doesn't apply. | `PATCH_APPLY_FAILED` is a first-class verdict (D16.7); proposer does **minimal** extraction only — no elaborate parser (avoids MiniNoetica `analyze()` debt, RK-debt). |
| RK3 | Docker | Episodes lost on `--rm`; or `git` absent for patch-apply. | Bind-mount `./data/episodes/` (C9); confirm/add `git` in the image (C4) before relying on patch-apply. |
| RK4 | Ollama | Container cannot reach host Ollama (WSL2/Docker Desktop networking). | Use `host.docker.internal` (D16.2); document in README; `ModelUnavailableError` path tested so failure is loud, not silent. |
| RK5 | Architectural | Orchestration drifts to host Python 3.10. | Orchestrate **in-container** on the 3.12 target (D16.2); host is never an execution target. |
| RK6 | Architectural | Model-based judging creeps into the verify path. | Hard invariant (§2.2, D3): no model in `verifier_sandbox`. Reviewer rejects any model import there. |
| RK7 | Determinism/CI | CI flakiness or hidden network dependence. | CI is hermetic (mocked proposer, no Ollama); the integration test asserts no network is touched. |
| RK8 | M2 compatibility | M1 structures the verifier such that M2 hardening requires a rewrite. | Keep patch-apply + test-execution inside one bounded `verify` method M2 can wrap (network isolation, flake detection, pinned env); leave `secondary_passed` as `null`. |
| RK9 | M2 compatibility | Proposer's network call ends up inside the soon-to-be-isolated verifier boundary. | Proposer is a separate module outside the verifier; the model call never sits inside `verifier_sandbox` (so M2's network isolation of the test step won't break proposing). |
| RK10 | Scope/debt | Scope creep (memory, arms, multiple tasks, routing) "while wiring." | §11 boundaries are binding; commit boundaries (§5) keep each step minimal; reviewer rejects any out-of-boundary addition. |
| RK11 | Technical | Untrusted generated code executes with network access in M1. | Container isolation + wall-clock timeout + disposable container now; full network isolation of the test step is later hardening, not an M1 concern. Documented, accepted. |
| RK12 | Provenance | An episode field is omitted "to add later." | All §9.1 fields present from C1; retrofitting provenance is the prohibited failure. Reviewer checks field completeness at C1. |
| RK13 | Docker/Technical | `git clean -fd` blast radius under bind mounts — destructive commands run in the wrong CWD could delete host-mounted files or dirty the committed fixture. | Operate on a disposable copy only; assert CWD is inside the copy before any destructive command; never run reset/clean against `tests/fixtures/` or a bind-mounted host path. |
| RK14 | Determinism | The episode content hash is unstable because volatile fields are inside the hash boundary. | Hash content fields only; exclude `timestamp`/`latency_seconds`/`verify_seconds`/`content_hash` (M1 spec §9.1.1) — required for D16.1. |

---

## 9. Common failure modes

For each: what the engineer is likely to do wrong · how to detect · how to recover.

1. **Treating a test failure as an exception.**
   - *Detect:* a `FAILED` task causes a non-zero exit or a stack trace instead of a logged episode.
   - *Recover:* route test-ran-but-not-passed to the `FAILED` verdict; reserve exceptions for infra only (D16.7). Re-run C4/C7 verification.

2. **Running the verdict on the host instead of the container.**
   - *Detect:* the spike or tests pass on host Python (3.10) but the container path is untested.
   - *Recover:* all verification commands go through `docker compose run --rm verifier ...`; the host is never the source of truth (§2.1).

3. **Letting the LLM adapter grow into a router.**
   - *Detect:* `llm/client.py` contains model-selection, fallback chains, or cost logic.
   - *Recover:* strip to `generate` + metadata; routing is M5 (D16.4). Reject the commit (C5 rollback).

4. **Elaborate patch parsing in the proposer.**
   - *Detect:* multi-branch extraction logic, regex zoo, "repair the diff" heuristics.
   - *Recover:* minimal extraction; if no clean diff, return `NO_PATCH`. Elaborate repair is debt (RK2).

5. **Omitting a provenance field "for now."**
   - *Detect:* an episode lacks a §9.1 field (e.g., `content_hash`, token counts, `velith_version`).
   - *Recover:* complete the schema at C1; never ship a partial record (RK12).

6. **Episodes not surviving container exit.**
   - *Detect:* after a `--rm` run, `./data/episodes/` on the host is empty.
   - *Recover:* bind-mount the episode dir (C9); confirm the write target is the mounted path.

7. **Model-based judging sneaking into the verifier.**
   - *Detect:* an import of `llm`/`proposer` inside `harness/verifier_sandbox.py`.
   - *Recover:* remove it; the verifier is deterministic and model-free (RK6/§2.2). Hard stop.

8. **CI reaching for Ollama.**
   - *Detect:* an integration test hangs or fails in CI trying to contact a model server.
   - *Recover:* mock the proposer in CI; the live run is local-only (M1 §14). The integration test must assert no network.

9. **Combining commits.**
   - *Detect:* a single commit touches the store and the proposer, or the verifier and the CLI.
   - *Recover:* split per §5; no commit mixes unrelated concerns.

10. **Introducing M2 hardening early (network isolation, flake detection, determinism guarantees).**
    - *Detect:* network-disabling flags or retry/quarantine logic in the verifier.
    - *Recover:* remove; that is M2. M1's verifier is functional, not hardened (§11).

11. **`secondary_passed` populated in M1.**
    - *Detect:* the field is set to anything but `null`.
    - *Recover:* leave it `null`; M2 owns it (RK8).

12. **Hashing volatile fields.**
    - *Detect:* the same recorded proposal yields different content hashes across runs, while the verdict is unchanged.
    - *Recover:* exclude `timestamp`, `latency_seconds`, `verify_seconds` (and `content_hash` itself) from the hash boundary; hash content fields only (M1 spec §9.1.1). Without this, D16.1's "same hash twice" is unsatisfiable.

13. **Destructive reset in the wrong directory / on the committed fixture.**
    - *Detect:* `git clean -fd` removes untracked files outside the intended workspace, or `tests/fixtures/` shows up dirty in git status after a run.
    - *Recover:* operate only on a disposable copy of the fixture; gate every `reset --hard`/`clean -fd` behind the asserted CWD guard (refuse unless CWD is inside the copy). The committed fixture is read-only input, never the verifier's working tree.

---

## 10. Definition of Done

M1 is complete only when **every** condition holds:

**Local verification**
- [ ] `python -m velith.runner.spike --task <id> --seed 0` (in container) writes one complete episode (all §9.1 fields) to `./data/episodes/`.
- [ ] The episode `content_hash` verifies on read.
- [ ] Verify→log on a **recorded proposal** is reproducible: same verdict + same hash on two runs (D16.1).
- [ ] `PASSED`, `FAILED`, `PATCH_APPLY_FAILED`, `NO_PATCH` all reachable as logged outcomes (exit 0); `INFRA_ERROR` aborts non-zero, logged loudly.
- [ ] A live run against **real Ollama** produced a real verdict at least once (local acceptance).

**Docker verification**
- [ ] The spike runs in-container; the verdict is produced in-container.
- [ ] Episodes persist to the host and survive `--rm`.
- [ ] Ollama reached via `host.docker.internal`; failure path is loud (`ModelUnavailableError`).

**CI verification**
- [ ] `ruff check`, `ruff format --check`, `mypy src tests` (strict), `pytest` all green in CI.
- [ ] CI is hermetic: no Ollama, no network model dependency; the integration test touches no network.

**Repository state**
- [ ] Only the four permitted M0 files modified (plus optional Dockerfile `git`); all other M0 files unchanged.
- [ ] D16 already present in `DECISIONS.md` (committed before/with M1).
- [ ] No out-of-boundary code present (§11).
- [ ] All §5 commits landed atomically, none combined.

**Release readiness**
- [ ] `main` is green end to end.
- [ ] The milestone is tag-ready as `m1-complete`.
- [ ] `PROJECT_STATE.md`/`ROADMAP.md` updates (if part of the milestone-close process) reflect M1 done — performed per the existing documentation procedure, not invented here.

---

## 11. Implementation boundaries — belongs to M2 or later, must NOT appear in M1

- **M2:** network isolation of the test-execution step; bit-for-bit determinism hardening; flake detection/quarantine; pinned execution environment beyond what M0 provides; population of `secondary_passed`.
- **M3:** indexed/DB episode store; query-by-arm/seed/checkpoint; integrity scans beyond per-record hash.
- **M4:** dataset loader; real SWE-bench Verified tasks; train/held-out split; mechanically-enforced held-out lock; multiple tasks.
- **M5:** batch runner; arm A0 (cold); `MemoryPolicy` and any policy logic; model routing; cost guard; the non-saturating base-model condition (binds from M5, D16.5).
- **M6:** shared retrieval substrate; embedder; index.
- **M7:** A1/A2 write-filter policies; memory read/inject into the proposer.
- **M8:** frozen checkpointed held-out evaluation.
- **M9–M10:** experiment orchestrator; A0/A2 runs; statistics; go/no-go report; pre-registration freeze.
- **Anywhere later:** A3/A4 arms; second base model; discovery loop; self-improvement; cognitive plane; causal model; free-energy computation.

Any of the above appearing in an M1 commit is a boundary violation and must be removed before M1 can be declared complete.

---

*End of M1 Implementation Handoff. This is the execution contract for M1. Build strictly within it; raise any conflict with a frozen contract rather than resolving it silently. Do not proceed into M2.*