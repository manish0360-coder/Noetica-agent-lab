"""PE-13 unit tests — Knowledge Store engine (§6.5).

Platform tests: schema-agnostic storage/indexing/retrieval/graph + provenance. No domain
knowledge (arbitrary kinds/props stand in for domain content).
"""
from __future__ import annotations

import pytest

from noetica.interfaces.knowledge import KnowledgeStore
from noetica.interfaces.provenance import Provenance
from noetica.knowledge import (
    EntityQuery,
    InMemoryKnowledgeStore,
    RelationQuery,
    deserialize_record,
    serialize_record,
)


def _p(t: str = "ingest") -> Provenance:
    return Provenance(source="test", transform=t)


def test_satisfies_interface_protocol() -> None:
    assert isinstance(InMemoryKnowledgeStore(), KnowledgeStore)


def test_upsert_get_and_provenance_retained() -> None:
    ks = InMemoryKnowledgeStore()
    ks.upsert("e1", {"kind": "widget", "size": 3}, _p("derive"))
    assert ks.get("e1") == {"kind": "widget", "size": 3}
    rec = ks.get_record("e1")
    assert rec is not None and rec.kind == "widget" and rec.provenance.transform == "derive"


def test_get_missing_returns_none() -> None:
    assert InMemoryKnowledgeStore().get("absent") is None


def test_query_entities_by_kind_and_where() -> None:
    ks = InMemoryKnowledgeStore()
    ks.upsert("a", {"kind": "node", "color": "red"}, _p())
    ks.upsert("b", {"kind": "node", "color": "blue"}, _p())
    ks.upsert("c", {"kind": "edge", "color": "red"}, _p())
    by_kind = ks.query(EntityQuery(kind="node"))
    assert {r.entity_id for r in by_kind} == {"a", "b"}
    red_nodes = ks.query(EntityQuery(kind="node", where={"color": "red"}))
    assert {r.entity_id for r in red_nodes} == {"a"}


def test_reupsert_updates_kind_index() -> None:
    ks = InMemoryKnowledgeStore()
    ks.upsert("x", {"kind": "old"}, _p())
    ks.upsert("x", {"kind": "new"}, _p())
    assert ks.query(EntityQuery(kind="old")) == ()
    assert {r.entity_id for r in ks.query(EntityQuery(kind="new"))} == {"x"}


def test_graph_relations_and_neighbors() -> None:
    ks = InMemoryKnowledgeStore()
    ks.add_relation("a", "part_of", "b", _p())
    ks.add_relation("a", "part_of", "c", _p())
    ks.add_relation("d", "linked", "b", _p())
    assert set(ks.neighbors("a", predicate="part_of")) == {"b", "c"}
    to_b = ks.query(RelationQuery(obj="b"))
    assert {r.subject for r in to_b} == {"a", "d"}
    part_of = ks.query(RelationQuery(predicate="part_of"))
    assert len(part_of) == 2


def test_relation_provenance_retained() -> None:
    ks = InMemoryKnowledgeStore()
    ks.add_relation("a", "rel", "b", _p("assert"))
    rel = ks.query(RelationQuery(subject="a"))[0]
    assert rel.provenance.transform == "assert"


def test_query_rejects_bad_pattern() -> None:
    with pytest.raises(TypeError):
        InMemoryKnowledgeStore().query("not-a-query")


def test_record_serialization_round_trip() -> None:
    ks = InMemoryKnowledgeStore()
    ks.upsert("e", {"kind": "k", "v": [1, 2]}, _p())
    rec = ks.get_record("e")
    assert rec is not None
    assert deserialize_record(serialize_record(rec)) == rec


def test_non_mapping_value_is_wrapped() -> None:
    ks = InMemoryKnowledgeStore()
    ks.upsert("n", 42, _p())
    assert ks.get("n") == {"value": 42}
