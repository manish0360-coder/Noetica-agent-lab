"""ModelRouter — model abstraction + routing + hard cost guard.

Purpose: make any frontier/open-weight/small model swappable behind one seam, so the
    system's identity depends on no single model or vendor; enforce a hard cost guard.
Owner: Noetica (Layer 2) (§6.15).
Consumer: Velith; Mini Prometheus.
Constitution: §6.15; Principle 3 (LLMs are components); D16.4 (extracted adapter seed).
Future implementation owner: Noetica (default router; seeded by re-implementing the
    MiniNoetica single-owner model-call pattern — never imported).

Interface surface only (PE-1). No provider client here.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, runtime_checkable


@dataclass(frozen=True)
class ModelRequest:
    """A vendor-neutral model request. Schema only."""

    messages: tuple[Mapping[str, Any], ...]
    model: str = ""
    max_tokens: int = 0


@dataclass(frozen=True)
class ModelResponse:
    """A vendor-neutral model response. Schema only."""

    text: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    stop_reason: str = ""


@runtime_checkable
class ModelRouter(Protocol):
    """Routes a request to a swappable provider under a hard cost guard."""

    def route(self, request: ModelRequest) -> ModelResponse: ...
