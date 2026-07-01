"""PE-3 unit tests — default Provenance & Lineage mechanism (Constitution §6.2).

Platform tests: no domain oracle, no real verifier (Law 20). Pure provenance mechanism.
"""
from __future__ import annotations

from noetica.interfaces.provenance import Provenance
from noetica.provenance import (
    LineageNode,
    ProvenanceLedger,
    content_hash,
    deserialize_node,
    deserialize_provenance,
    serialize_node,
    serialize_provenance,
)


def _p(source: str, transform: str, inputs: tuple[str, ...] = ()) -> Provenance:
    return Provenance(source=source, transform=transform, inputs=inputs)


def test_content_hash_deterministic_and_identifying() -> None:
    a = _p("s", "t")
    assert content_hash(a) == content_hash(_p("s", "t"))          # deterministic
    assert content_hash(a) != content_hash(_p("s", "t2"))          # sensitive to content


def test_provenance_serialization_round_trip() -> None:
    p = Provenance(source="s", transform="t", inputs=("a", "b"), attributes={"k": 1})
    assert deserialize_provenance(serialize_provenance(p)) == p


def test_record_returns_content_hash_and_is_idempotent() -> None:
    led = ProvenanceLedger()
    p = _p("agent", "derive")
    nid1 = led.record(p, ref="x@1")
    nid2 = led.record(p, ref="x@1")
    assert nid1 == nid2 == content_hash(p)
    assert led.nodes() == (nid1,)                                  # no duplicate


def test_get_returns_immutable_node_with_ref() -> None:
    led = ProvenanceLedger()
    nid = led.record(_p("s", "t"), ref="k@1")
    node = led.get(nid)
    assert node is not None and node.ref == "k@1"
    assert isinstance(node, LineageNode)


def test_lineage_ancestors_traced_through_inputs() -> None:
    led = ProvenanceLedger()
    root = led.record(_p("input", "ingest"))                       # no inputs
    mid = led.record(_p("agent", "step1", inputs=(root,)))
    leaf = led.record(_p("agent", "step2", inputs=(mid,)))
    assert led.parents(leaf) == (mid,)
    assert set(led.ancestors(leaf)) == {mid, root}                 # transitive
    assert led.ancestors(root) == ()                               # roots have none


def test_ancestors_cycle_safe() -> None:
    led = ProvenanceLedger()
    # craft two nodes referencing each other by id (degenerate cycle)
    a_id = "a"
    b_id = "b"
    led.record(_p("s", "ta", inputs=(b_id,)), node_id=a_id)
    led.record(_p("s", "tb", inputs=(a_id,)), node_id=b_id)
    # must terminate and not loop forever
    assert set(led.ancestors(a_id)) == {a_id, b_id}


def test_trace_returns_existing_nodes_only() -> None:
    led = ProvenanceLedger()
    root = led.record(_p("input", "ingest"))
    leaf = led.record(_p("agent", "s", inputs=(root, "missing-id")))
    traced_ids = {n.node_id for n in led.trace(leaf)}
    assert root in traced_ids and leaf in traced_ids
    assert "missing-id" not in traced_ids                          # unknown input skipped


def test_node_serialization_round_trip() -> None:
    led = ProvenanceLedger()
    nid = led.record(_p("s", "t", inputs=("i1",)), ref="k@2")
    node = led.get(nid)
    assert node is not None
    assert deserialize_node(serialize_node(node)) == node
