# PROJECT STATE

**Project:** Velith
**Document type:** Living status record. Captures the repository's *verified* state at each
milestone boundary. Updated at milestone close, never improvised mid-implementation.
**Last updated:** 2026-06-25
**Current tag:** `m1-complete`
**Branch:** `main` — green end to end, pushed.

---

## 1. Current state

**M0 — complete and certified** (`m0-complete`). Containerized skeleton: pinned Docker build,
in-container pytest, a single validated `Settings` object, structured logging, and hermetic CI
green from a fresh clone. The foundation every later milestone assumes.

**M1 — complete and certified** (`m1-complete`). The irreducible core of the program is now real
on the ground: for a single engineering task, a local model **proposes** a candidate patch, a
containerized verifier **disposes** of it against a hidden test, and the outcome is persisted as a
provenance-complete, content-hashed **episode** that survives container exit. The central
`propose → verify → log` loop is connected end to end and reproducible.

M1 is a spike, not a system: one fixture task, one model, an append-only JSONL store. Breadth,
scale, memory, experiment arms, and the compounding experiment are explicitly later milestones and
were deliberately not built.

## 2. M1 objectives and achievements

Every M1 engineering goal was met:

- **Model-proposal capability** introduced as a bounded component — a thin Ollama adapter over
  stdlib `urllib`, never the architecture (D9, D16.4).
- **Verifier execution path** made real — apply a candidate patch with pinned `git apply` and run
  the hidden test suite inside the container, returning a structured `Verdict`. This is the single
  seam M2 will harden (network isolation, flake detection, bit-for-bit determinism).
- **Provenance-complete `Episode`** — all M1 spec §9.1 fields, with a SHA-256 content hash over a
  canonical serialization (sort-keys, tight separators, UTF-8) that excludes volatile timing,
  protecting D16.1.
- **Orchestrator (`spike`)** — wires proposer → verifier → store into one CLI command and is the
  single owner of operation order (§8); CLI shell split from the importable orchestration function.
- **M0 invariant preserved** — the verdict is produced inside the container; the host is never the
  source of truth (D3).
- **CI stays hermetic** — no model server in CI; the live model path is a documented local
  acceptance step, not a gate.

**Definition of Done — all satisfied.** A live in-container run wrote one complete episode that
survived `--rm` with a verifying hash; the verify→log path is reproducible for a recorded proposal
(same verdict and same hash); all four grounded verdicts (`PASSED`, `FAILED`, `PATCH_APPLY_FAILED`,
`NO_PATCH`) are reachable as exit-0 outcomes and `INFRA_ERROR` aborts non-zero and logs loudly; the
four gates (`ruff check`, `ruff format --check`, `mypy --strict`, `pytest`) are green in the
container; only the permitted M0 files were modified; the milestone is tagged.

## 3. Repository status

M1 added, alongside the M0 skeleton:

```
src/velith/
├── task.py                       # Task value type + single-fixture loader
├── episodes/{episode,store}.py   # Episode schema + content hash; append-only JSONL store
├── harness/verifier_sandbox.py   # Deterministic verifier (the M2 hardening seam)
├── llm/client.py                 # Thin Ollama adapter (the M5 routing seam)
├── agent/proposer.py             # ProposerAgent + minimal patch extraction
└── runner/spike.py               # Orchestrator + CLI
tests/
├── unit/{test_episode,test_store,test_task,test_verifier_sandbox,test_proposer}.py
├── integration/test_spike_episode.py   # hermetic, mocked proposer, real verify→log
└── fixtures/calc_add_bug/        # minimal buggy repo + deterministic hidden test
```

Permitted M0 modifications used: `core/config.py` (M1 settings), `docker-compose.yml` (episode
bind-mount + `host.docker.internal`), `.gitignore` (`/data/episodes/`), `README.md` (M1 usage), and
`docker/verifier.Dockerfile` (`git`). No other M0 source or build file was changed.

**Commit ledger (atomic, conventional, none combined):**

| Commit | Subject |
|---|---|
| `539a770` | feat: episode schema + content hash (C1) |
| `f4eb74c` | fix: replace ambiguous en dash with ASCII hyphen (RUF003) |
| `4fd365d` | feat: episode store, jsonl append-only (C2) |
| `fb5fec1` | feat: task type + minimal fixture (C3) |
| `a424499` | feat: verifier sandbox (C4) |
| `7d7b787` | feat: ollama client, thin adapter (C5) |
| `df9bae7` | feat: proposer agent (C6) |
| `b165219` | feat: spike orchestrator + CLI (C7) |
| `f399e7e` | fix: normalize verifier output timing for reproducible content hash (D16.1) |
| `dd30f5c` | test: hermetic spike integration (C8) |
| `59ddd14` | build: episode volume + gitignore (C9) |
| `ffed330` | docs: M1 run + record/replay usage (C10) |

**Live acceptance:** model `qwen2.5:3b`, verdict `NO_PATCH`, `hash_ok = True`, exit 0, episode
persisted — a valid grounded outcome confirming the loop end to end. The `INFRA_ERROR` path was
independently exercised (a reasoning model exceeding the request timeout produced a loud non-zero
abort with no episode written).

## 4. Known limitations and deferred work

Recorded for the M2 team; full categorization is in the M1 close-out review. Highlights:

- The proposer's prompt is the task's prompt material only (no source embedded), so a live run may
  not produce an applying patch — by design (the dataset/prompt enrichment is M4). Grounded
  outcomes (`NO_PATCH`/`PATCH_APPLY_FAILED`) are still logged and correct.
- Patch extraction is deliberately minimal; diffs wrapped in non-standard headers (e.g. a
  `git format-patch` header) are treated as `NO_PATCH`.
- The exception taxonomy (`ModelUnavailableError`, `SandboxExecutionError`, `EpisodeIntegrityError`)
  is not yet unified under a shared base error.
- `Episode` still emits the benign pydantic `model_`-namespace warning (`Completion` and `Proposal`
  set `protected_namespaces=()`; `Episode` does not). Non-fatal, but noise in gate output.
- `velith_version` provenance uses the package version; a git ref is unavailable at runtime
  in-container (the image copies sources, not `.git`).
- The default Ollama request timeout (120s) is too short for multi-minute reasoning models; it is
  configurable via `VELITH_OLLAMA_TIMEOUT_SECONDS`.

## 5. Readiness for M2

M2 is the **deterministic, hardened verifier**: network isolation of the test-execution step,
fixed/pinned execution environment, flake detection and quarantine, bit-for-bit determinism, and
population of the `secondary_passed` field (the software model-gap detector).

The M1 verifier was built so M2 is a *hardening, not a rewrite*: patch-apply and test execution sit
inside one bounded `VerifierSandbox.verify` method that M2 can wrap; the disposable-workspace and
reset-before-run discipline is already in place; `secondary_passed` is present and `null`; and the
record/replay reproducibility surface (D16.1) that M2 builds its determinism tests on is proven. No
M1 work blocks M2.

**Repository is M2-ready.** Begin M2 only against its own ratified engineering specification and
implementation handoff, in the same atomic, gate-verified workflow used for M1.
