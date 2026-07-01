# src/noetica/state — State Substrate

**Constitution:** §6.1 (the State Substrate is the platform's *true core*). Governing
authority: `docs/constitution/HANDBOOK_v1.1.md`.

## Purpose
The persistent, typed, provenance-tracked shared state that every other mechanism reads
and writes. Generators, planners, verifiers, and learners are *transformations over this
shared state* — the substrate is named the core so the architecture cannot drift into a
control-flow-centric "bag of agents" (Principle 2, D9).

## Responsibilities
- Store typed values under keys, each write producing an **immutable `StateRecord`**
  carrying its value, `Provenance`, per-key `version`, and global `revision`.
- Preserve full **history** per key and expose **immutable snapshots** of the whole
  substrate at a revision.
- Integrate **provenance** on every write (§6.2) — no untracked writes.
- Provide a **versioned serialization contract** for records/snapshots (Law 21).

## Non-responsibilities (explicitly NOT here)
- **Memory** (episodic/experience persistence + write-filter) — §6.4, a distinct subsystem.
- **Knowledge** (typed semantic/graph store) — §6.5.
- **Context** (working-set assembly) — §6.6.
- Reasoning, planning, runtime, reflection, routing, tools, skills — all separate.
- Any **domain content** (engineering/manufacturing) — Law 3/5. No Velith or Mini
  Prometheus logic.
- Belief/probabilistic state — a *future* evolution (§8.3), not this default.

## Dependencies
- `noetica.interfaces.state.StateSubstrate` (the contract it satisfies).
- `noetica.interfaces.provenance.Provenance` (the provenance value type).
- `noetica.provenance` (canonical provenance serialization/identity — PE-3).
- Python standard library only. No third-party, no other layer, no `reference/`.

## Consumers
- **Velith** (Layer 3): the artifact-under-design lives on the substrate.
- **Mini Prometheus** (Layer 4): twin content syncs onto the substrate.
- Every future Noetica mechanism (memory, context, planning, …) transforms this state.
- All access is through the `StateSubstrate` interface — never Noetica's internal types.

## Constitution references
§6.1 (state substrate / core) · §6.2 (provenance) · §6.20 (State ≠ Memory ≠ Knowledge)
· Principle 2 & D9 (state-centric) · Law 3 (mechanism, not content) · Law 13 (no
duplicated abstractions) · Law 21 (versioned data contract).

## Future implementation milestones
- **Now (PE-2):** `InMemoryStateSubstrate` — append-only, versioned, in-memory default.
- **Later (by extraction, Law 8 / gated, Appendix D):**
  - Durable/persistent substrate backend (behind the same interface).
  - **Belief / probabilistic state** — confidence + epistemic/aleatoric separation
    (§6.1 evolution, §8.3), gated on reaching the first approximate (PCB/FEA) rung.
  - Substrate-level query/index surface, added only when a real consumer needs it.
