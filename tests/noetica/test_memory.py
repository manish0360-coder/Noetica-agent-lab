"""PE-14 unit tests — Memory Framework & Write-Filter (§6.4, D7)."""
from __future__ import annotations

from noetica.interfaces.episode import Episode
from noetica.interfaces.memory import MemoryStore, WriteFilter
from noetica.interfaces.provenance import Provenance
from noetica.interfaces.verification import Verdict, VerdictStatus
from noetica.memory import (
    InMemoryMemoryStore,
    UnfilteredWriteFilter,
    VerifiedSuccessOnlyWriteFilter,
    VerifiedWriteFilter,
)


def _ep(task: str, status: VerdictStatus) -> Episode:
    return Episode(
        task_id=task,
        verdict=Verdict(status=status),
        provenance=Provenance(source="agent", transform="propose"),
    )


def test_store_and_filters_satisfy_protocols() -> None:
    assert isinstance(InMemoryMemoryStore(UnfilteredWriteFilter()), MemoryStore)
    for f in (UnfilteredWriteFilter(), VerifiedWriteFilter(), VerifiedSuccessOnlyWriteFilter()):
        assert isinstance(f, WriteFilter)


def test_unfiltered_admits_everything() -> None:
    f = UnfilteredWriteFilter()
    for s in VerdictStatus:
        assert f.admit(_ep("t", s)) is True


def test_verified_admits_only_passed_and_failed() -> None:
    f = VerifiedWriteFilter()
    assert f.admit(_ep("t", VerdictStatus.PASSED)) is True
    assert f.admit(_ep("t", VerdictStatus.FAILED)) is True
    for s in (VerdictStatus.NO_PATCH, VerdictStatus.PATCH_APPLY_FAILED, VerdictStatus.INFRA_ERROR):
        assert f.admit(_ep("t", s)) is False


def test_verified_success_only_admits_only_passed() -> None:
    f = VerifiedSuccessOnlyWriteFilter()
    assert f.admit(_ep("t", VerdictStatus.PASSED)) is True
    assert f.admit(_ep("t", VerdictStatus.FAILED)) is False


def test_write_filter_is_the_only_gate_to_durability() -> None:
    mem = InMemoryMemoryStore(VerifiedWriteFilter())
    assert mem.write(_ep("ok", VerdictStatus.PASSED)) is True     # admitted -> durable
    assert mem.write(_ep("no", VerdictStatus.NO_PATCH)) is False  # rejected -> not durable
    assert len(mem) == 1
    assert [e.task_id for e in mem] == ["ok"]


def test_recall_is_recency_topk_and_strategy_free() -> None:
    mem = InMemoryMemoryStore(UnfilteredWriteFilter())
    for i in range(5):
        mem.write(_ep(f"t{i}", VerdictStatus.PASSED))
    recalled = mem.recall(query=None, k=2)
    assert [e.task_id for e in recalled] == ["t4", "t3"]          # most recent first
    assert mem.recall(query=None, k=0) == ()


def test_a1_vs_a2_differ_only_in_what_is_written() -> None:
    episodes = [
        _ep("pass", VerdictStatus.PASSED),
        _ep("fail", VerdictStatus.FAILED),
        _ep("nopatch", VerdictStatus.NO_PATCH),
    ]
    a1 = InMemoryMemoryStore(UnfilteredWriteFilter())
    a2 = InMemoryMemoryStore(VerifiedWriteFilter())
    for e in episodes:
        a1.write(e)
        a2.write(e)
    assert {e.task_id for e in a1} == {"pass", "fail", "nopatch"}  # A1 keeps all
    assert {e.task_id for e in a2} == {"pass", "fail"}            # A2 keeps verified only
