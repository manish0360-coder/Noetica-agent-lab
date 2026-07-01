"""Agent / Runtime — the agent lifecycle + developer surface.

Purpose: run an agent — set up an episode, drive condition-driven activation of
    functions, tear down cleanly — owning operation order WITHOUT deciding what to think
    (no homunculus). The public entry point domains build on.
Owner: Noetica (Layer 2) (§6.3, §6.18).
Consumer: Velith; Mini Prometheus (build agents via this SDK surface).
Constitution: §6.3 (runtime & lifecycle); §6.18 (developer surface); Law 3.
Future implementation owner: Noetica (default runtime + SDK).

Interface surface only (PE-1). No orchestration logic here.
"""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from noetica.interfaces.verification import Verdict


@runtime_checkable
class Agent(Protocol):
    """A grounded agent run entry point. Form only."""

    def run(self, goal: Any) -> Any: ...


@runtime_checkable
class Runtime(Protocol):
    """Owns episode setup -> activation -> teardown (operation order), not the thinking."""

    def start_episode(self, goal: Any) -> str: ...          # returns episode id
    def submit(self, candidate: Any) -> Verdict: ...        # via the verification protocol
    def end_episode(self, episode_id: str) -> None: ...
