# src/noetica/planning — Planning Runtime (§6.8)

Plan representation + executor, form only (Law 3). `SequentialPlanner` builds a `Plan`
(default: single `reason` step; domains inject a step source). `SequentialExecutor`
sequences steps over the State blackboard: each action runs via an injected handler, the
`reason` action delegates to an injected `ReasoningLoop` (DN-7 injection), and a reflection
**seam** (post-step hook) is exposed for PE-20 — planning never imports/implements reflection.

**Owns:** plan representation + step sequencing (form).
**Does NOT own:** domain plans/actions, reasoning content, reflection, runtime lifecycle,
memory, state ownership.

Deps (Roadmap v1.1): Reasoning, State — via interfaces, injected. No other mechanism imported.
