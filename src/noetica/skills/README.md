# src/noetica/skills — Skill Runtime & Interface

**Constitution:** §6.13 (skill system + interface), Law 3 (form vs content), §6.12 (Tool
runtime), §6.1 (state substrate).

## Purpose
Composable, reusable units of competence. The runtime registers `Skill`s and applies them,
**composing** the platform's registered tools and the shared state substrate. A skill is a
*deterministic, reusable composition of capabilities*; the runtime is a deterministic
dispatcher.

## Responsibilities
- `register(skill)` / `names()` — manage registered skills (duplicate/unknown guarded).
- `apply(name, **kwargs)` — apply a skill over the platform **state**, exposing a restricted
  **tool invoker** as the reserved `tools` keyword (composition of tools + state).
- `ToolInvoker` — synchronous tool invocation only (no registration/async control).

## Non-responsibilities (NOT here)
- **Reasoning, planning, reflection, autonomous agents, workflows, conversation loops,
  learning policies, prompt engineering** — the runtime performs none of these.
- **Domain-specific skills** — concrete skills are domain-owned, external, behind the
  `Skill` interface.

## Dependencies
- `noetica.tools.ToolRuntime` (PE-12), `noetica.interfaces.state.StateSubstrate` (a concrete
  substrate — e.g. PE-2 — is injected), `noetica.interfaces.{skill,tool}`.
- Python standard library only. No other layer, no `reference/`.

## Consumers
- Reasoning (PE-18), Planning (PE-19), Runtime (PE-21); domains implement concrete skills.

## Constitution references
§6.13 · Law 3 · §6.12 · §6.1.

## Future implementation milestones
- **Now (PE-15):** `SkillRuntime` (register/apply + tool/state composition), `ToolInvoker`.
- **Later:** domain skills behind `Skill`; skills promoted from verified experience by
  extraction (Law 8), never as reasoning/planning here.
