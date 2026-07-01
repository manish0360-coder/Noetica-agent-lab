# M1 — Engineering Specification

**Project:** Velith
**Milestone:** M1 — First propose → verify → log episode (the spike)
**Document type:** Engineering contract. Binding for the duration of M1. Conformant with `VISION.md`, `DECISIONS.md` (D1–D15), and the ratified M0–M10 roadmap (D12). Deviations from those are recorded in `DECISIONS.md`, never improvised.
**Depends on:** M0 (frozen, tagged `m0-complete`).
**Status:** Specification for review. **Not yet ratified for implementation** — see the open questions in the final section, several of which must be answered before code begins.
**Estimated effort:** 4–6 focused engineering days.

---

## 1. Purpose of M1

Deliver the irreducible core of the entire program: **one real engineering task in which a model proposes a solution, a containerized verifier disposes of it against a hidden check, and the outcome is persisted as a provenance-complete episode.** This is the smallest artifact that makes Velith's central loop real rather than designed.

If propose → verify → log does not work for a single task, nothing downstream (memory, arms, the compounding experiment) is buildable. M1 exists to prove the pipe is connected end to end, on the ground, before any of that weight is added.

M1 is a **spike**, not a system. It runs one task, uses one model, writes to a thin store, and stops. Breadth, scale, memory, and statistics are explicitly later milestones (§16).

---

## 2. Engineering goals

1. Introduce the **model-proposal** capability (Ollama integration, D13) as a bounded component, never as the architecture (D9).
2. Introduce the **verifier execution path** functionally — apply a candidate patch and run a hidden test suite inside the container — establishing the seam M2 will harden for determinism and isolation.
3. Define and persist the **Episode** record: a provenance-complete (I2) account of one task attempt, content-hashed for integrity.
4. Establish the **orchestrator** (`spike`) that wires proposer → verifier → store into one command.
5. Preserve M0's invariant: **the verdict is produced inside the container** (D3, §2 of M0 spec). The host is never the source of truth for a verdict.
6. Keep CI **hermetic and deterministic**: no model server in CI; the live model path is a local acceptance step, not a CI gate.

---

## 3. Definition of Done

M1 is done when **all** of the following hold. (Note: criterion 3 refines the roadmap's stated acceptance and is gated on Question Q1 in §20 — it is presented here as the recommended resolution, pending your ratification.)

1. `python -m velith.runner.spike --task <id> --seed 0`, run through the container, produces **one** JSON episode record on disk that survives container exit, containing every field in §9.1.
2. The episode record includes a **content hash** over its canonical content, and that hash verifies.
3. **Reproducibility (recommended scoping):** the **verify → log** path is deterministic — given a *recorded* proposal (fixed patch), re-running verification and logging twice yields the **same verdict and the same content hash**. Full proposal-level determinism (same seed + temperature 0 → identical patch) is *attempted and recorded* but is **not** a blocking criterion, for the reasons in §17 (R1) and Q1.
4. A **task outcome of "tests failed"** is a *successful* run of the loop (a valid grounded verdict logged), not an error. Only infrastructure failures (model unreachable, container fault) are errors.
5. All new unit and integration tests pass **inside the container**; the integration test uses a **mocked proposer** (no Ollama) and is fully hermetic.
6. `ruff check`, `ruff format --check`, `mypy src tests` (strict), and `pytest` all pass in the container and in CI, over the M0 + M1 code.
7. CI has **no** dependency on Ollama or any network model service.
8. `README.md` documents the M1 run command and the record/replay behavior.
9. The milestone is mergeable to a green `main` and tag-ready (`m1-complete`), with M0 unmodified.

---

## 4. Exact repository changes

Additions only. **No M0 file is modified except `core/config.py` (extended for model/store settings), `docker-compose.yml` (episode volume), and `README.md` (M1 usage).** M0's verifier image, CI gates, and packaging remain intact.

```
velith/
├── README.md                         (MODIFIED: add M1 usage)
├── docker-compose.yml                (MODIFIED: episode output volume; see §13)
├── .gitignore                        (MODIFIED: ignore data/episodes/)
├── src/velith/
│   ├── task.py                       (NEW: Task value type for the M1 fixture task)
│   ├── core/
│   │   └── config.py                 (MODIFIED: Ollama + store settings)
│   ├── llm/
│   │   ├── __init__.py               (NEW)
│   │   └── client.py                 (NEW: thin Ollama adapter — single seam, no routing)
│   ├── agent/
│   │   ├── __init__.py               (NEW)
│   │   └── proposer.py               (NEW: ProposerAgent)
│   ├── harness/
│   │   ├── __init__.py               (NEW)
│   │   └── verifier_sandbox.py       (NEW: VerifierSandbox — the M2 hardening seam)
│   ├── episodes/
│   │   ├── __init__.py               (NEW)
│   │   ├── episode.py                (NEW: Episode schema + content hash)
│   │   └── store.py                  (NEW: EpisodeStore — append-only JSONL)
│   └── runner/
│       ├── __init__.py               (NEW)
│       └── spike.py                  (NEW: orchestrator + CLI entrypoint)
└── tests/
    ├── fixtures/
    │   └── <task_id>/                (NEW: minimal buggy repo + hidden test; see §13/Q3)
    ├── unit/
    │   ├── test_episode.py           (NEW)
    │   ├── test_store.py             (NEW)
    │   ├── test_proposer.py          (NEW: mocked llm client)
    │   └── test_verifier_sandbox.py  (NEW: fixture patches, real local execution)
    └── integration/
        └── test_spike_episode.py     (NEW: mocked proposer, real verify→log, hermetic)
```

Directories for later milestones (`data/` loader, `memory/`, `eval/`) are **not** created in M1.

---

## 5. Required files & responsibilities

Single-responsibility per file (M0 §5 discipline continues).

| File | Responsibility | Must NOT contain |
|---|---|---|
| `task.py` | A typed value object describing the one M1 task: id, the working repo path/ref, the prompt material, the hidden-test invocation. | Dataset loading (M4); multiple tasks. |
| `llm/client.py` | A **thin** adapter over Ollama: given prompt + model + sampling params, return completion text plus call metadata (model+version, token counts, latency). | Routing, model selection policy, cost guard (M5); retries beyond a simple bounded one. |
| `agent/proposer.py` | `ProposerAgent`: turn a `Task` into a `Proposal` (a candidate patch + the exact prompt used + token/latency metadata) via `llm/client`. | Memory, retrieval, multiple attempts, self-critique. |
| `harness/verifier_sandbox.py` | `VerifierSandbox`: apply a candidate patch to the task's working tree and run the hidden test suite **inside the container**, returning a structured `Verdict`. The **single seam M2 hardens** (determinism, isolation, flake detection). | Network calls; the model; any scoring/judging by a model (D3 — deterministic only). |
| `episodes/episode.py` | The `Episode` schema (§9.1) and the canonical content-hash function (I2). | Storage I/O; querying. |
| `episodes/store.py` | `EpisodeStore`: append an episode to a JSONL file and read episodes back. | Indexing/DB (M3); arms/seeds querying logic beyond append/read. |
| `runner/spike.py` | Orchestrate proposer → verifier → store for one task; expose the `python -m velith.runner.spike` CLI; print the written episode path + a one-line summary. | Batch loops, multiple tasks, statistics, memory. |
| `core/config.py` (mod) | Extend `Settings` with Ollama host/model and episode output path. | Anything beyond validated config. |

---

## 6. Required modules

Conceptually, M1 introduces four collaborating components plus the orchestrator and two value types:

- **Value types:** `Task`, `Proposal`, `Verdict`, `Episode`.
- **Components:** `OllamaClient` (in `llm/client.py`), `ProposerAgent`, `VerifierSandbox`, `EpisodeStore`.
- **Orchestrator:** `spike` (function + CLI).

No other modules are in scope.

---

## 7. Public interfaces (contracts, not code)

Specified as contracts. Exact signatures are the implementer's to finalize within these contracts.

| Component | Operation | Inputs | Output | Contract |
|---|---|---|---|---|
| `OllamaClient` | `generate` | prompt, model, seed, temperature | completion text + metadata (model+version, prompt/completion token counts, latency) | Pure w.r.t. inputs except for model nondeterminism; raises a typed `ModelUnavailableError` on infra failure; never returns partial silent results. |
| `ProposerAgent` | `propose` | `Task`, `seed` | `Proposal` (candidate patch, exact prompt, token counts, latency, model+version) | Always returns a `Proposal`; if the model yields no usable patch, the `Proposal` carries an empty/`NO_PATCH` marker rather than raising. |
| `VerifierSandbox` | `verify` | `Task`, candidate patch | `Verdict` (state, raw test output, secondary_passed placeholder=None, duration) | Deterministic **given a fixed patch and fixed task** — the property M2 fully guarantees. **Determinism is achieved by execution isolation:** before each verification the sandbox restores the working tree to a clean state (`git reset --hard`, then `git clean -fd`) on a **disposable copy** of the fixture repository — never the committed fixture under `tests/fixtures/` — with an **asserted working-directory guard** executed before any destructive command (the sandbox refuses to reset/clean unless its CWD is confirmed to be inside the disposable copy). The **patch-apply mechanism is pinned to `git apply`**, and its failure maps to `PATCH_APPLY_FAILED` (a clean non-apply is an outcome, never an exception). A post-run reset is optional defense-in-depth, not required. Distinguishes outcome states (§10). Never raises on a test failure or a bad patch — those are verdict states. Raises only on infra fault (container/exec error). |
| `EpisodeStore` | `append` | `Episode` | written record location | Append-only; never mutates prior records; writes are durable to the mounted path before returning. |
| `EpisodeStore` | `read_all` | — | sequence of `Episode` | Returns every persisted episode; verifies content hashes on read (integrity, I2). |
| `spike` (CLI) | `--task <id> --seed <int>` | task id, seed | exit code + written episode path | Orchestrates the full loop; exit 0 on a completed loop (including a logged test-failure verdict); non-zero only on infra error. |

---

## 8. Internal interfaces

- **`ProposerAgent` → `OllamaClient`:** the proposer depends on the client abstraction, not on Ollama directly. This is the M5 routing seam; keep the dependency one-directional and narrow.
- **`spike` → components:** the orchestrator depends on `ProposerAgent`, `VerifierSandbox`, `EpisodeStore` through their public contracts only. It owns the control flow and the proposer/verifier hand-off; it must be the **only** place that knows the order of operations.
- **`Episode` construction:** `spike` assembles the `Episode` from the `Proposal` + `Verdict` + run context. `Episode` owns its own canonical hashing; no other module computes the hash.
- **Config access:** all components read configuration via the M0 `Settings` accessor; none read environment directly (M0 §7).
- **Logging:** all components log via the M0 structured logger; no `print` except the final human-facing summary line in the CLI (which may also be logged).
- **CLI / orchestration split:** `runner/spike.py` is split into two layers — an argument-parsing **CLI shell** (the `__main__`/entrypoint) that is a **terminal leaf imported by nothing**, and an **orchestration entry function** it wraps. The orchestration function may be imported **only** by the integration test (for mock-proposer injection, C8) and invoked by the entrypoint — it is imported by no other module in `src/`. This preserves the rule that the orchestrator is the single owner of operation order while keeping the loop testable without subprocess invocation.

---

## 9. Data flow

### 9.1 The Episode record (M1 fields)

The persisted episode must carry, at minimum:

- `task_id`
- `seed`
- `arm` — fixed to a single baseline value in M1 (the field **exists** for forward-compat with D7's arms; **no arm logic** is built here)
- `model` + `model_version`
- `prompt` (the exact text sent)
- `patch` (the candidate, possibly empty)
- `verdict_state` (§10) + `verdict_output` (raw hidden-test output)
- `secondary_passed` (placeholder `null` in M1; populated in M2)
- `prompt_tokens`, `completion_tokens`
- `latency_seconds` (proposal) and `verify_seconds` (verification) — the M1 "cost" signal; monetary cost is `null`/N/A for local Ollama but the field shape anticipates API models
- `timestamp` (UTC, ISO-8601)
- `content_hash` — SHA-256 over a **canonical serialization of the episode's content fields only** (see §9.1.1). The hash **excludes** volatile/timing provenance (`timestamp`, `latency_seconds`, `verify_seconds`) and excludes the `content_hash` field itself, so that the same recorded proposal yields the same hash (D16.1).
- `velith_version` / git ref (provenance)

M3 extends this schema (indexing, richer provenance); M1 must not omit any field above, because retrofitting provenance is the failure this program exists to avoid.

### 9.1.1 Canonical hashing and the hash boundary

The content hash must be stable across runs and machines, which a naive serialization does not guarantee (dict ordering, float/whitespace formatting, and non-ASCII handling all drift). The canonical rule is fixed:

- Serialize with `json.dumps(content, sort_keys=True, ensure_ascii=False, separators=(",", ":"))`, encoded as UTF-8, then SHA-256 the bytes.
- **Hash boundary (inside the hash):** `task_id`, `seed`, `arm`, `model`, `model_version`, `prompt`, `patch`, `verdict_state`, `verdict_output`, `secondary_passed`, `prompt_tokens`, `completion_tokens`, `velith_version`/git ref.
- **Excluded from the hash (recorded in the episode, but outside the boundary):** `timestamp`, `latency_seconds`, `verify_seconds`, and `content_hash` itself.
- The exact field set inside the boundary is **defined once, in `episode.py`**, and is the single authority; no other module recomputes or re-defines it.

Rationale: D16.1's blocking criterion is that a *recorded proposal* re-verified twice produces the **same verdict and the same hash**. Wall-clock timing fields vary run to run; including them in the hash would make that criterion unsatisfiable. Excluding them is therefore mandatory, not stylistic.

### 9.2 Flow (one task)

```
Settings → spike
  spike → Task (from fixture)
  spike → ProposerAgent.propose(Task, seed)
            ProposerAgent → OllamaClient.generate(prompt, model, seed, temp)  [reaches Ollama]
            ← Proposal(patch, prompt, tokens, latency, model+version)
  spike → VerifierSandbox.verify(Task, Proposal.patch)   [container: apply patch, run hidden tests]
            ← Verdict(state, output, duration)
  spike → Episode.build(Proposal, Verdict, context) → content_hash
  spike → EpisodeStore.append(Episode)   [durable write to mounted path]
  spike → print/log summary + episode path
```

---

## 10. Verdict taxonomy (M1)

A small, closed set of outcome states (final set pending Q7):

- `PASSED` — patch applied, hidden tests passed.
- `FAILED` — patch applied, hidden tests ran and did not pass. **A valid, successful loop outcome.**
- `PATCH_APPLY_FAILED` — the candidate patch did not apply cleanly. Logged outcome, not an error.
- `NO_PATCH` — the model produced no usable patch. Logged outcome, not an error.
- `INFRA_ERROR` — model unreachable, container/exec fault. **The only state that is an error** and aborts with a non-zero exit; still logged loudly before exit where possible.

The deterministic verifier (D3) decides `PASSED`/`FAILED`/`PATCH_APPLY_FAILED`. No model judges correctness anywhere in this path.

---

## 11. Error-handling strategy

- **Outcome vs. error.** The central discipline: a test failure or a bad patch is an *outcome* (a grounded verdict to log), never an exception. Infra problems (Ollama down, container fault) are *errors* that abort. Conflating these would corrupt the future compounding signal, where `FAILED` episodes are first-class learning data.
- **Fail fast, fail loud** on config and infra (continues M0 §10). Invalid config or an unreachable model raises immediately with an actionable message.
- **No silent `except`.** Caught exceptions are handled meaningfully or re-raised with context (M0 §10).
- **Typed errors.** Introduce a minimal exception taxonomy (e.g., `ModelUnavailableError`, `SandboxExecutionError`) under a `velith` base error. M1 grows the taxonomy minimally; later milestones extend it.
- **Partial-write safety.** An episode is written atomically (write-then-confirm) so a crash mid-write cannot leave a half-record that fails hash verification on read.

---

## 12. Logging expectations

- Structured logging only (M0 §9); the one human-facing `print` is the final CLI summary.
- Emit `INFO` at each loop stage: task loaded, proposal received (with token counts), verification started/completed (with verdict state), episode written (with path + hash).
- Log the **verdict state** and **timings**, never the raw model completion at `INFO` (keep large payloads to `DEBUG`).
- No secrets in logs (M0 §9). With local Ollama there are none; the rule stands for future API keys.
- This logging is the seed of the M3 episode/trace provenance; keep keys consistent and machine-parseable.

---

## 13. Docker implications

- **The verifier execution path becomes real.** `VerifierSandbox` applies a patch and runs tests in the container. For the M1 fixture task this needs only `git` (for patch apply) and `pytest` (already present); confirm `git` is in the image (may be a one-line Dockerfile addition — an M1-permitted modification to the build, see §4).
- **Episode persistence requires a volume.** M0 ran throwaway containers (`--rm`). M1 must persist episodes to the host: add a bind-mount (e.g. host `./data/episodes/` → container path) in `docker-compose.yml`, and gitignore it. Without this, episodes die with the container and DoD-1 fails.
- **Model reachability.** The spike's proposal step must reach Ollama (host service). For M1 the run container is **network-enabled** to reach Ollama (e.g. via host networking / `host.docker.internal`, platform-dependent — see Q2). **This network access is an accepted M1 condition, not the final state:** M2 introduces network isolation *for the test-execution step specifically* (R3/§15).
- **Run path.** The spike is invoked via a command override on the existing service (recommended) rather than a new service, to avoid service sprawl: `docker compose run --rm verifier python -m velith.runner.spike --task <id> --seed 0`. The default verifier `command` (pytest) is unchanged. Final shape pending Q2.

---

## 14. CI implications

- **CI stays hermetic.** Ollama is **never** invoked in CI. The integration test (`test_spike_episode.py`) injects a **mocked proposer** returning fixed patches (one that passes the hidden test, one that fails, one malformed), and exercises the real `VerifierSandbox` + `EpisodeStore`. This proves the verify → log path deterministically without a model. (This mirrors the mocked-model integration pattern already proven in the MiniNoetica reference work — the technique transfers; D11.)
- **No new CI services.** CI continues to run the four containerized gates; M1 only adds tests beneath them. No model server, no network model dependency.
- **The live end-to-end run (real Ollama) is a documented *local* acceptance step**, executed by the engineer to satisfy DoD-1, not a CI gate. CI green + local live-run success together certify M1.
- The corrected M0 CI workflow is reused unchanged in structure; only the test surface grows.

---

## 15. Security considerations

- **Execution of untrusted generated code.** The candidate patch and the task's tests are executed in the container — this is the primary risk surface. M1 mitigations: run only inside the container (isolation boundary), enforce a **wall-clock timeout** on test execution (prevent infinite loops / hangs), and treat the container as disposable (`--rm`). **Full network isolation of the test-execution step is deferred to M2** and is explicitly an accepted M1 risk (R3).
- **Network exposure during M1.** Because the run container has network access (for Ollama), generated code executed in the same run could, in principle, reach the network. Accepted for M1 with a controlled fixture task; closed in M2 by isolating the test step from the network. Documented, not hidden.
- **Task content is data, not instructions.** The prompt incorporates task text; a malicious task could attempt prompt injection. M1 uses a controlled fixture (low risk), but the principle — task/observed content is never treated as instructions to the system — is stated now for when real tasks arrive at M4.
- **Secrets.** None in M1 (local Ollama, no keys). The rule stands: any future API keys come from environment, never committed, never logged (M0 §7/§9).
- **Episode integrity.** The content hash makes episode tampering detectable on read (I2). Store writes are append-only; no in-place mutation.

---

## 16. Future compatibility with M2

M2 is "deterministic, hardened verifier." M1 must make M2 a *hardening*, not a *rewrite*:

- **`VerifierSandbox.verify` is the single seam.** Keep patch-apply and test-execution inside one clearly bounded method so M2 can wrap it with: pinned execution environment, network isolation of the test step, fixed timeouts, and the flake detector — without touching proposer, store, or orchestrator.
- **`Verdict` already carries `secondary_passed` (null in M1).** M2 populates it (held-out secondary tests, the software model-gap detector). No schema change required.
- **Determinism contract.** M1 establishes "verdict is deterministic given a fixed patch"; M2 guarantees it bit-for-bit and adds flake quarantine. The M1 record/replay capability (Q1) is what M2 builds its determinism tests on.
- **Episode schema** is provenance-complete now; M3 extends storage/indexing without altering the M1 fields.
- **Arm/seed fields exist** (D7) though unused; M5–M7 add arm logic with no schema migration.

---

## 17. Risks

| ID | Risk | Severity | Mitigation |
|---|---|---|---|
| R1 | **LLM nondeterminism** breaks "same seed + temp 0 → same verdict." Ollama at temp 0 is not guaranteed bit-identical across runs/hardware, and small patch differences can flip a verdict. | High | Scope DoD reproducibility to the **verify→log path given a recorded proposal** (record/replay); attempt but do not *gate* on proposal-level determinism. **Requires ratification — Q1.** |
| R2 | **SWE-bench task heaviness.** Real tasks carry per-task dependency environments; standing one up could blow the 4–6 day budget. | Med | Use a **minimal representative fixture** task for M1; real SWE-bench arrives at M4. **Q3.** |
| R3 | **Untrusted code + network access** in the same M1 container. | Med | Timeout + disposable container now; full network isolation of the test step in M2. Accepted, documented. |
| R4 | **Ollama reachability from container** is platform-specific (WSL2/Docker Desktop networking). | Med | Resolve host/network approach up front — Q2; document the exact mechanism in README. |
| R5 | **Scope creep** into memory/arms/multiple tasks "while wiring the loop." | Med | §19 non-goals are binding; commit boundaries (§18) keep each step minimal. |
| R6 | **Patch format mismatch** (model emits prose/markdown around a diff; diff doesn't apply). | Med | `PATCH_APPLY_FAILED` is a first-class verdict, not a crash; proposer does minimal extraction only — no elaborate parsing (that invites the MiniNoetica `analyze()` debt). |
| R7 | **Premature LLM abstraction** (`llm/client.py`) over-built into a routing framework. | Low | Keep it a thin adapter; routing/cost-guard are explicitly M5. **Q4.** |

---

## 18. Commit boundaries

Atomic commits, each leaving lint/type/test green where feasible:

1. `feat: episode schema + content hash` — `episodes/episode.py` + `tests/unit/test_episode.py`.
2. `feat: episode store (jsonl, append-only)` — `episodes/store.py` + `tests/unit/test_store.py`.
3. `feat: task type + minimal fixture` — `task.py` + `tests/fixtures/<task_id>/`.
4. `feat: verifier sandbox` — `harness/verifier_sandbox.py` + `tests/unit/test_verifier_sandbox.py` (real local execution against fixture patches); Dockerfile `git` addition if needed.
5. `feat: ollama client (thin adapter)` — `llm/client.py` + mocked unit test.
6. `feat: proposer agent` — `agent/proposer.py` + `tests/unit/test_proposer.py` (mocked client).
7. `feat: spike orchestrator + CLI` — `runner/spike.py`; `core/config.py` extension.
8. `test: hermetic spike integration` — `tests/integration/test_spike_episode.py` (mocked proposer, real verify→log).
9. `build: episode volume + gitignore` — `docker-compose.yml`, `.gitignore`; confirm CI green.
10. `docs: M1 run + record/replay usage` — `README.md`.

---

## 19. Explicit non-goals

Out of scope for M1. Building any of these is scope creep and a deviation:

- **No retrieval, no memory, no experiment arms (A0–A4).** (M5–M7.)
- **No multiple tasks, no dataset loader, no held-out lock.** (M4.)
- **No batch runner.** (M5.)
- **No statistics, no checkpoints, no frozen evaluation.** (M8–M10.)
- **No full cost guard** beyond a basic execution timeout/token-count record. (M5.)
- **No network isolation / bit-for-bit determinism hardening / flake detector.** (M2.)
- **No indexed/DB episode store.** M1 is append-only JSONL. (M3.)
- **No second model, model routing, or distillation.** (M5/L1 later.)
- **No model-based judging anywhere** (D3 — permanently out of the verifier; the only model role is *proposing*).
- **No CI Ollama integration.** CI stays hermetic.
- **No M2 work.** M1 stops at a logged episode from one task.

---

## 20. Milestone checklist

- [ ] `task.py` + minimal fixture task created.
- [ ] `llm/client.py` thin Ollama adapter created (mocked-tested).
- [ ] `agent/proposer.py` returns a `Proposal` for the task (mocked-tested).
- [ ] `harness/verifier_sandbox.py` applies a patch and runs hidden tests in-container, returning a `Verdict`.
- [ ] `episodes/episode.py` schema + content hash.
- [ ] `episodes/store.py` append-only JSONL store.
- [ ] `runner/spike.py` orchestrates the loop and exposes the CLI.
- [ ] `core/config.py` extended (Ollama + store path); `docker-compose.yml` episode volume; `.gitignore` updated.
- [ ] Dockerfile has `git` if patch-apply requires it.
- [ ] README documents the M1 command + record/replay.

## 21. Verification checklist

- [ ] `python -m velith.runner.spike --task <id> --seed 0` (in container) writes one complete episode (all §9.1 fields) that **survives container exit**.
- [ ] Episode `content_hash` verifies on read.
- [ ] Verify→log path on a **recorded proposal** is deterministic (same verdict + same hash twice). *(Q1-gated.)*
- [ ] A `FAILED` verdict run completes with exit 0 and a logged episode (outcome, not error).
- [ ] `PATCH_APPLY_FAILED` and `NO_PATCH` are logged outcomes, not crashes.
- [ ] `INFRA_ERROR` (simulate Ollama down) aborts non-zero, logged loudly.
- [ ] All new unit + integration tests pass **in the container**; integration test is hermetic (no Ollama).
- [ ] `ruff check`, `ruff format --check`, `mypy src tests` (strict), `pytest` green locally and in CI.
- [ ] CI has no Ollama/network-model dependency.
- [ ] M0 files unmodified except the three permitted (`config.py`, `docker-compose.yml`, `README.md`, plus optional Dockerfile `git`).
- [ ] Live end-to-end run against real Ollama produces a real verdict at least once (local acceptance).

## 22. Questions that must be answered before implementation begins

These are genuine, unresolved decisions. Several touch the ratified M1 acceptance (D12) and so require your ruling — I will not redesign them unilaterally.

- **Q1 (ratification required).** The roadmap's M1 acceptance reads "same seed + temperature 0 → same verdict." Per R1, full LLM proposal determinism is not reliably achievable with Ollama. **Do you ratify the refinement** — that M1's *blocking* reproducibility is the **verify→log path given a recorded proposal**, with proposal-level determinism attempted-and-recorded but non-blocking? If yes, this is recorded as a `DECISIONS.md` clarification, not a redesign. If no, we must discuss how to achieve true proposal determinism before coding.
- **Q2 (orchestration & networking).** Run the spike **in the container** (network-enabled to reach Ollama via host) — recommended, since host Python is 3.10 and not a build target — or on the host? And which concrete Ollama-reachability mechanism for WSL2 + Docker Desktop (`host.docker.internal` vs host networking)?
- **Q3 (M1 task).** Use a **minimal representative fixture** task (recommended; real SWE-bench at M4), or stand up a real SWE-bench Verified task now? The former protects the 4–6 day budget.
- **Q4 (LLM seam).** Confirm the **thin `llm/client.py` adapter** now (recommended — it is the M5 routing seam at first genuine use), versus inlining Ollama calls in the proposer.
- **Q5 (model choice).** Which Ollama model for M1 (e.g. a small local coder model already pulled)? Note: the **non-saturating base-model condition (D8) applies to the experiment (M5+), not to M1** — M1 only needs a model that can sometimes emit a valid patch. Final pick is yours based on what's installed.
- **Q6 (episode path).** Confirm the host episode directory (recommended `./data/episodes/`, gitignored) and JSONL filename convention.
- **Q7 (verdict taxonomy).** Confirm the §10 verdict states are complete and correctly named before they are encoded into the schema and tests.

---

## 23. Ratification status & binding fixture requirement

**Ratification.** Q1–Q7 are **resolved and ratified** via `DECISIONS.md` D16 (D16.1–D16.7). This specification is **approved for implementation**. The cross-review edits (canonical hashing with an explicit volatile-field-excluding boundary, the disposable verifier workspace with clean-state guarantee and CWD guard, the pinned `git apply` and its `PATCH_APPLY_FAILED` semantics, the CLI-shell vs. orchestration-function split, and the deterministic-fixture requirement below) are incorporated into §7, §8, and §9.1.1.

**Fixture determinism (binding).** The M1 fixture's hidden test must be deterministic: the **unpatched** repository must fail it **consistently** across repeated runs (no time-, network-, or random-dependence). Verifier-level isolation (§7) makes the *sandbox* deterministic, but a flaky fixture test makes the *verdict* nondeterministic regardless. Fixture-level nondeterminism is disqualifying and must be caught at C3 — run the unpatched repo's hidden test repeatedly and confirm a stable failure before proceeding.

---

*End of M1 Engineering Specification. Ratified for implementation per D16; cross-review edits incorporated. Do not proceed to M2.*