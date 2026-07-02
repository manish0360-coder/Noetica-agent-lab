"""PE-15 unit tests — Skill Runtime (§6.13).

Platform tests: register + apply, composing tools + platform state. Concrete skills/tools
are test doubles (real ones are domain-owned behind the interfaces).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from noetica.budget import InMemoryBudgetMeter
from noetica.interfaces.provenance import Provenance
from noetica.interfaces.skill import Skill
from noetica.interfaces.state import StateSubstrate
from noetica.interfaces.tool import ToolResult
from noetica.skills import DuplicateSkillError, SkillRuntime, ToolInvoker, UnknownSkillError
from noetica.state import InMemoryStateSubstrate
from noetica.tools import ToolRuntime


@dataclass
class _EchoTool:
    name: str = "echo"

    def invoke(self, **kwargs: Any) -> ToolResult:
        return ToolResult(ok=True, output=kwargs.get("value"))


@dataclass
class _GreetSkill:
    """Deterministic composition: read a name from state, format it via a tool."""

    name: str = "greet"

    def apply(self, state: StateSubstrate, tools: ToolInvoker, **kwargs: Any) -> Any:
        who = state.get(kwargs["name_key"])
        result = tools.invoke("echo", value=f"hello {who}")
        return result.output


def _runtime() -> tuple[SkillRuntime, InMemoryStateSubstrate, ToolRuntime]:
    state = InMemoryStateSubstrate()
    tools = ToolRuntime(InMemoryBudgetMeter(100.0))
    tools.register(_EchoTool())
    return SkillRuntime(state, tools), state, tools


def test_skill_satisfies_protocol() -> None:
    assert isinstance(_GreetSkill(), Skill)


def test_register_and_apply_composes_state_and_tool() -> None:
    rt, state, _ = _runtime()
    rt.register(_GreetSkill())
    state.put("user", "alice", Provenance(source="test", transform="seed"))
    assert rt.apply("greet", name_key="user") == "hello alice"
    assert rt.names() == ("greet",)


def test_duplicate_and_unknown() -> None:
    rt, _, _ = _runtime()
    rt.register(_GreetSkill())
    with pytest.raises(DuplicateSkillError):
        rt.register(_GreetSkill())
    with pytest.raises(UnknownSkillError):
        rt.apply("missing")


def test_tools_kwarg_is_reserved() -> None:
    rt, _, _ = _runtime()
    rt.register(_GreetSkill())
    with pytest.raises(ValueError):
        rt.apply("greet", name_key="user", tools="hijack")


def test_apply_is_deterministic() -> None:
    rt, state, _ = _runtime()
    rt.register(_GreetSkill())
    state.put("user", "bob", Provenance(source="test", transform="seed"))
    a = rt.apply("greet", name_key="user")
    b = rt.apply("greet", name_key="user")
    assert a == b == "hello bob"


def test_skill_can_write_platform_state() -> None:
    @dataclass
    class _StampSkill:
        name: str = "stamp"

        def apply(self, state: StateSubstrate, tools: ToolInvoker, **kwargs: Any) -> Any:
            state.put("stamped", True, kwargs["provenance"])
            return state.get("stamped")

    rt, state, _ = _runtime()
    rt.register(_StampSkill())
    out = rt.apply("stamp", provenance=Provenance(source="test", transform="stamp"))
    assert out is True and state.get("stamped") is True
