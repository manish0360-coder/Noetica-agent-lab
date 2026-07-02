# src/noetica/reasoning — Reasoning Runtime (§6.7)

Form of reasoning only (DN-7). Iterates inference via an injected `ModelRouter`, applies a
verification seam via an injected `Verifier`, and backtracks/retries within an injected
`BudgetMeter`, as a control plane over the shared `StateSubstrate` (blackboard). Reads an
injected `ContextAssembler`.

**Owns:** inference iteration, search/backtracking, retries, reasoning-loop control,
verification-seam invocation.
**Does NOT own:** planning, reflection, memory, knowledge, context ownership, tool
execution, state ownership, the verification protocol/oracle, the runtime lifecycle.
**Never:** conversation loop, autonomous agent, homunculus, semantic self-critique, domain
logic, prompt engineering.

Dependencies (Roadmap v1.1): State, Context, Router, Budget — all via interfaces, injected
(DN-7). No other platform mechanism imported.
