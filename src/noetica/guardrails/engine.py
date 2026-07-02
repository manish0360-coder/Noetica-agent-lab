"""GuardrailEngine — the default safety policy engine (§6.16, Law 17).

Purpose: evaluate platform policies against a proposed action and return an allow/deny
    `Decision`. It NEVER executes the action. It enforces an IMMUTABLE oversight boundary:
    oversight policies are fixed at construction, cannot be modified or removed, and an
    oversight denial is final (domain policies can only add restrictions, never relax it).
Owner: Noetica (Layer 2) owns the ENGINE and the immutable oversight boundary; domains
    supply domain-policy content.
Consumer: Runtime (PE-21) wires and consults the engine at the action boundary.
Constitution: §6.16; Principle 6 / Law 17 (grounding & oversight are immutable — the
    system may improve how it designs, never how it is overseen).
Future implementation owner: Noetica (engine); domains (policy content).

Scope: policy evaluation ONLY. No reasoning, planning, runtime behavior, action
execution, engineering-domain rules, or Velith logic.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from noetica.guardrails.policy import Policy
from noetica.interfaces.guardrail import Decision


@dataclass(frozen=True)
class GuardrailEngine:
    """Immutable safety engine. `oversight` is the fixed, non-overridable boundary
    (Law 17); `domain` policies may only be *added* (via `with_domain_policy`), which can
    make the engine stricter but can never relax or remove oversight.
    """

    oversight: tuple[Policy, ...] = ()
    domain: tuple[Policy, ...] = field(default=())

    def check(self, action: object) -> Decision:
        """Evaluate policies and return a Decision. Never executes the action.

        Oversight policies are evaluated first; an oversight denial is FINAL and is not
        overridable by any domain policy (Law 17). If all pass, domain policies are
        evaluated (any denial denies). Allow only if every policy allows.
        """
        for policy in self.oversight:
            decision = policy.evaluate(action)
            if not decision.allowed:
                return Decision(allowed=False, reason=f"oversight:{policy.name}: {decision.reason}")
        for policy in self.domain:
            decision = policy.evaluate(action)
            if not decision.allowed:
                return Decision(allowed=False, reason=f"policy:{policy.name}: {decision.reason}")
        return Decision(allowed=True, reason="")

    def with_domain_policy(self, policy: Policy) -> "GuardrailEngine":
        """Return a NEW engine with an added domain policy; oversight is carried over
        intact and unchanged (immutability, Law 17)."""
        return GuardrailEngine(self.oversight, (*self.domain, policy))

    def oversight_policy_names(self) -> tuple[str, ...]:
        return tuple(p.name for p in self.oversight)

    def domain_policy_names(self) -> tuple[str, ...]:
        return tuple(p.name for p in self.domain)
