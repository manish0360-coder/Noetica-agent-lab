"""ProvenanceLedger — the default Provenance & Lineage mechanism (§6.2).

Purpose: record the derivation of every belief/artifact and trace its lineage — where a
    value came from, which transform produced it, from which inputs. This is the reusable
    provenance mechanism the State Substrate needs to answer "why does this exist?"
Owner: Noetica (Layer 2).
Consumer: the State Substrate; Velith; Mini Prometheus (all via provenance nodes).
Constitution: §6.2; Principle 7 (provenance non-negotiable); Law 18.
Future implementation owner: Noetica (this in-memory default; durable/graph backends
    later, by extraction — Law 8).

Scope: provenance/lineage ONLY. No Memory, Episodes, Knowledge, Runtime, Planner, Router;
no domain content.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from noetica.interfaces.provenance import Provenance
from noetica.provenance.identity import (
    PROV_SCHEMA_VERSION,
    content_hash,
    deserialize_provenance,
    serialize_provenance,
)


@dataclass(frozen=True)
class LineageNode:
    """An immutable node in the lineage graph: an identified provenance record.

    `node_id` is the content hash of the provenance (stable identity). `ref` optionally
    names the artifact produced (e.g. a state key@version). `parents` are the input node
    ids taken from the provenance (`Provenance.inputs`).
    """

    node_id: str
    provenance: Provenance
    ref: str | None = None
    schema_version: str = PROV_SCHEMA_VERSION

    @property
    def parents(self) -> tuple[str, ...]:
        """Input node ids this node was derived from (from Provenance.inputs)."""
        return tuple(self.provenance.inputs)


class ProvenanceLedger:
    """In-memory default lineage store: record provenance and trace derivation."""

    def __init__(self) -> None:
        self._nodes: dict[str, LineageNode] = {}

    def record(
        self, provenance: Provenance, ref: str | None = None, node_id: str | None = None
    ) -> str:
        """Record a provenance node; returns its stable id (content hash by default).

        Idempotent: recording identical provenance yields the same id and does not
        duplicate the node.
        """
        nid = node_id if node_id is not None else content_hash(provenance)
        if nid not in self._nodes:
            self._nodes[nid] = LineageNode(node_id=nid, provenance=provenance, ref=ref)
        return nid

    def get(self, node_id: str) -> LineageNode | None:
        return self._nodes.get(node_id)

    def parents(self, node_id: str) -> tuple[str, ...]:
        node = self._nodes.get(node_id)
        return node.parents if node else ()

    def ancestors(self, node_id: str) -> tuple[str, ...]:
        """Transitive input closure (derivation lineage), cycle-safe. Excludes self."""
        seen: set[str] = set()
        order: list[str] = []
        stack: list[str] = list(self.parents(node_id))
        while stack:
            nid = stack.pop()
            if nid in seen:
                continue
            seen.add(nid)
            order.append(nid)
            stack.extend(self.parents(nid))
        return tuple(order)

    def trace(self, node_id: str) -> tuple[LineageNode, ...]:
        """The node and its known ancestors, as recorded LineageNodes (existing only)."""
        ids = [node_id, *self.ancestors(node_id)]
        return tuple(self._nodes[i] for i in ids if i in self._nodes)

    def nodes(self) -> tuple[str, ...]:
        return tuple(self._nodes.keys())


# ── versioned serialization contract for lineage nodes (Law 21) ────────────────
def serialize_node(n: LineageNode) -> dict[str, Any]:
    return {
        "schema_version": n.schema_version,
        "node_id": n.node_id,
        "ref": n.ref,
        "provenance": serialize_provenance(n.provenance),
    }


def deserialize_node(d: Mapping[str, Any]) -> LineageNode:
    return LineageNode(
        node_id=d["node_id"],
        provenance=deserialize_provenance(d["provenance"]),
        ref=d.get("ref"),
        schema_version=d.get("schema_version", PROV_SCHEMA_VERSION),
    )
