"""Runtime value types: state machine states, activations, handle, results (form only)."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

from noetica.interfaces.episode import Episode
from noetica.interfaces.provenance import Provenance
from noetica.interfaces.verification import Verdict

SCHEMA_VERSION = "0.1.0"


class EpisodeState(str, Enum):
    IDLE = "IDLE"
    SETUP = "SETUP"
    GUARD_CHECK = "GUARD_CHECK"
    ACTIVATE = "ACTIVATE"
    DISPATCH = "DISPATCH"
    YIELD = "YIELD"
    VERIFY = "VERIFY"
    PERSIST = "PERSIST"
    TEARDOWN = "TEARDOWN"
    DONE = "DONE"
    FAILED = "FAILED"
    HALTED = "HALTED"


class TerminalReason(str, Enum):
    PASSED = "PASSED"
    STEP_LIMIT = "STEP_LIMIT"
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"
    OVERSIGHT_DENIED = "OVERSIGHT_DENIED"
    STOPPED = "STOPPED"
    INFRA_ERROR = "INFRA_ERROR"


# ── Activations emitted by injected cognition; the Runtime dispatches on the type ──
@dataclass(frozen=True)
class ToolRequest:
    tool: str
    kwargs: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SkillRequest:
    skill: str
    kwargs: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Propose:
    candidate: str


@dataclass(frozen=True)
class Stop:
    reason: str = "done"


@dataclass(frozen=True)
class StepOutcome:
    index: int
    kind: str          # "dispatch" | "verify"
    detail: Any
    provenance: Provenance


@dataclass
class EpisodeHandle:
    episode_id: str
    goal: str
    state: EpisodeState
    step_index: int = 0
    outcomes: list[StepOutcome] = field(default_factory=list)
    final_verdict: Verdict | None = None
    terminal: TerminalReason | None = None


@dataclass(frozen=True)
class YieldSignal:
    reason: str
    episode_id: str
    state: EpisodeState


@dataclass(frozen=True)
class RunResult:
    episode_id: str
    goal: str
    success: bool
    terminal: TerminalReason
    steps: int
    episode: Episode | None
    schema_version: str = SCHEMA_VERSION
