"""PE-4 unit tests — default Episode & Episode Store (§7.5).

Platform tests: no domain oracle, no real verifier (Law 20).
"""
from __future__ import annotations

from pathlib import Path

from noetica.interfaces.episode import Episode, EpisodeStore
from noetica.interfaces.provenance import Provenance
from noetica.interfaces.verification import Verdict, VerdictStatus
from noetica.episodes import (
    InMemoryEpisodeStore,
    JsonlEpisodeStore,
    deserialize_episode,
    episode_content_hash,
    serialize_episode,
)


def _episode(task: str = "t1", status: VerdictStatus = VerdictStatus.PASSED,
             cost: int = 0) -> Episode:
    return Episode(
        task_id=task,
        verdict=Verdict(status=status, confidence=1.0),
        cost={"ms": cost},
        environment={"image": "py3.12"},
        provenance=Provenance(source="agent", transform="propose"),
    )


def test_stores_satisfy_interface_protocol(tmp_path: Path) -> None:
    assert isinstance(InMemoryEpisodeStore(), EpisodeStore)
    assert isinstance(JsonlEpisodeStore(tmp_path / "e.jsonl"), EpisodeStore)


def test_content_hash_reproducible_and_excludes_volatile() -> None:
    a = _episode(cost=10)
    b = _episode(cost=99999)                       # different cost (volatile) ...
    assert episode_content_hash(a) == episode_content_hash(b)   # ... same identity hash
    c = _episode(task="other")
    assert episode_content_hash(a) != episode_content_hash(c)   # identity change -> new hash


def test_append_returns_hash_and_populates_content_hash() -> None:
    store = InMemoryEpisodeStore()
    eid = store.append(_episode())
    assert eid == episode_content_hash(_episode())
    got = store.get(eid)
    assert got is not None and got.content_hash == eid


def test_inmemory_is_append_only_and_ordered() -> None:
    store = InMemoryEpisodeStore()
    store.append(_episode("a"))
    store.append(_episode("b"))
    tasks = [e.task_id for e in store]
    assert tasks == ["a", "b"]


def test_get_missing_returns_none() -> None:
    assert InMemoryEpisodeStore().get("nope") is None


def test_serialization_round_trip() -> None:
    e = _episode()
    restored = deserialize_episode(serialize_episode(e))
    assert restored.task_id == e.task_id
    assert restored.verdict.status == e.verdict.status
    assert restored.provenance == e.provenance


def test_jsonl_store_persists_across_instances(tmp_path: Path) -> None:
    path = tmp_path / "episodes.jsonl"
    s1 = JsonlEpisodeStore(path)
    eid = s1.append(_episode("persisted"))
    # a fresh store over the same file sees the episode (survives 'process exit')
    s2 = JsonlEpisodeStore(path)
    got = s2.get(eid)
    assert got is not None and got.task_id == "persisted"
    assert [e.task_id for e in s2] == ["persisted"]
