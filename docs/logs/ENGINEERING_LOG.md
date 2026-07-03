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

### PE-19 — planning (Planning Runtime, §6.8)
- files: src/noetica/planning/{models,planner,executor,__init__}.py, README.md; tests/noetica/test_planning.py
- impl: SequentialPlanner (Plan repr; default single `reason` step, injectable step_source); SequentialExecutor (sequences steps over State blackboard; `reason` delegates to injected ReasoningLoop; reflection SEAM hook for PE-20; per-run run_id keys). Form only.
- deps: interfaces only (Reasoning/State injected — DN-7); FIX-1 DAG clean.
- boundaries: no domain plans/actions, no reflection impl, no runtime lifecycle.
- verify: mypy 84 ok; 160 tests (9 new); 13 arch; boundary+intra-DAG clean.

### PE-20 — reflection (Reflection, §6.9)
- files: src/noetica/reflection/{models,reflector,__init__}.py, README.md; tests/noetica/test_reflection.py
- impl: GroundedReflector.reflect(attempt,outcome)->Revision; grounded (verdict-based) critique, deterministic, never LLM-as-judge; injectable CritiqueStrategy (Law 7 promotion seam); optional State blackboard write w/ provenance + run_id.
- deps: interfaces only (Verdict/Episode/State); revision feeds reasoning at consumer, not imported; FIX-1 DAG clean.
- boundaries: self-critique only; no planning/reasoning ownership, no runtime/agent/loop/domain.
- verify: mypy 86 ok; 168 tests (8 new); 13 arch; boundary+intra-DAG clean.

### PE-21 (spec) — Runtime/SDK Design Specification (frozen; no code)
- files: docs/specs/PE-21_DESIGN_SPEC.md
- content: 18 sections (purpose..out-of-scope + impossibility proofs). Integrator/DI, condition-driven activation, blackboard, yield protocol, failure states, SDK surface.
- proofs: cannot become homunculus/agent-brain/planner/reflection-engine/conversation-loop (DI + anti-cognition AST test + yield protocol + FIX-1).
- conformance: handbook refs verified (6.3/6.7/6.16/6.18/Law17/1.6/6.11/7.5/Law20 exist). No conflict.
- no implementation.

### PE-21 (spec) — Board fixes to Design Specification
- files: docs/specs/PE-21_DESIGN_SPEC.md
- fix1: §9 state machine adds DISPATCH state + §9.2 tool/skill orchestration — reasoning emits ToolRequest/SkillRequest (data), Runtime dispatches to injected Tool/SkillRuntime, writes result to substrate, resumes. DN-7 preserved. DI graph (§11) lists Tool/SkillRuntime.
- fix2: §9.1 circuit breaker — every ACTIVATE re-entry bounded by BudgetMeter + step limit + Yield Protocol; no infinite oscillation. §16 adds circuit-breaker + tool/skill-orchestration tests.
- unchanged: architecture, interfaces, mechanisms, DN-7, DN-8. No code.
