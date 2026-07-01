"""Default Episode Stores — append-only, content-hashed, survive process exit (§7.5).

Purpose: the default implementations of the `EpisodeStore` interface. An episode is the
    provenance-complete, content-hashed record of one grounded attempt; the store is
    append-only. `JsonlEpisodeStore` persists so episodes survive process exit (§7.5, the
    defining property); `InMemoryEpisodeStore` is the simple non-persistent default.
Owner: Noetica (Layer 2).
Consumer: Memory (PE-14), Evaluation (PE-17), Reflection (PE-20); Velith (produces).
Constitution: §7.5; §1.10; §11.7 (content-hash identity); Law 21.
Future implementation owner: Noetica (indexed/queryable backends by extraction, Law 8).

Scope: episode record + append-only store ONLY. No Memory/Knowledge/Context/Reasoning/
Planning/Runtime; no retrieval ranking; no domain content.
"""
from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from typing import Iterator

from noetica.interfaces.episode import Episode
from noetica.episodes.identity import episode_content_hash
from noetica.episodes.serialization import deserialize_episode, serialize_episode


def _with_hash(episode: Episode) -> tuple[Episode, str]:
    """Return the episode with its content_hash populated, and that hash."""
    eid = episode.content_hash or episode_content_hash(episode)
    stored = episode if episode.content_hash else replace(episode, content_hash=eid)
    return stored, eid


class InMemoryEpisodeStore:
    """Append-only, in-memory episode store. Does NOT survive process exit."""

    def __init__(self) -> None:
        self._log: list[Episode] = []
        self._by_id: dict[str, Episode] = {}

    def append(self, episode: Episode) -> str:
        stored, eid = _with_hash(episode)
        self._log.append(stored)
        self._by_id[eid] = stored          # latest wins for identical identity
        return eid

    def get(self, episode_id: str) -> Episode | None:
        return self._by_id.get(episode_id)

    def __iter__(self) -> Iterator[Episode]:
        return iter(tuple(self._log))       # immutable view in append order


class JsonlEpisodeStore:
    """Append-only JSONL episode store that survives process exit (§7.5, D16.6).

    One serialized episode per line. Re-implements the episode->JSONL pattern (never
    imported from MiniNoetica; D11).
    """

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.touch(exist_ok=True)

    def append(self, episode: Episode) -> str:
        stored, eid = _with_hash(episode)
        with open(self._path, "a", encoding="utf-8") as f:
            f.write(json.dumps(serialize_episode(stored), ensure_ascii=False) + "\n")
        return eid

    def get(self, episode_id: str) -> Episode | None:
        found: Episode | None = None
        for ep in self:
            if ep.content_hash == episode_id:
                found = ep                  # latest wins
        return found

    def __iter__(self) -> Iterator[Episode]:
        episodes: list[Episode] = []
        if self._path.exists():
            with open(self._path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        episodes.append(deserialize_episode(json.loads(line)))
        return iter(episodes)
