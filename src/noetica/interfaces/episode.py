"""Episode — a provenance-complete, content-hashed record of one grounded attempt.

Purpose: the first-class unit of learning data — task, proposal, verdict, cost,
    environment — that survives process exit; the reproducible *identity* lives in the
    content hash, non-reproducible signals in provenance.
Owner: Noetica (Layer 2) owns the Episode schema (a versioned data contract, Law 21)
    and the store engine.
Consumer: Velith (produces episodes); Mini Prometheus; MiniFlyWire (distilled datasets).
Constitution: §7.5; §1.10 (Episode); §11.7 (content-hash identity vs provenance);
    Law 21 (versioned schema).
Future implementation owner: Noetica (EpisodeStore default impl); domains populate it.

Interface surface only (PE-1). No hashing/serialization implemented here.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from collections.abc import Iterator
from typing import Any, Mapping, Protocol, runtime_checkable

from noetica.interfaces.provenance import Provenance
from noetica.interfaces.verification import Verdict


@dataclass(frozen=True)
class Episode:
    """Schema only. `content_hash` covers reproducible identity (task, patch, env);
    volatile signals live in `provenance`. No logic here (PE-1)."""

    task_id: str
    verdict: Verdict
    cost: Mapping[str, Any] = field(default_factory=dict)
    environment: Mapping[str, Any] = field(default_factory=dict)
    content_hash: str = ""
    provenance: Provenance | None = None
    schema_version: str = "0.1.0"


@runtime_checkable
class EpisodeStore(Protocol):
    """Append-only, provenance-complete store of episodes (engine owned by Noetica)."""

    def append(self, episode: Episode) -> str: ...          # returns stored id
    def get(self, episode_id: str) -> Episode | None: ...
    def __iter__(self) -> Iterator[Episode]: ...
