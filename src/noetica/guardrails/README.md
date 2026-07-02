# src/noetica/guardrails — Safety Policy Engine

**Constitution:** §6.16 (guardrails / safety policy engine), Principle 6 / Law 17
(grounding & oversight are immutable).

## Purpose
The engine that enforces policy — including the immutable human-oversight boundary the
system may never modify. Noetica owns the *engine*; domains supply domain-policy *content*.

## Responsibilities
- Evaluate a proposed action against policies and return an allow/deny `Decision`.
  **Never executes the action.**
- Enforce an **immutable oversight boundary** (Law 17): oversight policies are fixed at
  construction; they cannot be modified or removed; an oversight denial is FINAL.
- Allow domains to *add* domain policies (`with_domain_policy`, returns a new engine),
  which can only make the engine stricter — never relax or remove oversight.

## Non-responsibilities (NOT here)
- **Executing actions** — the engine decides; the Runtime (PE-21) acts on the decision.
- **Reasoning, planning, runtime behavior** — separate subsystems.
- **Engineering-domain rules / Velith logic** — domain-policy *content* is domain-owned.
- The self-modification path itself (enforced by wiring at PE-21); this engine guarantees
  the oversight boundary object is immutable.

## Dependencies
- `noetica.interfaces.guardrail.Decision`; `noetica.guardrails.policy`.
- Python standard library only. No other platform mechanism, no other layer, no `reference/`.

## Consumers
- Runtime (PE-21) consults the engine at the action boundary; domains supply policy content.

## Constitution references
§6.16 · Principle 6 · Law 17.

## Future implementation milestones
- **Now (PE-9):** `GuardrailEngine` (immutable oversight + extendable domain policies),
  `Policy`/`FunctionPolicy`.
- **Later:** domain policy content (domain-owned); runtime enforcement wiring (PE-21).
