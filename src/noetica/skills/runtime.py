"""SkillRuntime — the default skill system: register + apply reusable compositions (§6.13).

Purpose: register `Skill`s and apply them, composing the platform's registered tools and
    the shared state substrate for the skill. A skill is a deterministic, reusable
    composition of capabilities (tools + state); the runtime is a deterministic dispatcher
    — it performs no reasoning, planning, or orchestration.
Owner: Noetica (Layer 2).
Consumer: Reasoning (PE-18), Planning (PE-19), Runtime (PE-21); domains implement concrete
    Skills behind the `Skill` interface.
Constitution: §6.13; Law 3 (form vs content); §6.12 (composes the Tool runtime); §6.1 (state).
Future implementation owner: Noetica (runtime); domains (concrete skills).

Scope: registration + application + tool/state composition ONLY. NO reasoning, planning,
reflection, autonomous agents, workflows, conversation loops, learning policies, prompt
engineering, or domain-specific skills. Consumes the Tool runtime (PE-12) and the
StateSubstrate interface (a concrete substrate is injected).
"""
from __future__ import annotations

from typing import Any

from noetica.interfaces.skill import Skill
from noetica.interfaces.state import StateSubstrate
from noetica.interfaces.tool import ToolResult
from noetica.tools import ToolRuntime


class SkillError(RuntimeError):
    """Base error for the skill runtime."""


class UnknownSkillError(SkillError):
    """No skill is registered under the given name."""


class DuplicateSkillError(SkillError):
    """A skill with the given name is already registered."""


class ToolInvoker:
    """A restricted capability handle passed to skills: synchronous tool invocation only
    (no registration or async control). Skills compose tools through this."""

    def __init__(self, tools: ToolRuntime) -> None:
        self._tools = tools

    def invoke(self, name: str, **kwargs: Any) -> ToolResult:
        return self._tools.invoke(name, **kwargs)


class SkillRuntime:
    """Registers skills and applies them, composing tools + platform state. Deterministic
    dispatch: the runtime adds no reasoning/planning; it wires state + a tool invoker to
    the skill and calls `apply`."""

    def __init__(self, state: StateSubstrate, tools: ToolRuntime) -> None:
        self._skills: dict[str, Skill] = {}
        self._state = state
        self._invoker = ToolInvoker(tools)

    def register(self, skill: Skill) -> None:
        if skill.name in self._skills:
            raise DuplicateSkillError(skill.name)
        self._skills[skill.name] = skill

    def names(self) -> tuple[str, ...]:
        return tuple(self._skills.keys())

    def apply(self, name: str, **kwargs: Any) -> Any:
        """Apply a registered skill over the platform state, exposing the tool invoker as
        the reserved `tools` keyword. Returns whatever the skill returns."""
        if "tools" in kwargs:
            raise ValueError("'tools' is reserved and injected by the runtime")
        skill = self._require(name)
        return skill.apply(self._state, tools=self._invoker, **kwargs)

    def _require(self, name: str) -> Skill:
        skill = self._skills.get(name)
        if skill is None:
            raise UnknownSkillError(name)
        return skill
