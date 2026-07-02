"""InMemoryKnowledgeStore — the default Knowledge Store engine (§6.5).

Purpose: the reusable, schema-agnostic, typed, provenance-tracked semantic/graph store
    ENGINE — storage, indexing, and retrieval of entities and relations. Noetica owns the
    engine; domains POPULATE it with content. Entity persistence is provenance-tracked via
    the State substrate (state-centric, D9); the graph and indexes live in the engine.
Owner: Noetica (Layer 2).
Consumer: Context (PE-16); Velith / Mini Prometheus (populate content).
Constitution: §6.5; §6.20 (distinct from Memory/Context); §6.1/D9 (state-centric);
    Law 3 (engine vs content).
Future implementation owner: Noetica (engine); domains (content).

Scope: storage + indexing + retrieval + graph relations ONLY. NO domain knowledge,
engineering facts, manufacturing data, physics rules, prompts, reasoning, planning,
memory behavior, or world models.
"""
from __future__ import annotations

from typing import Any, Mapping

from noetica.interfaces.provenance import Provenance
from noetica.knowledge.records import (
    EntityQuery,
    KnowledgeRecord,
    Relation,
    RelationQuery,
)
from noetica.state import InMemoryStateSubstrate


def _entity_key(entity_id: str) -> str:
    return f"knowledge:entity:{entity_id}"


class InMemoryKnowledgeStore:
    """Typed, provenance-tracked, indexed graph store. Entities persist through the State
    substrate; kind and relation indexes are maintained in the engine."""

    def __init__(self, substrate: InMemoryStateSubstrate | None = None) -> None:
        self._substrate = substrate if substrate is not None else InMemoryStateSubstrate()
        self._by_kind: dict[str, set[str]] = {}
        self._relations: list[Relation] = []
        self._rel_by_subject: dict[str, list[int]] = {}
        self._rel_by_object: dict[str, list[int]] = {}
        self._rel_by_predicate: dict[str, list[int]] = {}

    # ── KnowledgeStore interface ────────────────────────────────────────────────
    def upsert(self, entity_id: str, data: Any, provenance: Provenance) -> None:
        if isinstance(data, Mapping):
            kind = str(data.get("kind", ""))
            props: Mapping[str, Any] = dict(data)
        else:
            kind = ""
            props = {"value": data}
        self.put_entity(entity_id, kind, props, provenance)

    def get(self, entity_id: str) -> Any | None:
        record = self.get_record(entity_id)
        return record.data if record is not None else None

    def query(self, pattern: Any) -> tuple[Any, ...]:
        if isinstance(pattern, EntityQuery):
            return self.entities(pattern)
        if isinstance(pattern, RelationQuery):
            return self.relations(pattern)
        raise TypeError("query pattern must be an EntityQuery or a RelationQuery")

    # ── typed entity surface ─────────────────────────────────────────────────────
    def put_entity(
        self, entity_id: str, kind: str, data: Mapping[str, Any], provenance: Provenance
    ) -> None:
        previous = self.get_record(entity_id)
        if previous is not None and previous.kind != kind:
            self._by_kind.get(previous.kind, set()).discard(entity_id)
        self._substrate.put(_entity_key(entity_id), {"kind": kind, "data": dict(data)}, provenance)
        self._by_kind.setdefault(kind, set()).add(entity_id)

    def get_record(self, entity_id: str) -> KnowledgeRecord | None:
        state_record = self._substrate.get_record(_entity_key(entity_id))
        if state_record is None:
            return None
        value = state_record.value
        return KnowledgeRecord(
            entity_id=entity_id,
            kind=value["kind"],
            data=value["data"],
            provenance=state_record.provenance,
        )

    def entities(self, query: EntityQuery) -> tuple[KnowledgeRecord, ...]:
        if query.kind is not None:
            ids = sorted(self._by_kind.get(query.kind, set()))
        else:
            ids = sorted(eid for group in self._by_kind.values() for eid in group)
        results: list[KnowledgeRecord] = []
        for eid in ids:
            record = self.get_record(eid)
            if record is None:
                continue
            if query.where is not None and not _matches(record.data, query.where):
                continue
            results.append(record)
        return tuple(results)

    # ── typed relation / graph surface ────────────────────────────────────────
    def add_relation(
        self, subject: str, predicate: str, obj: str, provenance: Provenance
    ) -> None:
        index = len(self._relations)
        self._relations.append(Relation(subject=subject, predicate=predicate, obj=obj, provenance=provenance))
        self._rel_by_subject.setdefault(subject, []).append(index)
        self._rel_by_object.setdefault(obj, []).append(index)
        self._rel_by_predicate.setdefault(predicate, []).append(index)

    def relations(self, query: RelationQuery) -> tuple[Relation, ...]:
        if query.subject is not None:
            candidates = self._rel_by_subject.get(query.subject, [])
        elif query.obj is not None:
            candidates = self._rel_by_object.get(query.obj, [])
        elif query.predicate is not None:
            candidates = self._rel_by_predicate.get(query.predicate, [])
        else:
            candidates = list(range(len(self._relations)))
        results = []
        for i in candidates:
            rel = self._relations[i]
            if query.subject is not None and rel.subject != query.subject:
                continue
            if query.predicate is not None and rel.predicate != query.predicate:
                continue
            if query.obj is not None and rel.obj != query.obj:
                continue
            results.append(rel)
        return tuple(results)

    def neighbors(self, entity_id: str, predicate: str | None = None) -> tuple[str, ...]:
        rels = self.relations(RelationQuery(subject=entity_id, predicate=predicate))
        return tuple(r.obj for r in rels)

    # ── introspection ────────────────────────────────────────────────────────────
    def kinds(self) -> tuple[str, ...]:
        return tuple(sorted(k for k, ids in self._by_kind.items() if ids))


def _matches(data: Mapping[str, Any], where: Mapping[str, Any]) -> bool:
    return all(data.get(k) == v for k, v in where.items())
