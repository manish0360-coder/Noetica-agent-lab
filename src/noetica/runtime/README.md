# src/noetica/runtime — Runtime & Agent Lifecycle (§6.3, PE-21)

The integrator. Owns operation order (episode setup/teardown, condition-driven activation
dispatch, guardrail checkpoints, budget metering, tool/skill dispatch orchestration,
observability, yield protocol, circuit breaker). Owns **no** cognition — reasoning, planning,
reflection, verification oracle, model calls, memory retention are all injected via
interfaces. Implements the frozen PE-21 Design Specification (`docs/specs/PE-21_DESIGN_SPEC.md`).

**Reasoning never executes tools:** cognition emits `ToolRequest`/`SkillRequest`; the Runtime
dispatches to the injected `ToolRuntime`/`SkillRuntime`, writes the result to the State
blackboard, and resumes (DN-7). **Circuit breaker:** every ACTIVATE re-entry is bounded by
`max_steps` + `BudgetMeter` + the caller pump — no infinite oscillation. Satisfies the
`Runtime` interface (start_episode/submit/end_episode) plus step/run drivers.
