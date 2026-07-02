"""Experiment arm configuration.

Purpose: bundle an experiment arm — a name, a solver (task -> candidate, external), and the
    mechanisms under measurement (its memory / state). The solver contains any reasoning;
    the harness only measures.
Owner: Noetica (Layer 2).
Consumer: EvaluationHarness; Velith configures arms (A0–A4).
Constitution: §6.10; D7 (arms).
Future implementation owner: Noetica (arm type); domains supply the solver + mechanisms.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from noetica.memory import InMemoryMemoryStore
from noetica.state import InMemoryStateSubstrate


@dataclass(frozen=True)
class Arm:
    """One experiment arm. `solver` (task_id -> candidate) is external (it holds any
    reasoning). `memory`/`state` are the mechanisms measured/guarded during frozen eval."""

    name: str
    solver: Callable[[str], Any]
    memory: InMemoryMemoryStore | None = None
    state: InMemoryStateSubstrate | None = None
