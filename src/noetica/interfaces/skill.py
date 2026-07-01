"""Skill — composable, learned units of competence.

Purpose: how verified experience crystallizes into reusable competence — a mechanism of
    composition. Form owned by Noetica; concrete skills are domain content.
Owner: Noetica (Layer 2) owns the interface + runtime (§6.13).
Consumer: Velith (engineering skills); Mini Prometheus (mfg skills).
Constitution: §6.13; Law 3 (form vs content).
Future implementation owner: DOMAIN (concrete skills); Noetica ships the runtime.

Interface surface only (PE-1). No skill implementation here.
"""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Skill(Protocol):
    """A composable unit of competence. Domains implement concrete skills."""

    name: str

    def apply(self, state: Any, **kwargs: Any) -> Any: ...
