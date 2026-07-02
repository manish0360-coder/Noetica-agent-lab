# src/noetica/memory — Memory Framework & Write-Filter

**Constitution:** §6.4 (memory framework + write-filter), §6.20 (distinct from Knowledge/
Context), D6-D8 / §7.6 (compounding experiment; write-filter is the single manipulated
variable), §11.10 (experiment-integrity test), Law 13.

## Purpose
Persistence of episodic experience over time, whose durability is decided **solely** by the
constitutional **write filter**. The write filter is the single manipulated variable of the
compounding experiment (verified vs. unverified retention).

## Responsibilities
- `write(episode) -> bool` — admit-or-reject via the write filter (the **only** gate); a
  rejected episode never becomes durable memory.
- **Write filters** (constitutional gates over the grounded verdict):
  - `UnfilteredWriteFilter` (A1) — retain all (RAG/null control).
  - `VerifiedWriteFilter` (A2) — retain only verification-passing solutions and verified
    failure signatures (the verified-vs-unverified distinction).
  - `VerifiedSuccessOnlyWriteFilter` (A4) — retain only passing solutions (ablation).
- `recall(query, k)` — a **fixed, strategy-free** most-recent-k retriever, identical across
  all write filters (the D7 integrity invariant).

## Non-responsibilities (NOT here)
- **Retrieval strategies** (similarity/embedding/ranking) — richer retrieval is Context
  (PE-16); the retriever here is deliberately trivial and filter-independent.
- **Reasoning, planning, reflection, autonomous behavior, conversation loops, learning
  policies, heuristics, domain knowledge** — none of these; this is a mechanism, not an agent.

## Dependencies
- `noetica.episodes` (Episode store, PE-4), `noetica.interfaces.{episode,memory,verification}`.
  Provenance (PE-3) is carried by Episode. **No other mechanism dependency.**
- Python standard library only. No other layer, no `reference/`.

## Consumers
- Context (PE-16), Evaluation Harness (PE-17); Velith; Mini Prometheus.

## Constitution references
§6.4 · §6.20 · D6-D8 · §7.6 · §11.10 · Law 13.

## Future implementation milestones
- **Now (PE-14):** `InMemoryMemoryStore` + write filters (A1/A2/A4).
- **Later:** richer retrieval is Context (PE-16); forgetting/retention primitives promoted
  from MiniFlyWire by re-implementation (Law 7); data-lifecycle governance gated (PE-G2).
