"""PE-18 unit tests — Reasoning Runtime (§6.7). Form only; injected capabilities."""
from __future__ import annotations

from typing import Any

from noetica.budget import InMemoryBudgetMeter
from noetica.interfaces.context import Context
from noetica.interfaces.reasoning import ReasoningLoop
from noetica.interfaces.router import ModelRequest, ModelResponse
from noetica.interfaces.verification import Verdict, VerdictStatus
from noetica.reasoning import ReasoningRuntime
from noetica.state import InMemoryStateSubstrate
from noetica.verification import ReferenceVerifier


class _SeqRouter:
    """Fake ModelRouter returning a scripted sequence of candidates."""

    def __init__(self, outputs: list[str]) -> None:
        self._outputs = outputs
        self.calls = 0

    def route(self, request: ModelRequest) -> ModelResponse:
        out = self._outputs[min(self.calls, len(self._outputs) - 1)]
        self.calls += 1
        return ModelResponse(text=out)


class _FakeContext:
    def __init__(self) -> None:
        self.calls = 0

    def assemble(self, goal: Any, token_budget: int) -> Context:
        self.calls += 1
        return Context(items=("ctx",), token_budget=token_budget)


def _verifier_on_candidate() -> ReferenceVerifier:
    return ReferenceVerifier(
        default=Verdict(status=VerdictStatus.FAILED),
        script={"good": Verdict(status=VerdictStatus.PASSED)},
        key_fn=lambda task, candidate: str(candidate),
    )


def test_satisfies_reasoning_loop_protocol() -> None:
    r = ReasoningRuntime(_SeqRouter(["good"]), ReferenceVerifier())
    assert isinstance(r, ReasoningLoop)


def test_single_step_success() -> None:
    r = ReasoningRuntime(_SeqRouter(["good"]), _verifier_on_candidate())
    result = r.run("g", max_steps=1)
    assert result.success and len(result.steps) == 1
    assert result.final is not None and result.final.verdict.status is VerdictStatus.PASSED


def test_backtrack_retry_until_pass() -> None:
    router = _SeqRouter(["bad0", "bad1", "good"])
    r = ReasoningRuntime(router, _verifier_on_candidate())
    result = r.run("g", max_steps=5)
    assert result.success and len(result.steps) == 3      # searched/backtracked to 'good'
    assert router.calls == 3


def test_exhaust_without_pass() -> None:
    r = ReasoningRuntime(_SeqRouter(["nope"]), _verifier_on_candidate())
    result = r.run("g", max_steps=3)
    assert result.success is False and len(result.steps) == 3


def test_budget_meta_control_stops() -> None:
    r = ReasoningRuntime(_SeqRouter(["good"]), _verifier_on_candidate(),
                         budget=InMemoryBudgetMeter(0.0))   # already exhausted
    result = r.run("g", max_steps=5)
    assert result.steps == () and result.success is False   # stopped before any inference


def test_state_blackboard_records_steps_with_provenance() -> None:
    state = InMemoryStateSubstrate()
    r = ReasoningRuntime(_SeqRouter(["good"]), _verifier_on_candidate(), state=state)
    r.run("g", max_steps=1)
    rec = state.get_record("reasoning:step:0")
    assert rec is not None and rec.provenance.source == "reasoning"


def test_context_is_consumed() -> None:
    ctx = _FakeContext()
    r = ReasoningRuntime(_SeqRouter(["bad", "bad"]), _verifier_on_candidate(), context=ctx)
    r.run("g", max_steps=2)
    assert ctx.calls == 2                                  # context assembled each step


def test_step_returns_verified_candidate() -> None:
    r = ReasoningRuntime(_SeqRouter(["good"]), _verifier_on_candidate())
    step = r.step("g")
    assert step.candidate == "good" and step.verdict.status is VerdictStatus.PASSED
