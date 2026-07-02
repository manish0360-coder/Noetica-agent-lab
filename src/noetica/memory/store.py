"""InMemoryMemoryStore — the default typed Memory Store engine (§6.4).

Purpose: durable persistence of episodic experience, gated SOLELY by a WriteFilter. The
    recall path is a fixed, strategy-free recency retriever that is IDENTICAL regardless of
    the write filter — so the compounding experiment's only legal difference between arms is
    the write filter (D7, §11.10).
Owner: Noetica (Layer 2).
Consumer: Context (PE-16), Evaluation Harness (PE-17); Velith; Mini Prometheus.
Constitution: §6.4; §6.20 (Memory = persistence of experience, distinct from Knowledge/
    Context); D7; Law 13.
Future implementation owner: Noetica.

Scope: a reusable memory MECHANISM — a store + the write-filter gate. NO retrieval
strategies, reasoning, planning, reflection, autonomous behavior, conversation loops,
learning policies, heuristics, or domain knowledge. Backed by an EpisodeStore (PE-4).
"""
from __future__ import annotations

from collections.abc import Iterator

from noetica.episodes import InMemoryEpisodeStore
from noetica.interfaces.episode import Episode, EpisodeStore
from noetica.interfaces.memory import WriteFilter


class InMemoryMemoryStore:
    """Durable episodic memory whose ONLY admission gate is the write filter.

    `recall` is a fixed most-recent-k retriever, independent of the write filter (the D7
    invariant: hold the retriever identical; vary only the write filter).
    """

    def __init__(self, write_filter: WriteFilter, store: EpisodeStore | None = None) -> None:
        self._filter = write_filter
        self._store: EpisodeStore = store if store is not None else InMemoryEpisodeStore()
        self._admitted: list[Episode] = []

    def write(self, episode: Episode) -> bool:
        """Admit-or-reject via the write filter (the ONLY gate). Returns True if the
        episode became durable memory, False if the filter rejected it."""
        if not self._filter.admit(episode):
            return False
        self._store.append(episode)
        self._admitted.append(episode)
        return True

    def recall(self, query: object, k: int = 5) -> tuple[Episode, ...]:
        """Fixed, strategy-free retrieval: the most recent k admitted episodes (most
        recent first). Independent of the write filter and of `query` content — richer
        retrieval is Context (PE-16), deliberately out of scope here (D7 integrity)."""
        if k <= 0:
            return ()
        return tuple(reversed(self._admitted[-k:]))

    def __len__(self) -> int:
        return len(self._admitted)

    def __iter__(self) -> Iterator[Episode]:
        return iter(tuple(self._admitted))
