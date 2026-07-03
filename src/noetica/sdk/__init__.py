"""Noetica · sdk — Developer Surface (§6.18). The stable public entry surface.

Re-exports the Runtime + the `Agent` convenience + the activation request types. Owns no
cognition; the SDK wires injected mechanisms and drives the Runtime integrator.
"""
from __future__ import annotations

from noetica.runtime import (
    Propose,
    RunResult,
    Runtime,
    SkillRequest,
    Stop,
    ToolRequest,
    YieldSignal,
)
from noetica.sdk.agent import Agent, reasoning_activator

__all__ = [
    "Agent",
    "reasoning_activator",
    "Runtime",
    "ToolRequest",
    "SkillRequest",
    "Propose",
    "Stop",
    "RunResult",
    "YieldSignal",
]
