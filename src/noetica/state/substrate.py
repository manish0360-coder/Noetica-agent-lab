"""InMemoryStateSubstrate — the default StateSubstrate implementation (Constitution §6.1).

Purpose: the persistent, typed, provenance-tracked shared state that every other
    mechanism reads and writes — the platform's true core. This default is an in-memory,
    append-only, versioned store. Generators/planners/verifiers/learners are
    transformations over this state (they live elsewhere; none are implemented here).
Owner: Noetica (Layer 2).
Consumer: Velith; Mini Prometheus (through the StateSubstrate interface only).
Constitution: §6.1; §6.2 (provenance); Principle 2 / D9 (state-centric); Law 3.
Future implementation owner: Noetica (this default; later a belief/probabilistic
    substrate, §8.3 — gated, Appendix D).

Scope discipline: this file implements ONLY state. No memory (episodic), planner,
reasoning, runtime, reflection, or routing logic; no consumer/Velith/Mini Prometheus
logic (§6.20 keeps State distinct from Memory/Knowledge/Context).
"""
from __future__ import annotations

from types import MappingProxyType
from typing import Any

from noetica.interfaces.provenance import Provenance
from noetica.state.records import StateRecord, StateSnapshot


class InMemoryStateSubstrate:
    """Append-only, versioned, provenance-tracked in-memory state.

    Satisfies the `noetica.interfaces.state.StateSubstrate` Protocol structurally
    (get/put/history) and adds the record-level, versioning, and snapshot surface the
    default needs. Domain-agnostic.
    """

    def __init__(self) -> None:
        # key -> ordered history of immutable records (oldest first).
        self._history: dict[str, list[StateRecord]] = {}
        # global monotonic revision, incremented on every write.
        self._revision: int = 0

    # ── writes ────────────────────────────────────────────────────────────────
    def put(self, key: str, value: Any, provenance: Provenance) -> None:
        """Append a new immutable, provenance-tracked record for `key`."""
        self._revision += 1
        versions = self._history.setdefault(key, [])
        versions.append(
            StateRecord(
                key=key,
                value=value,
                provenance=provenance,
                version=len(versions) + 1,
                revision=self._revision,
            )
        )

    # ── reads ─────────────────────────────────────────────────────────────────
    def get(self, key: str) -> Any | None:
        """Return the latest value for `key`, or None if never written."""
        records = self._history.get(key)
        return records[-1].value if records else None

    def get_record(self, key: str) -> StateRecord | None:
        """Return the latest full record (value + provenance + versioning) for `key`."""
        records = self._history.get(key)
        return records[-1] if records else None

    def history(self, key: str) -> tuple[Any, ...]:
        """Return all values ever written to `key`, oldest first (immutable tuple)."""
        return tuple(r.value for r in self._history.get(key, ()))

    def record_history(self, key: str) -> tuple[StateRecord, ...]:
        """Return all records ever written to `key`, oldest first (immutable tuple)."""
        return tuple(self._history.get(key, ()))

    def keys(self) -> tuple[str, ...]:
        """Return all keys that have at least one record."""
        return tuple(self._history.keys())

    @property
    def revision(self) -> int:
        """The current global revision (number of writes applied)."""
        return self._revision

    # ── snapshots ───────────────────────────────────────────────────────────────
    def snapshot(self) -> StateSnapshot:
        """Return an immutable snapshot: latest record per key at the current revision."""
        latest: dict[str, StateRecord] = {
            key: records[-1] for key, records in self._history.items() if records
        }
        return StateSnapshot(revision=self._revision, records=MappingProxyType(latest))
