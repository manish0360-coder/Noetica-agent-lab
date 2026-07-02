"""ToolRuntime — the default tool system: register, invoke, sandbox, async-dispatch (§6.12).

Purpose: the mechanism for registering, invoking, and SANDBOXING tools, with ASYNC,
    non-blocking invocation so the reasoning loop never blocks on a long-running solve.
    The tools themselves are wrapped external kernels owned by domains ("wrap, don't
    rebuild") — none are implemented here.
Owner: Noetica (Layer 2).
Consumer: Skill (PE-15), Reasoning (PE-18), Runtime (PE-21); domains implement concrete
    Tools (CAD, solvers, MES, robots) behind the `Tool` interface.
Constitution: §6.12; Principle 9 (wrap, don't rebuild); §6.14 (budget cost guard).
Future implementation owner: Noetica (runtime); domains (concrete tools).

Scope: registration/invocation/sandbox/async-dispatch + budget guard ONLY. No concrete
tools, no external kernels, no reasoning/planning/runtime-orchestration/domain logic.
Consumes the BudgetMeter INTERFACE (a concrete meter is injected).
"""
from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from collections.abc import Mapping
from types import TracebackType
from typing import Any

from noetica.interfaces.budget import BudgetMeter
from noetica.interfaces.tool import Tool, ToolResult


class ToolError(RuntimeError):
    """Base error for the tool runtime."""


class UnknownToolError(ToolError):
    """No tool is registered under the given name."""


class DuplicateToolError(ToolError):
    """A tool with the given name is already registered."""


class ToolBudgetError(ToolError):
    """The tool's cost cannot be afforded within the remaining budget (hard guard)."""


class UnknownHandleError(ToolError):
    """No async invocation exists for the handle."""


class ToolRuntime:
    """Registers tools, invokes them (sync or async), sandboxes faults, and meters cost.

    Sandbox: a tool that raises never crashes the runtime — the exception is isolated into
    a failed `ToolResult`. Async: `submit()` returns immediately with a handle; `poll()`
    is non-blocking; `result()` waits. Budget: each invocation charges the injected meter
    (hard guard) before the tool runs.
    """

    def __init__(self, budget: BudgetMeter, max_workers: int = 4) -> None:
        self._tools: dict[str, tuple[Tool, float]] = {}
        self._budget = budget
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._futures: dict[str, Future[ToolResult]] = {}
        self._counter = 0

    # ── registration ────────────────────────────────────────────────────────────
    def register(self, tool: Tool, cost: float = 0.0) -> None:
        if cost < 0:
            raise ValueError("tool cost must be non-negative")
        if tool.name in self._tools:
            raise DuplicateToolError(tool.name)
        self._tools[tool.name] = (tool, cost)

    def names(self) -> tuple[str, ...]:
        return tuple(self._tools.keys())

    # ── invocation ────────────────────────────────────────────────────────────
    def invoke(self, name: str, **kwargs: Any) -> ToolResult:
        """Synchronous, sandboxed, budget-charged invocation."""
        tool = self._charge(name)
        return self._sandbox(tool, kwargs)

    def submit(self, name: str, **kwargs: Any) -> str:
        """Non-blocking dispatch: charge budget, start the tool on a worker, return a handle
        immediately (the reasoning loop must never block on a long solve)."""
        tool = self._charge(name)
        handle = f"tool-{self._counter}"
        self._counter += 1
        self._futures[handle] = self._executor.submit(self._sandbox, tool, kwargs)
        return handle

    def poll(self, handle: str) -> ToolResult | None:
        """Return the result if the async invocation is done, else None (non-blocking)."""
        future = self._require(handle)
        return future.result() if future.done() else None

    def result(self, handle: str, timeout: float | None = None) -> ToolResult:
        """Wait (up to timeout) for the async invocation and return its result."""
        return self._require(handle).result(timeout)

    def cancel(self, handle: str) -> bool:
        """Attempt to cancel a not-yet-started async invocation."""
        return self._require(handle).cancel()

    # ── lifecycle ────────────────────────────────────────────────────────────────
    def shutdown(self) -> None:
        self._executor.shutdown(wait=True)

    def __enter__(self) -> "ToolRuntime":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.shutdown()

    # ── internal ────────────────────────────────────────────────────────────────
    def _charge(self, name: str) -> Tool:
        entry = self._tools.get(name)
        if entry is None:
            raise UnknownToolError(name)
        tool, cost = entry
        if cost > self._budget.remaining():
            raise ToolBudgetError(
                f"tool {name!r} cost {cost} exceeds remaining {self._budget.remaining()}"
            )
        self._budget.spend(cost, f"tool:{name}")
        return tool

    @staticmethod
    def _sandbox(tool: Tool, kwargs: Mapping[str, Any]) -> ToolResult:
        try:
            return tool.invoke(**kwargs)
        except Exception as e:  # intentional: isolate tool faults from the runtime
            return ToolResult(
                ok=False,
                output=None,
                detail={"error": repr(e), "error_type": type(e).__name__},
            )

    def _require(self, handle: str) -> Future[ToolResult]:
        future = self._futures.get(handle)
        if future is None:
            raise UnknownHandleError(handle)
        return future
