"""DataContractRegistry — the default Data Contract & Versioning mechanism (Law 21).

Purpose: govern the Experience Flow's schemas. Every episode/dataset/derived-question
    payload carries a `schema_version`; a schema change requires a new version AND a
    registered forward migration path. Consumers read against a declared version. This is
    the framework the §11.10 data-contract check enforces.
Owner: Noetica (Layer 2) — the contract authority.
Consumer: Episode/Memory schema evolution; the Experience Flow; Velith; Mini Prometheus.
Constitution: §4.3; Law 21; §11.7; §11.10; §11.11.
Future implementation owner: Noetica.

Scope: versioning + migration framework ONLY. No router/compute/memory/knowledge/context/
reasoning/planning/runtime; no concrete domain schemas; no domain content.
"""
from __future__ import annotations

from collections import deque
from collections.abc import Callable, Mapping
from typing import Any

from noetica.datacontracts.version import Version

# A migration transforms one payload into the next version's shape. The registry stamps
# the target `schema_version` after applying it, so the function only maps fields.
Migration = Callable[[Mapping[str, Any]], Mapping[str, Any]]


class DataContractError(RuntimeError):
    """Base error for data-contract violations (Law 21)."""


class UnknownContractError(DataContractError):
    """The named contract has no registered versions."""


class UnknownVersionError(DataContractError):
    """A requested version is not registered for the contract."""


class MigrationError(DataContractError):
    """No forward migration path exists, or a downgrade was requested."""


def is_data_contract(obj: object) -> bool:
    """True if `obj` declares a string `SCHEMA_VERSION` (the DataContract marker)."""
    return isinstance(getattr(obj, "SCHEMA_VERSION", None), str)


class DataContractRegistry:
    """Registry of versioned contracts and their forward migrations."""

    def __init__(self) -> None:
        self._versions: dict[str, set[Version]] = {}
        self._edges: dict[str, dict[Version, list[tuple[Version, Migration]]]] = {}

    # ── registration ────────────────────────────────────────────────────────────
    def register_version(self, name: str, version: str) -> None:
        self._versions.setdefault(name, set()).add(Version.parse(version))

    def register_migration(
        self, name: str, from_version: str, to_version: str, migrate: Migration
    ) -> None:
        a = Version.parse(from_version)
        b = Version.parse(to_version)
        if not a < b:
            raise ValueError(f"migration must be forward: {from_version} -> {to_version}")
        self.register_version(name, from_version)
        self.register_version(name, to_version)
        self._edges.setdefault(name, {}).setdefault(a, []).append((b, migrate))

    # ── queries ───────────────────────────────────────────────────────────────
    def versions(self, name: str) -> tuple[Version, ...]:
        if name not in self._versions:
            raise UnknownContractError(name)
        return tuple(sorted(self._versions[name]))

    def latest(self, name: str) -> Version:
        return self.versions(name)[-1]

    # ── migration ───────────────────────────────────────────────────────────────
    def migrate(self, name: str, payload: Mapping[str, Any], to_version: str) -> dict[str, Any]:
        if name not in self._versions:
            raise UnknownContractError(name)
        src_raw = payload.get("schema_version")
        if not isinstance(src_raw, str) or not src_raw:
            raise DataContractError("payload is missing a 'schema_version' (Law 21)")
        src = Version.parse(src_raw)
        dst = Version.parse(to_version)
        if dst not in self._versions[name]:
            raise UnknownVersionError(f"{name} has no registered version {to_version}")
        if src == dst:
            return dict(payload)
        if dst < src:
            raise MigrationError(f"downgrade not supported: {src} -> {dst} for {name}")
        path = self._find_path(name, src, dst)
        if path is None:
            raise MigrationError(f"no migration path {src} -> {dst} for {name}")
        current: dict[str, Any] = dict(payload)
        for to_v, fn in path:
            current = dict(fn(current))
            current["schema_version"] = str(to_v)
        return current

    def read(self, name: str, payload: Mapping[str, Any], expected_version: str) -> dict[str, Any]:
        """Consumer read: return the payload migrated to the declared expected version."""
        return self.migrate(name, payload, expected_version)

    def assert_migratable(self, name: str) -> None:
        """Law 21 governance: every registered version must be reachable by forward
        migration from the earliest (no version gap without a migration)."""
        vs = self.versions(name)
        if len(vs) < 2:
            return
        if self._find_path(name, vs[0], vs[-1]) is None:
            raise MigrationError(
                f"{name}: no complete forward migration path {vs[0]} -> {vs[-1]} (Law 21)"
            )

    # ── internal ────────────────────────────────────────────────────────────────
    def _find_path(
        self, name: str, src: Version, dst: Version
    ) -> list[tuple[Version, Migration]] | None:
        edges = self._edges.get(name, {})
        queue: deque[tuple[Version, list[tuple[Version, Migration]]]] = deque([(src, [])])
        seen: set[Version] = {src}
        while queue:
            node, acc = queue.popleft()
            if node == dst:
                return acc
            for to_v, fn in edges.get(node, []):
                if to_v not in seen:
                    seen.add(to_v)
                    queue.append((to_v, [*acc, (to_v, fn)]))
        return None
