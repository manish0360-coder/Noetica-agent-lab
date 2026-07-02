"""PE-16 unit tests — Context Engine (§6.6).

Platform tests: explicit-policy assembly from State/Memory/Knowledge under a budget.
"""
from __future__ import annotations

from typing import Any

from noetica.context import ContextEngine, ContextPolicy
from noetica.interfaces.context import ContextAssembler
from noetica.interfaces.episode import Episode
from noetica.interfaces.provenance import Provenance
from noetica.interfaces.verification import Verdict, VerdictStatus
from noetica.knowledge import EntityQuery, InMemoryKnowledgeStore
from noetica.memory import InMemoryMemoryStore, UnfilteredWriteFilter
from noetica.state import InMemoryStateSubstrate


def _prov() -> Provenance:
    return Provenance(source="test", transform="seed")


def _episode(task: str) -> Episode:
    return Episode(task_id=task, verdict=Verdict(status=VerdictStatus.PASSED), provenance=_prov())


def _fixture() -> tuple[InMemoryStateSubstrate, InMemoryMemoryStore, InMemoryKnowledgeStore]:
    state = InMemoryStateSubstrate()
    state.put("goal_note", "N", _prov())
    memory = InMemoryMemoryStore(UnfilteredWriteFilter())
    for i in range(3):
        memory.write(_episode(f"e{i}"))
    knowledge = InMemoryKnowledgeStore()
    knowledge.upsert("k1", {"kind": "fact", "v": 1}, _prov())
    knowledge.upsert("k2", {"kind": "other"}, _prov())
    return state, memory, knowledge


def _engine(policy: ContextPolicy, cost_one: bool = True) -> ContextEngine:
    state, memory, knowledge = _fixture()
    cost = (lambda c: 1) if cost_one else None
    return ContextEngine(state, memory, knowledge, policy, cost_fn=cost)


def test_engine_satisfies_assembler_protocol() -> None:
    assert isinstance(_engine(ContextPolicy()), ContextAssembler)


def test_assembles_from_all_three_sources_per_policy() -> None:
    eng = _engine(ContextPolicy(state_keys=("goal_note",), memory_k=2,
                                knowledge_query=EntityQuery(kind="fact")))
    ctx = eng.assemble(goal="g", token_budget=100)
    sources = [it.source for it in ctx.items]
    assert sources.count("state") == 1
    assert sources.count("memory") == 2       # 2 most-recent episodes
    assert sources.count("knowledge") == 1    # only kind=fact


def test_empty_policy_yields_empty_context() -> None:
    ctx = _engine(ContextPolicy()).assemble(goal="g", token_budget=100)
    assert ctx.items == ()


def test_budget_prefix_truncation() -> None:
    eng = _engine(ContextPolicy(state_keys=("goal_note",), memory_k=3), cost_one=True)
    # order: 1 state + 3 memory = 4 items, each cost 1
    ctx = eng.assemble(goal="g", token_budget=2)
    assert len(ctx.items) == 2                 # prefix of 2 fits
    assert [it.source for it in ctx.items] == ["state", "memory"]
    assert ctx.token_budget == 2


def test_zero_budget_yields_nothing() -> None:
    eng = _engine(ContextPolicy(state_keys=("goal_note",), memory_k=3))
    assert eng.assemble(goal="g", token_budget=0).items == ()


def test_reads_live_sources_not_owned() -> None:
    # The engine holds references it does not own: mutating memory after construction is
    # reflected on the next assemble (it does not snapshot/persist).
    state, memory, knowledge = _fixture()
    eng = ContextEngine(state, memory, knowledge,
                        ContextPolicy(memory_k=5), cost_fn=lambda c: 1)
    before = len(eng.assemble("g", 100).items)
    memory.write(_episode("new"))
    after = len(eng.assemble("g", 100).items)
    assert after == before + 1


def test_deterministic() -> None:
    eng = _engine(ContextPolicy(state_keys=("goal_note",), memory_k=2))
    a = eng.assemble("g", 100)
    b = eng.assemble("g", 100)
    assert [it.ref for it in a.items] == [it.ref for it in b.items]
