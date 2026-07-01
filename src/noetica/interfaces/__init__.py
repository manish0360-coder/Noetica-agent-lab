"""Noetica · interfaces — the typed public contract surface (Constitution Part VI / §6.18).

Purpose: the single, versioned surface domains consume — Protocols, ABCs, data models,
    and enums. Interfaces are designed early; depth (implementations) is added on a
    schedule by extraction (Principle 4; Law 8; §13.6).
Owner: Noetica (Layer 2). Consumer: Velith; Mini Prometheus.
Future implementation owner: Noetica default impls, except domain-supplied concretes
    (Verifier oracle, Tool, Skill, compute adapters).

PE-1 defines contracts ONLY — no implementations, no algorithms.
"""
from __future__ import annotations

from noetica.interfaces.budget import BudgetMeter
from noetica.interfaces.compute import ComputeInterface
from noetica.interfaces.context import Context, ContextAssembler
from noetica.interfaces.datacontract import DataContract
from noetica.interfaces.episode import Episode, EpisodeStore
from noetica.interfaces.evaluation import EvalHarness, EvalResult
from noetica.interfaces.guardrail import Decision, Guardrail
from noetica.interfaces.knowledge import KnowledgeStore
from noetica.interfaces.memory import MemoryStore, WriteFilter
from noetica.interfaces.plan import Executor, Plan, Planner, Step
from noetica.interfaces.provenance import Provenance, Provenanced
from noetica.interfaces.reasoning import ReasoningLoop
from noetica.interfaces.reflection import Reflector
from noetica.interfaces.router import ModelRequest, ModelResponse, ModelRouter
from noetica.interfaces.runtime import Agent, Runtime
from noetica.interfaces.skill import Skill
from noetica.interfaces.state import StateSubstrate
from noetica.interfaces.tool import Tool, ToolResult
from noetica.interfaces.verification import Verdict, VerdictStatus, Verifier
from noetica.interfaces.worldmodel import WorldModel

__all__ = [
    "Agent", "Runtime",
    "StateSubstrate", "Provenance", "Provenanced",
    "Episode", "EpisodeStore", "DataContract",
    "MemoryStore", "WriteFilter", "KnowledgeStore",
    "Context", "ContextAssembler",
    "ReasoningLoop", "Plan", "Step", "Planner", "Executor", "Reflector",
    "Tool", "ToolResult", "Skill",
    "ModelRouter", "ModelRequest", "ModelResponse",
    "BudgetMeter", "ComputeInterface",
    "EvalHarness", "EvalResult",
    "Guardrail", "Decision",
    "Observability",
    "Verifier", "Verdict", "VerdictStatus",
    "WorldModel",
]

from noetica.interfaces.observability import Observability  # noqa: E402 (kept with group)
