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
    """Fake ModelRouter: scripted candidates; records the requests it receives."""

    def __init__(self, outputs: list[str]) -> None:
        self._outputs = outputs
        self.calls = 0
        self.seen: list[ModelRequest] = []

    def route(self, request: ModelRequest) -> ModelResponse:
        self.seen.append(request)
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
    assert isinstance(ReasoningRuntime(_SeqRouter(["good"]), ReferenceVerifier()), ReasoningLoop)


def test_single_step_success() -> None:
    result = ReasoningRuntime(_SeqRouter(["good"]), _verifier_on_candidate()).run("g", max_steps=1)
    assert result.success and len(result.steps) == 1
    assert result.final is not None and result.final.verdict.status is VerdictStatus.PASSED


def test_backtrack_retry_until_pass() -> None:
    router = _SeqRouter(["bad0", "bad1", "good"])
    result = ReasoningRuntime(router, _verifier_on_candidate()).run("g", max_steps=5)
    assert result.success and len(result.steps) == 3 and router.calls == 3


def test_exhaust_without_pass() -> None:
    result = ReasoningRuntime(_SeqRouter(["nope"]), _verifier_on_candidate()).run("g", max_steps=3)
    assert result.success is False and len(result.steps) == 3


def test_retry_feeds_back_prior_candidate_and_verdict() -> None:
    router = _SeqRouter(["bad0", "good"])
    ReasoningRuntime(router, _verifier_on_candidate()).run("g", max_steps=2)
    # the 2nd request must carry the 1st failed candidate + its verdict (non-sterile, local)
    second = router.seen[1]
    feedback = " ".join(str(m["content"]) for m in second.messages)
    assert "bad0" in feedback and "FAILED" in feedback


def test_budget_meta_control_stops() -> None:
    result = ReasoningRuntime(_SeqRouter(["good"]), _verifier_on_candidate(),
                              budget=InMemoryBudgetMeter(0.0)).run("g", max_steps=5)
    assert result.steps == () and result.success is False


def test_run_ids_are_unique_and_state_keys_do_not_collide() -> None:
    state = InMemoryStateSubstrate()
    r = ReasoningRuntime(_SeqRouter(["good"]), _verifier_on_candidate(), state=state)
    a = r.run("g", max_steps=1)
    b = r.run("g", max_steps=1)
    assert a.run_id != b.run_id
    assert state.get_record(f"reasoning:{a.run_id}:step:0") is not None
    assert state.get_record(f"reasoning:{b.run_id}:step:0") is not None   # both preserved


def test_explicit_run_id_and_provenance() -> None:
    state = InMemoryStateSubstrate()
    r = ReasoningRuntime(_SeqRouter(["good"]), _verifier_on_candidate(), state=state)
    result = r.run("g", max_steps=1, run_id="RUN42")
    assert result.run_id == "RUN42"
    rec = state.get_record("reasoning:RUN42:step:0")
    assert rec is not None and rec.provenance.source == "reasoning"


def test_context_is_consumed() -> None:
    ctx = _FakeContext()
    ReasoningRuntime(_SeqRouter(["bad", "bad"]), _verifier_on_candidate(), context=ctx).run("g", max_steps=2)
    assert ctx.calls == 2


def test_step_returns_verified_candidate() -> None:
    step = ReasoningRuntime(_SeqRouter(["good"]), _verifier_on_candidate()).step("g")
    assert step.candidate == "good" and step.verdict.status is VerdictStatus.PASSED
