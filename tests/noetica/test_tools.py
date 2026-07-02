"""PE-12 unit tests — Tool Runtime (§6.12).

Platform tests: register/invoke/sandbox + async non-blocking + budget guard. Concrete
tools are test doubles (real tools are domain-owned behind the Tool interface).
"""
from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Any

import pytest

from noetica.budget import InMemoryBudgetMeter
from noetica.interfaces.tool import Tool, ToolResult
from noetica.tools import (
    DuplicateToolError,
    ToolBudgetError,
    ToolRuntime,
    UnknownToolError,
)


@dataclass
class _EchoTool:
    name: str = "echo"

    def invoke(self, **kwargs: Any) -> ToolResult:
        return ToolResult(ok=True, output=kwargs)


@dataclass
class _RaisingTool:
    name: str = "boom"

    def invoke(self, **kwargs: Any) -> ToolResult:
        raise RuntimeError("kernel exploded")


class _BlockingTool:
    """Blocks until an event is set — models a long-running solve."""

    name = "slow"

    def __init__(self) -> None:
        self.release = threading.Event()

    def invoke(self, **kwargs: Any) -> ToolResult:
        self.release.wait(timeout=5)
        return ToolResult(ok=True, output="done")


def test_echo_tool_satisfies_tool_protocol() -> None:
    assert isinstance(_EchoTool(), Tool)


def test_register_and_invoke() -> None:
    with ToolRuntime(InMemoryBudgetMeter(10.0)) as rt:
        rt.register(_EchoTool())
        out = rt.invoke("echo", x=1, y=2)
        assert out.ok and out.output == {"x": 1, "y": 2}
        assert rt.names() == ("echo",)


def test_duplicate_and_unknown() -> None:
    with ToolRuntime(InMemoryBudgetMeter(10.0)) as rt:
        rt.register(_EchoTool())
        with pytest.raises(DuplicateToolError):
            rt.register(_EchoTool())
        with pytest.raises(UnknownToolError):
            rt.invoke("missing")


def test_sandbox_isolates_tool_faults() -> None:
    with ToolRuntime(InMemoryBudgetMeter(10.0)) as rt:
        rt.register(_RaisingTool())
        out = rt.invoke("boom")                       # does NOT raise
        assert out.ok is False
        assert out.detail["error_type"] == "RuntimeError"
        assert "kernel exploded" in out.detail["error"]


def test_budget_charged_on_invoke() -> None:
    meter = InMemoryBudgetMeter(10.0)
    with ToolRuntime(meter) as rt:
        rt.register(_EchoTool(), cost=3.0)
        rt.invoke("echo")
        assert meter.spent == 3.0


def test_budget_hard_guard_blocks_and_does_not_run() -> None:
    meter = InMemoryBudgetMeter(2.0)
    ran = {"v": False}

    @dataclass
    class _Marker:
        name: str = "mark"
        def invoke(self, **kwargs: Any) -> ToolResult:
            ran["v"] = True
            return ToolResult(ok=True)

    with ToolRuntime(meter) as rt:
        rt.register(_Marker(), cost=5.0)
        with pytest.raises(ToolBudgetError):
            rt.invoke("mark")
        assert ran["v"] is False and meter.spent == 0.0


def test_async_submit_is_non_blocking_then_completes() -> None:
    tool = _BlockingTool()
    with ToolRuntime(InMemoryBudgetMeter(10.0)) as rt:
        rt.register(tool)
        handle = rt.submit("slow")                    # returns immediately
        assert rt.poll(handle) is None                # still running -> non-blocking
        tool.release.set()                            # let it finish
        result = rt.result(handle, timeout=5)
        assert result.ok and result.output == "done"
        assert rt.poll(handle) is not None            # now done
