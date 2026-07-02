"""Noetica · skills — Skill Runtime & Interface (§6.13).

Composable, reusable units of competence: the runtime registers `Skill`s and applies them,
composing the platform's tools (PE-12) and shared state (PE-2). PE-15 provides
`SkillRuntime` and the `ToolInvoker` handle. Deterministic dispatch — no reasoning,
planning, reflection, agents, workflows, loops, learning policies, or domain skills;
concrete skills are domain-owned behind the `Skill` interface.
"""
from __future__ import annotations

from noetica.skills.runtime import (
    DuplicateSkillError,
    SkillError,
    SkillRuntime,
    ToolInvoker,
    UnknownSkillError,
)

__all__ = [
    "SkillRuntime",
    "ToolInvoker",
    "SkillError",
    "UnknownSkillError",
    "DuplicateSkillError",
]
