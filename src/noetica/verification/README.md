# src/noetica/verification — Verification Protocol Support (Reference Verifier)

**Constitution:** §6.11 (verification protocol; oracle in the domain), Law 15
(protocol owned above / oracle owned by the domain), Law 16 (verdicts may be
distributions), Law 20 (self-tests use a reference/fake verifier, never a domain oracle).

## Purpose
Noetica owns the verification **protocol** (`Verifier`, `Verdict`, `VerdictStatus` — in
the frozen interface surface). This subsystem provides only the **deterministic reference
/ fake verifier** that Noetica's own tests and the evaluation harness run against, so the
platform can validate the protocol and harness **without any domain oracle** (Law 20).

## Responsibilities
- Provide `ReferenceVerifier`: returns a configured default `Verdict`, optionally
  overridden per key by a fixed script; fully deterministic (same inputs + config → same
  verdict). Convenience `always(status)`.

## Non-responsibilities (NOT here — this is the core Law 15 boundary)
- **No real oracle.** No SWE test-runner, FEA/SPICE, or manufacturing check — those are
  **domain-owned** (Velith, Mini Prometheus).
- **No engineering-domain verification, heuristics, simulation, or Velith functionality.**
  The reference verifier never inspects a candidate's domain meaning.
- Memory, knowledge, context, reasoning, planning, runtime, evaluation harness.

## Dependencies
- `noetica.interfaces.verification` (`Verifier`, `Verdict`, `VerdictStatus`).
- Python standard library only. No other platform mechanism, no other layer, no `reference/`.

## Consumers
- Evaluation Harness (PE-17); platform self-tests; Memory write-filter tests (PE-14).

## Constitution references
§6.11 · Law 15 · Law 16 · Law 20.

## Future implementation milestones
- **Now (PE-8):** `ReferenceVerifier` (deterministic fake).
- **Never here:** real oracles — those are implemented by the domain layers against this
  same protocol (Velith `SweVerifier`, etc.).
