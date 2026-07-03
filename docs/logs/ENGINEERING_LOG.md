# Engineering Log

Append-only per-milestone log (Engineering Execution Mode). One entry per milestone;
detailed history lives here so chat replies stay compact. Frozen context (Constitution,
Roadmap v1.1, DN-1..DN-8, FIX-1) is not restated.

Format: `PE-x <name> — commit <hash> — <status> — tests/mypy/boundary/arch`.

## Completed (backfill index)

| Milestone | Subsystem | Commit | Status |
|---|---|---|---|
| PE-1  | interfaces (contract surface, 21 pkgs) | `6260306` | done |
| PE-2  | state (StateSubstrate) §6.1 | `5866619` | done |
| PE-3  | provenance (Provenance & Lineage) §6.2 | `e971b80` | done |
| PE-4  | episodes (Episode & Episode Store) §7.5 | `5b4a283` | done |
| PE-5  | observability §6.17 | `bcab1d4` | done |
| PE-6  | budget (Budget & Meta-control) §6.14 | `16f4c88` | done |
| PE-7  | datacontracts §4.3/Law 21 | `483818b` | done |
| PE-8  | verification (ReferenceVerifier) §6.11/Law 20 | `ba77ddd` | done |
| PE-9  | guardrails §6.16/Law 17 | `d5ebe8d` | done |
| PE-10 | router (Model Router) §6.15 | `b834539` | done |
| PE-11 | compute (Compute Interface) §6.21 | `ebf3448` | done |
| PE-12 | tools (Tool Runtime) §6.12 | `a7bd66a` | done |
| PE-13 | knowledge (Knowledge Store) §6.5 | `a622c0e` | done |
| PE-14 | memory (Memory & Write-Filter) §6.4/D7 | `5bdb356` | done |
| PE-15 | skills (Skill Runtime) §6.13 | `c270a63` | done |
| PE-16 | context (Context Engine) §6.6 | `2370c92` | done |
| PE-17 | evaluation (Harness & Held-out Lock) §6.10 | `72db671` | done |
| FIX-1 | intra-platform DAG enforcement + DN-7/DN-8 | `0ba2521` | done |

Baseline at FIX-1: mypy --strict clean (79 files); 141 tests; 13 architecture tests;
boundary clean + fail-closed.

## Log (append below, newest last)

<!-- New milestone entries are appended here. -->

### PE-18 — reasoning (Reasoning Runtime, §6.7)
- files: src/noetica/reasoning/{models,runtime,__init__}.py, README.md; tests/noetica/test_reasoning.py
- impl: ReasoningRuntime (ReasoningLoop): infer→verify-seam→backtrack/retry; budget meta-control stop; state blackboard writes; context consumed. Form only.
- deps: interfaces only (State/Context/Router/Budget/Verifier all injected — DN-7); no mechanism import; FIX-1 DAG clean.
- boundaries: no planner/reflection/runtime-lifecycle/conversation/agent/homunculus/self-critique/domain.
- verify: mypy 81 ok; 149 tests (8 new); 13 arch; boundary+intra-DAG clean.

### PE-18.1 — reasoning review fixes (Board)
- files: src/noetica/reasoning/{models,runtime}.py; tests/noetica/test_reasoning.py
- fix1 non-sterile retries: prior candidate+raw verdict re-presented in next inference (deterministic, local; no self-critique/reflection).
- fix2 blackboard collisions: per-run run_id; state keys reasoning:{run_id}:step:{i}; ReasoningResult.run_id; concurrent/historical runs preserved.
- usability: default max_steps 1→3 (DEFAULT_MAX_STEPS); interface unchanged.
- not done (Law 8): Tool/Skill injection deferred — no real consumer yet.
- verify: mypy 81 ok; 151 tests (10 reasoning); 13 arch; boundary+intra-DAG clean.
