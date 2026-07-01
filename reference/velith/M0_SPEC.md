# M0 — Engineering Specification

**Project:** Velith
**Milestone:** M0 — Project skeleton & environment validation
**Document type:** Engineering contract. Binding for the duration of M0. Implementation must conform to this specification; deviations are recorded in `DECISIONS.md`, not improvised.
**Status:** Ratified for execution.
**Date:** 2026-06-20
**Estimated effort:** 1–2 focused engineering days.

**Naming note.** The Python package is `velith` (the repo is `velith/`). The ratified M0–M10 roadmap was authored under the earlier working name and used `noetica/` paths; per D11 (Velith is a new repository with zero coupling to the MiniNoetica reference), the package is named `velith` to prevent confusion with the MiniNoetica codebase. This is a naming alignment, not an architectural change.

---

## 1. Objective

Prove that the full toolchain runs end-to-end on the verified environment **before any agent, model, dataset, or verification logic exists**. M0 produces a minimal, runnable repository skeleton in which a **containerized verifier process executes one trivial sanity check and reports green through CI on a fresh clone**.

M0 is deliberately the smallest possible milestone. Its purpose is not capability — it is *de-risking the foundation* that every subsequent milestone assumes: Docker builds, the Linux container runs Python, pytest executes inside the container, configuration loads, structured logging works, and CI reproduces all of it from a clean checkout. If any of these is broken, it must be discovered now, not under the experimental harness.

M0 does **not** build the real verifier. It builds the *container shell* that M2 will later harden into the deterministic SWE verifier. The sanity check inside it is a placeholder whose only job is to prove the pipe is connected.

---

## 2. Success criteria

M0 succeeds if and only if all of the following are true:

1. **One-command run.** From a fresh clone on the verified environment, a single documented command builds the container and runs the sanity check to green, with **zero manual setup steps** beyond that command and the documented prerequisites.
2. **Containerized execution.** The sanity check runs *inside the Docker container*, not on the host Python. (This is non-negotiable: M2's determinism guarantee depends on the verifier always running in the container, and that discipline starts here.)
3. **CI parity.** The same build-and-test sequence runs in CI on every push and reproduces the green result with no environment-specific patching.
4. **Config loads and validates.** The configuration object loads from environment, validates, and fails loudly with a clear message on invalid input.
5. **Structured logging emits.** A structured log line is produced by the sanity path, demonstrating the logging foundation is wired (observability is first-class from the first commit, per D9).
6. **Lint and type gates pass.** `ruff` (lint + format check) and `mypy` (strict) pass on the entire (small) codebase, locally and in CI.

If any criterion fails, M0 is **not done**, regardless of how close the rest is.

---

## 3. Deliverables

1. A runnable repository skeleton (`velith/`) with the structure in §4.
2. A Docker container definition that builds a Linux image capable of running the project's Python and pytest.
3. A `docker compose` service (`verifier`) that runs the sanity check inside that container.
4. One sanity test that proves the container executes pytest successfully.
5. One configuration module (`config.py`) with a validated settings object.
6. One logging module establishing structured logging.
7. A CI workflow that builds the image, runs lint/type/test, and gates on green.
8. Project metadata (`pyproject.toml`) with pinned tool versions and dependency declarations.
9. Pre-commit hooks for lint/type/format.
10. A `README.md` documenting the single run command and the environment prerequisites.
11. A `.gitignore` and an `.env.example` (no secrets committed).

No other deliverables. Anything beyond this list is out of scope (§13).

---

## 4. Repository structure to create

Only what M0 requires. The tree is intentionally minimal; later milestones add to it.

```
velith/
├── README.md
├── pyproject.toml
├── .gitignore
├── .env.example
├── .pre-commit-config.yaml
├── docker-compose.yml
├── docker/
│   └── verifier.Dockerfile
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── velith/
│       ├── __init__.py
│       └── core/
│           ├── __init__.py
│           ├── config.py
│           └── logging.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── sanity_test.py
```

Directories named in the M0–M10 roadmap for later milestones (`agent/`, `harness/`, `episodes/`, `data/`, `memory/`, `eval/`, `runner/`) are **not** created in M0. They are introduced by the milestone that first needs them, to avoid empty-folder scaffolding that implies unbuilt structure.

---

## 5. File-by-file responsibilities

Each file has a single responsibility. If a file starts doing two things, the boundary is wrong.

| File | Responsibility | Must NOT contain |
|---|---|---|
| `README.md` | The one run command, the environment prerequisites, and how to interpret a green result. | Architecture, vision, roadmap (those live in their own docs). |
| `pyproject.toml` | Package metadata, dependency declarations, and pinned versions of `ruff`, `mypy`, `pytest`. Tool configuration (ruff/mypy/pytest settings). | Application logic. |
| `.gitignore` | Exclude `.env`, `__pycache__`, build artifacts, virtualenvs, caches. | — |
| `.env.example` | Document the expected environment variables with placeholder values. | Real secrets or real values. |
| `.pre-commit-config.yaml` | Wire `ruff` (lint+format) and `mypy` as pre-commit hooks. | Heavy/slow hooks that discourage committing. |
| `docker-compose.yml` | Define the `verifier` service that builds from the Dockerfile and runs the sanity check inside the container. | Multiple services, databases, networks (none needed in M0). |
| `docker/verifier.Dockerfile` | Build a Linux image with the project's Python and dependencies installed; set the working directory; default to running pytest. | Any SWE/verification logic (that is M2). Any model or dataset. |
| `.github/workflows/ci.yml` | On push/PR: build the image, run lint, type-check, and the sanity test; gate the build on green. | Deployment, publishing, secrets-dependent steps. |
| `src/velith/__init__.py` | Mark the package; expose version. | Logic. |
| `src/velith/core/__init__.py` | Mark the subpackage. | Logic. |
| `src/velith/core/config.py` | Define a single validated `Settings` object (pydantic) sourced from environment; fail loudly on invalid config. | Business logic, I/O beyond reading config, global mutable state. |
| `src/velith/core/logging.py` | Configure structured logging; expose a single accessor for a configured logger. | `print` statements anywhere in the project; per-module ad-hoc logging config. |
| `tests/conftest.py` | Shared pytest fixtures (minimal in M0). | Test logic. |
| `tests/sanity_test.py` | One test proving the container runs pytest and that config + logging import and function. | Any agent/model/dataset/verifier assertions. |

---

## 6. Development environment assumptions

Per D13, the build and runtime environment is fixed:

- **OS / runtime:** WSL2 + Ubuntu. All container builds and test execution occur in the Linux environment, not native Windows.
- **Python:** 3.12 (the Velith target). The MiniNoetica reference repo's Python 3.10 is *not* inherited.
- **Container:** Docker (verified). The sanity check runs inside the container; the host Python is used only for editor tooling and pre-commit, never as the source of truth for a verdict.
- **Version control:** Git, with the workflow in §11.
- **Ollama:** installed and verified, but **not used in M0** (no model calls until M1). Its presence is assumed for later milestones only.
- **Pinning:** Python tool versions (`ruff`, `mypy`, `pytest`) are pinned in `pyproject.toml`; the container base image is pinned to a specific tag (no `latest`). Reproducibility starts at M0.

The README must state these prerequisites so a second engineer (or future you) reproduces the environment without guesswork.

---

## 7. Coding standards

- **Formatting & linting:** `ruff` is the single source for both lint and format. Code must pass `ruff check` and `ruff format --check` clean.
- **Typing:** Full type annotations on all functions and public attributes. `mypy` runs in **strict** mode and must pass with zero errors. "The libraries handle it" is not a reason to skip annotations.
- **Configuration:** Configuration is a single validated `pydantic` `Settings` object. No scattered `os.getenv` calls, no magic numbers or environment reads buried in modules.
- **No `print`:** All diagnostic output goes through the structured logger (§9). A `print` statement is a defect in this project.
- **Module discipline:** Small, single-responsibility modules. No god-modules. If a module exceeds one clear responsibility, split it.
- **No global mutable state.** Configuration and the logger are constructed and passed/accessed through defined accessors, not mutated globally.
- **Naming:** Clear, intention-revealing names. Code is read far more than written; optimize for the reader who forgot everything in 18 months.

These standards are enforced mechanically (pre-commit + CI), not by good intentions.

---

## 8. Testing strategy

M0 has a deliberately tiny test surface, but the *discipline* it establishes is permanent.

- **The single load-bearing test** is the sanity test, and it must run **inside the container**. The acceptance command builds the image and executes pytest within it. A test that passes on the host but is never run in the container does not satisfy M0 — because the entire point is to prove the *containerized* execution path.
- **What the sanity test asserts:** (a) pytest executes successfully inside the container; (b) `Settings` loads and validates; (c) the logger is constructed and emits a structured line. Nothing about agents, models, datasets, or verification — those do not exist yet.
- **Test placement:** all tests under `tests/`, discoverable by pytest configured in `pyproject.toml`.
- **CI runs the tests through the same containerized path as local**, so "passes on my machine" and "passes in CI" are the same execution, not two different ones.
- **No mocking is required in M0** (nothing external is called). Mocking discipline begins at M1 when the LLM enters.

---

## 9. Logging requirements

Observability is a first-class deliverable from the first commit (D9), so logging is set up in M0 even though the system does almost nothing.

- **Structured logging.** Log records are structured (key/value or JSON-capable), not free-text `print`. The format must be machine-parseable so later milestones can build the episode store and traces on the same foundation.
- **Single configuration point.** Logging is configured once, in `core/logging.py`, and accessed through one accessor. No module configures logging on its own.
- **Levels.** Standard levels used correctly: `DEBUG` for development detail, `INFO` for normal lifecycle events, `WARNING`/`ERROR` for problems. M0's sanity path emits at least one `INFO` line proving the pipe works.
- **No secrets in logs.** Configuration values that could be sensitive are never logged.
- **Foundation only.** M0 does not build trace correlation, episode logging, or provenance fields — those arrive with the episode store (M3). M0 only proves structured logging *exists and emits*.

---

## 10. Error-handling philosophy

- **Fail fast, fail loud at startup.** Invalid configuration must raise immediately at construction with a clear, actionable message — never silently default to a wrong value. A misconfigured system must refuse to start, not run incorrectly.
- **No silent `except`.** Bare `except:` and swallowed exceptions are defects. Caught exceptions are either handled meaningfully or re-raised with context.
- **Typed errors foundation.** Where M0 needs to signal a failure (e.g., bad config), it does so through clear exceptions; the project's exception taxonomy will grow in later milestones but begins with the principle that errors are explicit and informative.
- **Container/CI failures surface, not hide.** If the container build or the sanity run fails, the command and CI must exit non-zero with the underlying cause visible. A green that masks a failure is worse than a red.

M0's error surface is small (config and container), but the philosophy it sets — explicit, loud, non-silent — is the one every later milestone inherits.

---

## 11. Git workflow for M0

- **Trunk-based, solo-disciplined.** `main` is the trunk and is always green. Work happens on short-lived branches (e.g. `m0/skeleton`) merged into `main` only when CI is green; for a solo operator, direct small commits to a working branch then a single reviewed merge is acceptable, provided `main` never holds a red state.
- **CI gates merges.** No merge to `main` while CI is red. The fresh-clone-green property is the project's heartbeat and must never be broken on the trunk.
- **Conventional commit messages.** Commits use a clear convention (e.g. `feat:`, `chore:`, `ci:`, `test:`, `docs:`) so history is readable.
- **Milestone tag.** When M0's Definition of Done (§14) is met, tag the commit (e.g. `m0-complete`). Tags mark milestone boundaries for the record.
- **No secrets in history.** `.env` is gitignored; only `.env.example` is committed. If a secret is ever committed, it is rotated, not merely deleted.

---

## 12. Commit boundaries

M0 is small enough to land in a handful of atomic commits, each leaving the repo in a coherent state. Recommended boundaries, in order:

1. **`chore: initialize repo metadata`** — `pyproject.toml`, `.gitignore`, `.env.example`, `README` stub. Repo installs/parses.
2. **`feat: configuration object`** — `core/config.py` with the validated `Settings`. Includes its unit coverage in the sanity test or a dedicated config test.
3. **`feat: structured logging foundation`** — `core/logging.py` and its accessor.
4. **`test: sanity test`** — `tests/conftest.py`, `tests/sanity_test.py` (passes on host first to prove the test itself is sound).
5. **`build: containerized verifier shell`** — `docker/verifier.Dockerfile`, `docker-compose.yml`; the sanity test now runs inside the container.
6. **`ci: pipeline`** — `.github/workflows/ci.yml` running build + lint + type + test; green on push.
7. **`chore: pre-commit hooks`** — `.pre-commit-config.yaml`.
8. **`docs: README run command and prerequisites`** — finalize the README so a fresh clone is reproducible from documentation alone.

Each commit should leave lint/type/test in a passing state wherever feasible; commit 5 is the one that flips the canonical execution from host to container.

---

## 13. Out of scope for M0

Explicitly **not** built in M0. Building any of these here is scope creep and a deviation:

- No LLM calls, no Ollama integration, no model adapter.
- No agent, proposer, or any reasoning logic.
- No dataset loading, no SWE-bench, no tasks.
- No real verification logic — only the trivial sanity check. The actual deterministic SWE verifier is **M2**.
- No episode schema, no episode store, no JSONL/DB persistence (that is **M1/M3**).
- No memory, retrieval, embeddings, or experiment arms.
- No cost guard, batch runner, evaluator, or orchestrator.
- No M1 work of any kind. M0 stops at a green containerized sanity check.
- No databases, message queues, or additional services in `docker-compose`.
- No CI deployment/publishing steps.

---

## 14. Definition of Done

M0 is done when **every** box is checked:

- [ ] Fresh clone on WSL2/Ubuntu, with documented prerequisites, runs **one documented command** and reaches green with zero additional manual steps.
- [ ] The sanity check executes **inside the Docker container** (not host Python).
- [ ] CI builds the image and runs lint + `mypy --strict` + the sanity test, green, on push.
- [ ] `Settings` loads, validates, and fails loudly on invalid input.
- [ ] Structured logging is configured once and emits at least one `INFO` line on the sanity path.
- [ ] `ruff check`, `ruff format --check`, and `mypy` pass clean locally and in CI.
- [ ] Pre-commit hooks are installed and enforce lint/type/format.
- [ ] `README.md` documents the prerequisites and the single run command; no other doc is required to reproduce.
- [ ] No secrets in the repo or history; only `.env.example` is committed.
- [ ] Tool and base-image versions are pinned.
- [ ] The commit at completion is tagged (e.g. `m0-complete`).

If all boxes are checked, M0 is banked and M1 may be specified. Not before.

---

## 15. Common implementation mistakes to avoid

- **Running pytest on the host and calling it done.** The whole point of M0 is the *containerized* path; a green host run that never enters the container fails the milestone's purpose and hides container problems until M2.
- **Building more than the skeleton.** Adding an LLM call, a dataset stub, or an episode schema "while I'm here" is the exact scope creep the program spent four reviews disciplining out. Build M0, stop, bank it.
- **Using `latest` tags or unpinned tools.** Reproducibility begins at M0; an unpinned base image or tool version means a future fresh clone may not reproduce green.
- **Scattering `os.getenv` and magic numbers.** Configuration is one validated object; resist the temptation to read environment variables ad hoc.
- **`print` for diagnostics.** Establish the structured logger now; a `print` is a defect.
- **Silent exception swallowing.** A bare `except` that hides a container or config failure will cost hours later; fail loud now.
- **Committing `.env` or secrets.** Commit `.env.example` only; gitignore the rest from the first commit.
- **Skipping `mypy --strict` "for now."** Strict typing is cheap to start and expensive to retrofit; turn it on at commit one.
- **Leaving `main` red.** The fresh-clone-green heartbeat is the project's core invariant; never merge a red trunk.
- **Creating empty future folders.** Empty `agent/`, `episodes/`, `memory/` directories imply unbuilt structure and invite premature filling; create directories only when the milestone that needs them arrives.
- **Drifting into M1.** The instruction and this spec both stop at M0. Specifying or building the proposer/verify/log episode is M1's contract, written only after M0 is banked.

---

*End of M0 Engineering Specification. Implementation may begin against this contract; do not proceed to M1 specification or build until M0's Definition of Done is met and tagged.*