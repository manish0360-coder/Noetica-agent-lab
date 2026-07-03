# src/noetica/reflection — Reflection (§6.9)

Self-critique mechanism, form only (Law 3; a re-implementation seam for a validated
MiniFlyWire primitive, Law 7). `GroundedReflector.reflect(attempt, outcome)` inspects an
attempt against its **grounded** `Verdict` and proposes a `Revision` (revise flag + grounded
feedback). Deterministic; uses the verifier's verdict, never a model opinion (never
LLM-as-judge). A validated `CritiqueStrategy` may be injected. Optionally records critiques
to the State blackboard with provenance.

**Owns:** self-critique (form).
**Does NOT own:** planning, reasoning, runtime lifecycle, memory, state ownership, domain
logic; no autonomous agent, no conversation loop.

Deps (Roadmap v1.1): Reasoning, Episode, State — via interfaces. The revision feeds reasoning
at the consumer (PE-21), not by importing reasoning.
