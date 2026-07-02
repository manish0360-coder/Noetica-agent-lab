"""Experiment-integrity enforcement (§11.10, D7): the A1 and A2 arms must share an
IDENTICAL retriever — the only legal difference is the write filter.

The MemoryStore.recall path must not depend on the write filter. Given episodes that BOTH
filters admit, recall must be identical across arms.
"""
from __future__ import annotations

from noetica.interfaces.episode import Episode
from noetica.interfaces.provenance import Provenance
from noetica.interfaces.verification import Verdict, VerdictStatus
from noetica.memory import InMemoryMemoryStore, UnfilteredWriteFilter, VerifiedWriteFilter


def _ep(task: str) -> Episode:
    # PASSED is admitted by BOTH A1 and A2 -> isolates the retriever from the filter.
    return Episode(
        task_id=task,
        verdict=Verdict(status=VerdictStatus.PASSED),
        provenance=Provenance(source="agent", transform="propose"),
    )


def test_a1_and_a2_share_an_identical_retriever() -> None:
    episodes = [_ep(f"t{i}") for i in range(6)]
    a1 = InMemoryMemoryStore(UnfilteredWriteFilter())
    a2 = InMemoryMemoryStore(VerifiedWriteFilter())
    for e in episodes:
        a1.write(e)
        a2.write(e)
    # identical retriever across arms for every k
    for k in (0, 1, 3, 6, 10):
        assert [e.task_id for e in a1.recall(None, k)] == [e.task_id for e in a2.recall(None, k)]
