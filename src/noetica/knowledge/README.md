# src/noetica/knowledge — Knowledge Store Engine

**Constitution:** §6.5 (knowledge store engine), §6.20 (distinct from Memory/Context),
§6.1/D9 (state-centric), Law 3 (engine vs content), Law 21 (versioned records).

## Purpose
The typed, provenance-tracked, **schema-agnostic** semantic/graph store *engine* — how to
store, index, and retrieve structured knowledge (entities, relations, properties). Noetica
owns the **engine**; domains **populate** it with content.

## Responsibilities
- Store typed, provenance-tracked **entity records** (`upsert`/`put_entity`) and **graph
  relations** (`add_relation`) — persistence is provenance-tracked via the State substrate.
- **Index** entities by `kind` and relations by subject/object/predicate.
- **Retrieve**: `get`/`get_record`, `entities(EntityQuery)`, `relations(RelationQuery)`,
  `neighbors()` (graph traversal), `query(pattern)`.
- Versioned serialization of records/relations (Law 21).

## Non-responsibilities (NOT here)
- **Any domain knowledge**: engineering facts, manufacturing data, physics rules,
  ontologies — domain-owned CONTENT populated into the engine.
- **Prompts, reasoning, planning, memory behavior, world models** — separate subsystems
  (Memory §6.4, Context §6.6 are distinct — §6.20).

## Dependencies
- `noetica.state.InMemoryStateSubstrate` (PE-2; provenance-tracked persistence),
  `noetica.interfaces.provenance.Provenance`, `noetica.provenance` (serialization).
- Python standard library only. No other layer, no `reference/`.

## Consumers
- Context (PE-16); Velith (engineering ontology); Mini Prometheus (mfg concepts).

## Constitution references
§6.5 · §6.20 · §6.1/D9 · Law 3 · Law 21.

## Future implementation milestones
- **Now (PE-13):** `InMemoryKnowledgeStore` — typed records, relations, kind/relation
  indexes, retrieval, serialization.
- **Later (by extraction, Law 8):** persistent/graph-DB backends, richer query language,
  constraints/transitions — added when a real consumer needs them.
