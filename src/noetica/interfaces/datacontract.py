"""DataContract — the versioned-schema base for the Experience Flow.

Purpose: declare the versioning contract every upward experience schema (episode,
    dataset, derived-question) must satisfy, held to the same rigor as downward
    interfaces.
Owner: Noetica (Layer 2) — the contract *authority*.
Consumer: Velith; Mini Prometheus (emit/consume against a declared version).
Constitution: §4.3 (Experience Flow); Law 21 (Data Contract Law); §11.7; §11.11.
Future implementation owner: Noetica (versioning + migration framework).

Interface surface only (PE-1). No implementation.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class DataContract(Protocol):
    """Any experience payload governed by a versioned schema (Law 21).

    A concrete payload declares SCHEMA_VERSION; a change requires a new version and a
    migration path (enforced later by the data-contract check, §11.10).
    """

    SCHEMA_VERSION: str
