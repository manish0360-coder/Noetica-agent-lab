"""PE-10 unit tests — Model Router (§6.15).

Platform tests: deterministic routing + hard cost guard; providers behind the interface
(a test-double provider stands in for a vendor adapter). No vendor logic in the platform.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from noetica.budget import InMemoryBudgetMeter
from noetica.interfaces.router import ModelRequest, ModelResponse, ModelRouter
from noetica.router import (
    BudgetGuardError,
    DefaultModelRouter,
    ModelProvider,
    NoProviderError,
)


@dataclass
class _FakeProvider:
    """Test double for a wrapped provider (a real vendor adapter lives outside the platform)."""

    name: str
    capabilities: frozenset[str] = field(default_factory=frozenset)
    cost: float = 1.0
    seen: list[ModelRequest] = field(default_factory=list)

    def estimate_cost(self, request: ModelRequest) -> float:
        return self.cost

    def generate(self, request: ModelRequest) -> ModelResponse:
        self.seen.append(request)
        return ModelResponse(text=f"{self.name}:ok", input_tokens=1, output_tokens=1, stop_reason="stop")


def _req(model: str = "") -> ModelRequest:
    return ModelRequest(messages=({"role": "user", "content": "hi"},), model=model)


def test_router_satisfies_interface_and_provider_is_protocol() -> None:
    r = DefaultModelRouter([_FakeProvider("m")], InMemoryBudgetMeter(10.0))
    assert isinstance(r, ModelRouter)
    assert isinstance(_FakeProvider("m"), ModelProvider)


def test_routes_by_model_name() -> None:
    a, b = _FakeProvider("a"), _FakeProvider("b")
    r = DefaultModelRouter([a, b], InMemoryBudgetMeter(10.0))
    assert r.route(_req("b")).text == "b:ok"
    assert b.seen and not a.seen                      # only the selected provider generated


def test_deterministic_lowest_cost_tiebreak_name() -> None:
    cheap = _FakeProvider("z-cheap", cost=1.0)
    pricey = _FakeProvider("a-pricey", cost=5.0)
    r = DefaultModelRouter([pricey, cheap], InMemoryBudgetMeter(100.0))
    assert r.route(_req()).text == "z-cheap:ok"       # lowest cost wins, deterministically


def test_required_capabilities_filter() -> None:
    plain = _FakeProvider("plain")
    tools = _FakeProvider("tools", capabilities=frozenset({"tools"}))
    r = DefaultModelRouter([plain, tools], InMemoryBudgetMeter(10.0),
                           required_capabilities=frozenset({"tools"}))
    assert r.route(_req()).text == "tools:ok"


def test_no_provider_for_unknown_model() -> None:
    r = DefaultModelRouter([_FakeProvider("a")], InMemoryBudgetMeter(10.0))
    with pytest.raises(NoProviderError):
        r.route(_req("does-not-exist"))


def test_hard_cost_guard_blocks_and_does_not_generate() -> None:
    p = _FakeProvider("pricey", cost=50.0)
    meter = InMemoryBudgetMeter(10.0)
    r = DefaultModelRouter([p], meter)
    with pytest.raises(BudgetGuardError):
        r.route(_req())
    assert not p.seen                                 # never generated
    assert meter.spent == 0.0                         # nothing charged


def test_budget_charged_on_successful_route() -> None:
    meter = InMemoryBudgetMeter(10.0)
    r = DefaultModelRouter([_FakeProvider("a", cost=3.0)], meter)
    r.route(_req())
    assert meter.spent == 3.0 and meter.remaining() == 7.0


def test_router_does_not_mutate_request_or_touch_prompt() -> None:
    p = _FakeProvider("a")
    r = DefaultModelRouter([p], InMemoryBudgetMeter(10.0))
    req = _req()
    r.route(req)
    assert p.seen[0] is req                            # same request delegated, unmodified
