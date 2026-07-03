"""Agent — SDK convenience entry (§6.18). Satisfies the `Agent` interface.

Wires an injected `ReasoningLoop` into a default activator (cognition -> Propose(candidate))
and drives a `Runtime`. Owns no cognition; imports no cognitive mechanism (reasoning is an
injected interface).
"""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from noetica.interfaces.reasoning import ReasoningLoop
from noetica.interfaces.verification import Verifier
from noetica.runtime import Activation, EpisodeHandle, Propose, RunResult, Runtime


def reasoning_activator(reasoning: ReasoningLoop) -> Callable[[EpisodeHandle], Activation]:
    """Adapt an injected ReasoningLoop into an activator that emits Propose(candidate)."""

    def activate(handle: EpisodeHandle) -> Activation:
        result = reasoning.run(handle.goal)
        final = getattr(result, "final", None)
        candidate = getattr(final, "candidate", "") if final is not None else ""
        return Propose(candidate=str(candidate))

    return activate


class Agent:
    """Convenience agent: injected reasoning + verifier (+ runtime kwargs) -> a driven run."""

    def __init__(self, reasoning: ReasoningLoop, verifier: Verifier, **runtime_kwargs: Any) -> None:
        self._reasoning = reasoning
        self._verifier = verifier
        self._runtime_kwargs = runtime_kwargs

    def run(self, goal: Any, max_steps: int | None = None) -> RunResult:
        runtime = Runtime(
            activator=reasoning_activator(self._reasoning),
            verifier=self._verifier,
            **self._runtime_kwargs,
        )
        return runtime.run(goal, max_steps)
