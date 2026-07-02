"""ModelProvider — the router's provider-adapter seam ("wrap, don't rebuild").

Purpose: the interface every model backend is wrapped behind, so the router selects among
    swappable providers by declared metadata/capabilities without any vendor-specific
    knowledge. Concrete providers (vendor adapters) are implemented elsewhere (domain /
    external), never in the platform.
Owner: Noetica (Layer 2) — the router's internal plug-in interface (§6.19).
Consumer: DefaultModelRouter; vendor adapters implement it.
Constitution: §6.15; Principle 3 (LLMs are swappable components); Principle 9 (wrap).
Future implementation owner: concrete providers = domain/external adapters (never here).
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from noetica.interfaces.router import ModelRequest, ModelResponse


@runtime_checkable
class ModelProvider(Protocol):
    """A wrapped, swappable model backend. Declares a name + capabilities, estimates cost,
    and generates a response. No vendor logic lives in the platform — only this seam."""

    name: str
    capabilities: frozenset[str]

    def estimate_cost(self, request: ModelRequest) -> float: ...

    def generate(self, request: ModelRequest) -> ModelResponse: ...
