"""Noetica · episodes — Episode & Episode Store (§7.5, §1.10).

The provenance-complete, content-hashed record of one grounded attempt and its
append-only store. PE-4 provides the content-hash identity, versioned serialization
(Law 21), and default stores (in-memory + persistent JSONL that survives process exit).
Domain-agnostic; no memory/knowledge/context/reasoning/planning/runtime.
"""
from __future__ import annotations

from noetica.episodes.identity import HASH_INCLUDED_FIELDS, episode_content_hash
from noetica.episodes.serialization import deserialize_episode, serialize_episode
from noetica.episodes.store import InMemoryEpisodeStore, JsonlEpisodeStore

__all__ = [
    "InMemoryEpisodeStore",
    "JsonlEpisodeStore",
    "episode_content_hash",
    "HASH_INCLUDED_FIELDS",
    "serialize_episode",
    "deserialize_episode",
]
