"""Provenance — the derivation record of every belief and artifact.

Purpose: carry *where a value came from and why* (which transform produced it, from
    which inputs) as a first-class, typed value attached to everything the platform
    stores or derives.
Owner: Noetica (Layer 2).
Consumer: Velith; Mini Prometheus (transitive); every Noetica subsystem.
Constitution: §6.2 (Provenance & Lineage); Principle 7; Law 18.
Future implementation owner: Noetica (default provenance store).

Interface surface only (PE-1): data models + Protocol. No implementation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, runtime_checkable


@dataclass(frozen=True)
class Provenance:
    """Typed derivation record. Schema only — construction/validation is deferred impl."""

    source: str                                   # origin id (agent, tool, import, human)
    transform: str                                # the transformation that produced the value
    inputs: tuple[str, ...] = ()                  # identifiers of inputs consumed
    attributes: Mapping[str, Any] = field(default_factory=dict)  # non-identity metadata
    schema_version: str = "0.1.0"                 # data-contract version (Law 21)


@runtime_checkable
class Provenanced(Protocol):
    """A value that can report its own provenance."""

    @property
    def provenance(self) -> Provenance: ...
