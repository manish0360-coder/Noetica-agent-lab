"""PE-21 unit tests — SDK Agent (§6.18)."""
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from noetica.interfaces.runtime import Agent as AgentProto
from noetica.interfaces.verification import Verdict, VerdictStatus
from noetica.sdk import Agent
from noetica.verification import ReferenceVerifier


class _FakeReasoning:
    def step(self, state: Any) -> Any:
        return None

    def run(self, goal: Any, max_steps: int = 1) -> Any:
        return SimpleNamespace(final=SimpleNamespace(candidate="good"))


def _verifier() -> ReferenceVerifier:
    return ReferenceVerifier(default=Verdict(status=VerdictStatus.FAILED),
                             script={"good": Verdict(status=VerdictStatus.PASSED)},
                             key_fn=lambda task, candidate: str(candidate))


def test_agent_satisfies_protocol_and_runs() -> None:
    agent = Agent(_FakeReasoning(), _verifier())
    assert isinstance(agent, AgentProto)
    result = agent.run("g")
    assert result.success is True
