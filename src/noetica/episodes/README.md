# src/noetica/episodes — Episode & Episode Store

**Constitution:** §7.5 (the grounded loop's record), §1.10 (Episode definition),
§11.7 (content-hash identity vs provenance), Law 21 (versioned schema).

## Purpose
The **Episode** is the provenance-complete, content-hashed record of one grounded attempt
(task, verdict, cost, environment, provenance). The **Episode Store** is the append-only
persistence of episodes — first-class learning data that survives process exit.

## Responsibilities
- Compute an episode's **reproducible content hash** over its identity inputs only
  (task, verdict outcome, environment); exclude volatile provenance/cost and
  measurement-quality signals (§11.7, D21).
- Provide a **versioned serialization contract** for episodes (Law 21).
- Provide **default append-only stores**: `InMemoryEpisodeStore` (non-persistent) and
  `JsonlEpisodeStore` (persists; survives process exit, §7.5).

## Non-responsibilities (NOT here)
- **Memory** (retrieval + write-filter over episodes) — §6.4, PE-14.
- **Knowledge**, **Context**, **Reasoning**, **Planning**, **Reflection**, **Runtime**.
- Indexed/queryable retrieval, ranking, or a DB backend (added by extraction, Law 8).
- Any **domain episode content**; the concrete verifier/oracle (domain-owned).

## Dependencies
- `noetica.interfaces.episode` (`Episode`, `EpisodeStore`), `.verification` (`Verdict`).
- `noetica.provenance` (canonical hash + provenance serialization).
- Python standard library only. No State dependency (§6.20: Episode ≠ State). No other
  layer, no `reference/`.

## Consumers
- **Memory** (PE-14), **Evaluation** (PE-17), **Reflection** (PE-20).
- **Velith** produces episodes; **MiniFlyWire** consumes distilled datasets.

## Constitution references
§7.5 · §1.10 · §11.7 · Law 21 · §6.20 (Episode distinct from State/Memory/Knowledge).

## Future implementation milestones
- **Now (PE-4):** content hash, serialization, in-memory + JSONL append-only stores.
- **Later (by extraction, Law 8):** indexed/queryable store; compression/retention under
  Data Lifecycle governance (PE-G2, §11.11) — gated.
