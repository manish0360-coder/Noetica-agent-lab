# src/noetica/evaluation — Evaluation Harness & Held-out Lock

**Constitution:** §6.10 (evaluation harness), §5.6 / D8 (held-out lock, frozen evaluation,
staged spending), §11.10 (integrity checks), Law 20 (self-tests use the reference verifier).

## Purpose
The experiment machinery that runs arms over a locked held-out benchmark under **frozen**
evaluation and **measures** them. It exists only to measure mechanisms — **never** to
improve them during execution.

## Responsibilities
- **Arm management** — `register_arm(name, Arm)`.
- **Frozen benchmark execution** — run each arm's solver over the held-out tasks; verify via
  the injected `Verifier`; the harness performs no memory/state writes.
- **Held-out dataset locking** — `HeldoutDataset` is immutable; the harness mechanically
  refuses any held-out task appearing in an arm's memory (`HeldoutViolation`).
- **Provenance recording** — each evaluation is a provenance-complete `Episode` in the
  harness log (never written to arm memory).
- **Integrity enforcement** — arm memory and state must be unchanged during evaluation
  (`FrozenEvaluationViolation`); the held-out set must never enter memory.

## Non-responsibilities (NOT here)
- **Reasoning, planning, reflection, runtime behavior** — the solver (external) holds any
  reasoning; the harness only measures.
- **Optimization policies, benchmark tuning, domain-specific evaluation, engineering
  oracles** — the oracle is the injected `Verifier`; the platform self-tests use only the
  `ReferenceVerifier` (Law 20).

## Dependencies
- `noetica.memory.InMemoryMemoryStore` (PE-14), `noetica.state.InMemoryStateSubstrate` (PE-2),
  `noetica.interfaces.{evaluation,verification,episode,provenance}`. The Verifier is
  injected (self-tests: `ReferenceVerifier`, PE-8).
- Python standard library only. No other layer, no `reference/`.

## Consumers
- Velith configures arms (A0–A4) and the held-out set; Mini Prometheus.

## Constitution references
§6.10 · §5.6 · D8 · §11.10 · Law 20.

## Future implementation milestones
- **Now (PE-17):** `EvaluationHarness` + `HeldoutDataset` + `Arm` (frozen eval, held-out
  lock, provenance, integrity).
- **Later:** staged spending orchestration, effect-size/seed-spread reporting by extraction
  (Law 8). The full compounding experiment run needs the agent (PE-21) and Velith.
