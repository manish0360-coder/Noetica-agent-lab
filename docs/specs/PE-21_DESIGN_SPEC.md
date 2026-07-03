# PE-21 — Runtime, Agent Lifecycle & SDK — Design Specification (FROZEN)

**Status:** Architecture only. No code. Frozen on ratification; changes require a superseding
decision (§11.7). Authority: Handbook v1.1, Roadmap v1.1, DN-1..DN-8, FIX-1.
**Constitution:** §6.3 (runtime & agent lifecycle), §6.18 (developer surface), §6.16 / Law 17
(guardrails / immutable oversight), §1.6 (condition-driven activation; five functions),
§1.9 / §6.7 (not a homunculus; form not mind), Principle 2 / D9 (state-centric), §7.5 (episode).

---

## 1. Purpose
Own **operation order** for a grounded agent run: set up an episode, drive the
**condition-driven activation** of injected cognitive mechanisms, enforce the immutable
oversight boundary, and tear down cleanly — while owning **none** of the thinking. It is the
integrator (Tier-7) and the stable developer surface (SDK) domains build on. It is a control
plane over shared state, never a central mind.

## 2. Responsibilities
- Episode setup/teardown (create/close an episode context on the substrate, provenance-complete).
- Drive **operation order** only: evaluate activation conditions and dispatch to injected
  mechanisms (reasoning, planning, reflection, memory, context, verification, router, tools,
  skills) — in a defined order, never implementing their logic.
- Enforce guardrails at defined checkpoints (oversight boundary is immutable, Law 17).
- Meter the run against the injected `BudgetMeter` and stop when exhausted.
- Persist the run as a provenance-complete `Episode`; hand retention to the memory
  write-filter (does not decide retention itself).
- Emit observability (logs/metrics/traces) across the lifecycle.
- Publish the versioned SDK surface (Agent/Runtime + plugin registration).
- Honor the **Yield Protocol** (§14): never run autonomously.

## 3. Non-responsibilities
Implements **no** cognition or content: no inference, no planning/sequencing logic, no
self-critique, no retrieval strategy, no memory retention policy, no model calls, no
verification oracle, no domain logic, no prompt construction, no conversation/dialogue state.
Does not decide *what* to think — only *when* activation proceeds.

## 4. Ownership boundaries
| Owns (form) | Does NOT own |
|---|---|
| Operation order / activation dispatch | Reasoning content (§6.7 — injected `ReasoningLoop`) |
| Episode setup/teardown (§7.5) | Planning content (§6.8 — injected `Planner`/`Executor`) |
| Guardrail checkpoints + oversight enforcement (Law 17) | Reflection content (§6.9 — injected `Reflector`) |
| Budget metering hooks (§6.14) | Memory retention (§6.4 — the write-filter decides) |
| Observability emission points (§6.17) | Verification oracle (§6.11, Law 15 — domain) |
| SDK surface + plugin registration (§6.18) | Model calls (§6.15 — injected `ModelRouter`) |
| Yield protocol | State substrate ownership (§6.1 — it transforms, not owns) |
| Tool/Skill **dispatch orchestration** (§6.12/§6.13) | Tool/Skill execution (injected `ToolRuntime`/`SkillRuntime`); cognition only *emits requests* |

## 5. Inputs
Goal/task; the injected mechanism set (DI graph, §11); a configured `BudgetMeter`; an
oversight `Guardrail` (+ domain policy content); registrations (tools/skills/verifier supplied
to their own runtimes); the shared `StateSubstrate`.

## 6. Outputs
A provenance-complete `Episode` (persisted via `EpisodeStore`; retention decided by the
memory write-filter); an agent run result value; observability signals; updated substrate
state (blackboard); **YieldSignals** to the caller/overseer.

## 7. Dependency graph
Integrator (Tier-7). Consumes PE-2..PE-20 **by injection through interfaces**; **nothing
imports PE-21** (import sink). Strict DAG top — matches Roadmap v1.1 and FIX-1 (INTRA_ALLOWED
integrator = may import any subsystem; no subsystem imports runtime/sdk → no cycle).

```
PE-2..PE-20  ──(interfaces, injected)──►  PE-21 (runtime + sdk)   [nothing imports PE-21]
```

## 8. Lifecycle
`start_episode(goal) → [guard → activate → yield]* → verify → persist → teardown → end`.
Setup writes an episode context to the substrate with provenance; teardown persists the
episode and releases resources. Each milestone in the loop is a bounded, caller-pumped step.

## 9. Runtime state machine
States: `IDLE, SETUP, GUARD_CHECK, ACTIVATE, DISPATCH, YIELD, VERIFY, PERSIST, TEARDOWN,
DONE, FAILED, HALTED`.
```
IDLE        --start_episode-->             SETUP
SETUP       --episode+provenance init-->   GUARD_CHECK
GUARD_CHECK --allow-->                      ACTIVATE     | --deny(oversight)--> HALTED
ACTIVATE    --dispatch injected cognition (reasoning/planning/reflection), condition-driven--> YIELD
ACTIVATE    --cognition emits ToolRequest/SkillRequest (data, not execution)--> DISPATCH
DISPATCH    --Runtime invokes injected ToolRuntime/SkillRuntime; writes result to substrate--> GUARD_CHECK
ACTIVATE(submit) --verify(injected)-->      VERIFY
VERIFY      --PASSED-->                      PERSIST     | --not passed--> YIELD (retry; bounded §9.1)
YIELD       --caller pump & budget ok & step-limit ok & oversight ok--> GUARD_CHECK
YIELD       --budget exhausted OR step-limit reached--> TEARDOWN(reason=budget|step_limit)
YIELD       --oversight halt-->             HALTED
PERSIST     --EpisodeStore + write-filter--> TEARDOWN
TEARDOWN    --observability + release-->     DONE        | --infra fault--> FAILED
```
Activation is **condition-driven** (external observation / internal inconsistency / active
goal) and only **selects order**; the activated mechanism is an injected interface.

### 9.1 Circuit breaker (bounded ACTIVATE cycles)
Every transition back to `ACTIVATE` — a retry after a non-passing `VERIFY`, or a
reflection-driven revision — is bounded by THREE independent limiters, any one of which
terminates or yields the run before infinite oscillation:
1. **BudgetMeter (§6.14):** `ACTIVATE` is entered only while the injected budget is not
   exhausted; on exhaustion the Runtime goes to `TEARDOWN(reason=budget)`, never `ACTIVATE`.
2. **Configured step limit (`max_steps`):** the retry/reflection loop halts at the limit ->
   `TEARDOWN(reason=step_limit)`.
3. **Yield Protocol (§14):** every cycle passes through `YIELD`, which is caller-pumped, so
   the Runtime never self-drives; the caller/overseer may halt at any yield.
If any limiter trips, the next state is `TEARDOWN` or `HALTED` — never `ACTIVATE`. Infinite
retry/reflection oscillation is therefore impossible by construction.

### 9.2 Tool/Skill orchestration (DN-7 preserved)
**Reasoning NEVER executes tools or skills.** A cognitive mechanism *emits* a
`ToolRequest`/`SkillRequest` value (a runtime-level request datum — not a change to any frozen
PE-1 interface, and not execution) and returns control to the Runtime (`ACTIVATE -> DISPATCH`).
The Runtime dispatches the request to the injected `ToolRuntime`/`SkillRuntime`, writes the
result to the **State Substrate** under the `episode_id`/`run_id` namespace with provenance,
then resumes the cognitive state machine (`DISPATCH -> GUARD_CHECK -> ACTIVATE`). Tool/skill
execution is thus Runtime-orchestrated; cognition only requests — DN-7 ownership is intact
(reasoning owns no tool execution).

## 10. SDK surface
Versioned public surface (§6.18), stable contract:
- `Agent.run(goal) -> RunResult` — convenience entry (bounded, yield-aware).
- `Runtime.start_episode(goal) -> EpisodeHandle`; `Runtime.step(handle) -> YieldSignal|StepResult`;
  `Runtime.submit(handle, candidate) -> Verdict`; `Runtime.end_episode(handle) -> Episode`.
- Plugin registration: `register_mechanism(kind, impl)` (interface-typed) / `register_plugin(...)`.
- All construction is via the DI graph (§11). No mechanism is constructed internally.

## 11. Dependency Injection graph
Runtime is constructed with interface-typed references only; it stores and dispatches, never
constructs cognition:
`StateSubstrate, Provenance(ledger), EpisodeStore, Observability, BudgetMeter, ModelRouter,
Guardrail, MemoryStore + WriteFilter, ContextAssembler, ReasoningLoop, Planner, Executor,
Reflector, Verifier, ToolRuntime, SkillRuntime`. Absent a mechanism, its activation branch is inert (fail-closed, §13).
DI is the structural guarantee of "integrator, not homunculus."

## 12. Blackboard interaction
All working/episode state lives on the `StateSubstrate` (blackboard, §6.1/D9). The runtime
reads/writes episode state with provenance under an `episode_id`/`run_id` namespace (per the
PE-18/PE-19 collision rule); injected mechanisms read/write the same substrate. Coordination
is **via shared state**, not via runtime-held state. The runtime holds no domain working state
in local variables beyond control bookkeeping (handles, indices).

## 13. Failure states
`INFRA_ERROR` (non-grounded; loud non-zero teardown), `BUDGET_EXCEEDED` (meta-control stop),
`OVERSIGHT_DENIED`/`HALTED` (guardrail deny is final, Law 17), verification non-pass (grounded
outcome; retry within budget), missing-mechanism (inert branch, no silent fallback). Grounded
outcomes vs errors follow the closed taxonomy (D16.7). The runtime never mutates its success
criterion or the oversight boundary (Law 17).

## 14. Yield protocol
The runtime is **non-autonomous by construction**: it contains no unbounded self-driving loop.
Every advance is caller-pumped (`step`/bounded `run(max_steps)`) or halts at a **yield point**
returning a `YieldSignal(reason, handle)`. Yield points: post-setup, before/after each
activation, oversight checkpoint, budget exhaustion, verification boundary, teardown. The
caller/overseer decides continuation; oversight may halt at any yield (Law 17). No dialogue
accumulation; yields are control signals, not conversation turns.

## 15. Constitution references
§6.3, §6.18, §6.16, Law 17 (oversight immutable), §1.6 (condition-driven activation; five
functions), §1.9 / §6.7 (not a homunculus; form not mind), Principle 2 / D9 (state-centric),
§6.14 (budget), §6.17 (observability), §7.5 / §1.10 (episode), §6.11 / Law 15 / Law 20
(verification protocol; oracle domain; self-tests use the reference verifier), §13.4 / §13.7.

## 16. Verification requirements
- `mypy --strict`; unit tests; boundary + intra-platform DAG (FIX-1) clean.
- **Law 20:** every runtime self-test uses only the `ReferenceVerifier`; end-to-end run over
  it yields a provenance-complete `Episode`.
- **Law 17:** a test proving no runtime path modifies the oversight boundary or verifier;
  guardrail deny is final and halts the run.
- **Anti-homunculus AST test:** the `runtime`/`sdk` packages define **no** cognition — no
  inference, planning, critique, retrieval, or model-call logic; only dispatch + DI wiring.
- **Yield-protocol test:** the runtime never advances without a caller pump; no `while True`
  autonomous loop; every run is bounded and yields.
- **Blackboard test:** episode state is written to the substrate (provenance + `episode_id`
  namespace), not held as domain state in the runtime.
- **Circuit-breaker test:** retry/reflection cycles terminate/yield within budget and the
  configured step limit; no run reaches `ACTIVATE` unbounded (no infinite oscillation).
- **Tool/Skill-orchestration test:** cognition emits a request; the Runtime dispatches to the
  injected ToolRuntime/SkillRuntime and writes the result to the substrate; reasoning executes
  no tool/skill (DN-7).
- Fresh-clone green with one command (§13.4).

## 17. Out-of-scope
Domain agents/content; any real domain verifier in the loop; model implementations; premature
scale/distribution infra; conversation/chat UX; autonomous long-running operation without
oversight; learned meta-control (gated PE-G5); plugin marketplace; experience aggregation
(gated PE-G3).

## 18. Impossibility proofs (required)
- **Homunculus — impossible:** the runtime implements no cognition; all cognition is injected
  interface references (§11 DI) and the anti-homunculus AST test (§16) fails the build if any
  cognitive logic appears. It owns order (form), never understanding (§6.7, §1.9).
- **Agent Brain — impossible:** no central decision of *what* to do — activation is
  condition-driven *order selection* (§1.6); the *what* is decided inside injected mechanisms.
  The runtime holds no domain working state (§12 blackboard).
- **Planner — impossible:** sequencing of domain steps is the injected `Planner`/`Executor`
  (§6.8); the runtime dispatches to it and never composes domain plans (verified by §16 AST +
  FIX-1: planning is a peer, not implemented here).
- **Reflection Engine — impossible:** self-critique is the injected `Reflector` (§6.9); the
  runtime performs none (AST test).
- **Conversation Loop — impossible:** the Yield Protocol (§14) forbids an autonomous loop;
  runs are episode-based, bounded, caller-pumped, with no dialogue-state accumulation; oversight
  can halt at any yield (Law 17).
