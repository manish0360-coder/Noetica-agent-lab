"""DefaultModelRouter — the default Model Router mechanism (§6.15).

Purpose: make any frontier/open-weight/small model swappable behind one seam, choosing a
    provider DETERMINISTICALLY from request metadata, declared provider capabilities,
    budget constraints, and a platform routing policy — with a HARD cost guard. It never
    inspects prompt content, reasons, plans, or executes domain logic.
Owner: Noetica (Layer 2).
Consumer: Reasoning (PE-18), Runtime (PE-21); Velith; Mini Prometheus.
Constitution: §6.15; Principle 3 (LLMs are components, not the mind); D16.4; §6.14 (cost
    guard via the BudgetMeter interface).
Future implementation owner: Noetica (this router). Concrete providers: domain/external.

Scope: routing decisions + cost guard + delegation ONLY. No vendor-specific logic, prompt
engineering, reasoning, planning, memory, runtime orchestration, or engineering-domain
functionality. Consumes the BudgetMeter INTERFACE (a concrete meter is injected).
"""
from __future__ import annotations

from collections.abc import Iterable

from noetica.interfaces.budget import BudgetMeter
from noetica.interfaces.router import ModelRequest, ModelResponse
from noetica.router.provider import ModelProvider


class RoutingError(RuntimeError):
    """Base error for routing failures."""


class NoProviderError(RoutingError):
    """No registered provider satisfies the request's model/capabilities."""


class BudgetGuardError(RoutingError):
    """No candidate provider is affordable within the remaining budget (hard guard)."""


class DefaultModelRouter:
    """Deterministic, budget-guarded router over swappable providers.

    Selection (deterministic): providers must declare all `required_capabilities`; if the
    request names a `model`, only that provider name matches; among affordable candidates
    the lowest estimated cost wins, ties broken by provider name. The chosen cost is then
    charged to the budget meter (hard guard). Delegates generation to the provider.
    """

    def __init__(
        self,
        providers: Iterable[ModelProvider],
        budget: BudgetMeter,
        required_capabilities: frozenset[str] = frozenset(),
    ) -> None:
        self._providers: tuple[ModelProvider, ...] = tuple(providers)
        self._budget = budget
        self._required = frozenset(required_capabilities)

    def route(self, request: ModelRequest) -> ModelResponse:
        candidates = self._select(request)
        if not candidates:
            raise NoProviderError(
                f"no provider for model={request.model!r} capabilities>={sorted(self._required)}"
            )
        remaining = self._budget.remaining()
        scored = [(p, p.estimate_cost(request)) for p in candidates]
        affordable = [(p, c) for (p, c) in scored if c <= remaining]
        if not affordable:
            raise BudgetGuardError(
                f"no affordable provider (remaining={remaining}) for model={request.model!r}"
            )
        provider, cost = min(affordable, key=lambda pc: (pc[1], pc[0].name))  # deterministic
        self._budget.spend(cost, f"route:{provider.name}")                     # hard cost guard
        return provider.generate(request)

    def _select(self, request: ModelRequest) -> list[ModelProvider]:
        candidates = [p for p in self._providers if self._required <= p.capabilities]
        if request.model:
            candidates = [p for p in candidates if p.name == request.model]
        return candidates

    def provider_names(self) -> tuple[str, ...]:
        return tuple(p.name for p in self._providers)
