# src/noetica/sdk — Developer Surface (§6.18, PE-21)

The stable public SDK surface. `Agent(reasoning, verifier, **runtime_kwargs)` is a convenience
that wires an injected `ReasoningLoop` into a default activator and drives a `Runtime`.
Re-exports `Runtime` and the activation request types (`ToolRequest`/`SkillRequest`/`Propose`/
`Stop`). Owns no cognition; imports no cognitive mechanism (reasoning is an injected interface).
