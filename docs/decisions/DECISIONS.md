# DECISIONS — Noetica

**Project:** Noetica (Layer 2 — Agent Intelligence Platform)
**Document type:** Permanent, append-only engineering decision ledger (§11.7). A ratified
decision changes only by a new dated entry that explicitly supersedes the prior one.
**Authority:** subordinate to `docs/constitution/HANDBOOK_v1.1.md` (P.2).

> Velith's decision record (D1–D21) is a **separate, Velith-owned** ledger, archived at
> `reference/velith/DECISIONS.md`. It remains historically authoritative for the
> decisions it records; this ledger records **Noetica-layer** decisions only. Mechanisms
> those decisions produced enter Noetica by extraction (N.3), never by import.

---

## DN-1 — Adopt the Engineering Constitution Handbook v1.1 as highest authority
**Status:** Accepted.
**Decision.** The RATIFIED Handbook v1.1 (`docs/constitution/`) is Noetica's highest
authority; every module, doc, and PR conforms to it. Architecture is not redesigned.
**Rationale.** A decade-scale platform needs one frozen fixed point against which drift
is detected the moment it is proposed (P.1).
**Alternatives rejected.** Treating the audit or plans as authority (they are subordinate).
**Consequences.** Changes to architecture require a ratified CAP (Law 23); AI may
recommend, never ratify (Law 22).

## DN-2 — Transform the repository to the canonical Noetica layout (Plan v2)
**Status:** Accepted.
**Decision.** Restructure to `src/noetica/` (Part VI 1:1), `docs/` (Noetica-owned),
`reference/<layer>/` (read-only, other-layer), enforced by CI. Executed M0–M6, all
history-preserving and reversible from tag `pre-noetica-transform`.
**Rationale.** The repo previously conflated MiniNoetica (education), MiniFlyWire
(research), and Velith (engineering) material with the unbuilt Noetica platform.
**Alternatives rejected.** Rewriting from scratch (loses history); leaving material in
place (boundary rot).
**Consequences.** MiniNoetica code, MiniFlyWire corpus, and Velith docs are read-only
references, never imported; the platform namespace is clean.

## DN-3 — Amendment A1: cross-layer document ownership rule
**Status:** Accepted.
**Decision.** Documentation or code owned by a layer other than Noetica lives under
`reference/<layer>/` with an ownership `README.md`, never in the Noetica namespace.
Promotion/extraction occurs only by validated re-implementation (Law 7) or extraction
(Law 8) — never by import.
**Rationale.** `docs/` is Noetica-owned; placing other-layer material there would
silently transfer ownership (§9.2, §11.9).
**Alternatives rejected.** Keeping MiniFlyWire/Velith docs under `docs/`.
**Consequences.** Applied to MiniFlyWire (M3), MiniNoetica (M3.5), Velith (M5).

## DN-4 — Constitutional boundaries are mechanically enforced in CI
**Status:** Accepted.
**Decision.** `tools/check_boundaries.py` + `tests/architecture/` + a CI workflow fail
the build if the platform imports `reference/`, legacy, or a domain layer, or if
`reference/` becomes executable platform code (Law 4/9, D11, §11.10). Verified
fail-closed.
**Rationale.** The Constitution is enforced, not merely stated (§11.10).
**Alternatives rejected.** Relying on review discipline alone.
**Consequences.** Every push/PR is gated; a boundary violation cannot merge green.
**Operational note.** The git index is kept on reliable local storage (not the working
mount) to avoid index corruption observed on the FUSE mount during transformation; no
history impact.

## DN-5 — Freeze Platform Engineering Roadmap v1
**Status:** Accepted.
**Decision.** The Platform Engineering implementation order is frozen as
`docs/roadmap/PLATFORM_ENGINEERING_ROADMAP_v1.md`: PE-1..PE-21 ordered strictly by
dependency depth (lowest first), plus gated PE-G1..G5. Tag: `pe-roadmap-v1`.
**Rationale.** Prevents ad-hoc, feature-popularity ordering; guarantees every mechanism is
built on already-verified foundations (Law 8, Principle 4). The order is a valid topological
sort of the dependency DAG (no cycles), mirroring the Code-Flow invariant (Law 9).
**Alternatives rejected.** Top-down/feature-first (forces stubs + rework); breadth-first
(would build Context/Reasoning before Memory/Episode); experiment-first (stubs the very
mechanisms §1.7 must measure).
**Consequences.** PE-4 is Observability. Milestones proceed one at a time with per-milestone
verification (mypy --strict, unit tests, boundary fail-closed, interface conformance).
Gated milestones are built only when their gate is met (§11.8). Changes require a superseding
decision (§11.7).

## DN-6 — Platform Engineering Roadmap v1.1 (supersedes DN-5 ordering)
**Status:** Accepted. **Supersedes:** DN-5 (ordering only).
**Decision.** Adopt `docs/roadmap/PLATFORM_ENGINEERING_ROADMAP_v1.1.md`. Move **Episode &
Episode Store to PE-4** (immediately after State + Provenance); shift the independent
Tier-1 services to PE-5..PE-9 ordered by first consumer (Observability, Budget, Data
Contract, Reference Verifier, Guardrails). Tier-2+ (PE-10..PE-21) and the gated set are
unchanged. Tag: `pe-roadmap-v1.1` (v1 retained for history, §11.6).
**Rationale.** Dependency review found Episode's only hard platform prerequisite is
Provenance (done); Observability and Episode are incomparable in the DAG, so v1 ordered
them by cross-cutting importance, not dependency. v1 also overstated Episode's dependency
on DataContract (Episode carries schema_version; the framework isn't required to build the
record). v1.1 orders strictly by true dependency, ties broken by first-consumer proximity
(Law 8). Remains a valid topological sort (no cycles, Law 9).
**Alternatives rejected.** Keeping Observability first (importance-based, not dependency);
depth-only tiebreak (does not reflect that Episode is dependency-ready now and is the
cohesive data-spine continuation).
**Consequences.** PE-4 is Episode & Episode Store. Per-milestone verification unchanged.

## DN-7 — Reasoning Runtime ownership boundary, injection, and the state blackboard (pre-PE-18)
**Status:** Accepted. **Scope:** architecture hardening ratified before PE-18; no roadmap/
dependency/interface/mechanism change.
**Decision.** The ownership boundary of the Reasoning Runtime (§6.7) is fixed:
- Reasoning OWNS only: (1) inference iteration; (2) search / backtracking; (3) retries;
  (4) reasoning-loop control flow; (5) verification-seam *invocation* (the invocation point
  of the Verifier protocol — not the protocol or oracle).
- Reasoning explicitly does NOT own: planning (§6.8), reflection (§6.9), memory (§6.4),
  knowledge (§6.5), Context ownership (§6.6 — it *consumes* Context), tool execution (§6.12),
  State ownership (§6.1 — it *transforms* shared state, does not own the substrate), the
  verification protocol/oracle (§6.11, Law 15), and the runtime lifecycle (§6.3/§6.18, PE-21).
- **Tool and Skill capabilities are consumed ONLY through dependency injection, never by
  direct import** (consistent with every Tier-2+ mechanism). Reasoning's declared import
  dependencies remain **{State, Context, Router, Budget}** per Roadmap v1.1 (DN-6), unchanged.
- The **State Substrate (§6.1) is the shared control plane (blackboard)** the Constitution
  requires ("every other subsystem reads and writes it"; Principle 2; D9). Reasoning is a
  control plane OVER the shared substrate (reads Context/State; writes results to State with
  provenance) — never a control-flow homunculus.
**Rationale.** Prevents the forbidden homunculus (§1.9, §6.7) and the mechanically-preventable
cyclic dependencies of Law 9: owning Planning/Reflection/tool-execution would create
Reasoning↔Planning / Reasoning↔Reflection cycles. Resolves independent-review claims 1, 3, 5.
**Alternatives rejected.** Reasoning importing the Tool/Skill runtimes (over-coupling → use
injection); Reasoning owning planning/reflection (homunculus + cycle); a strict
all-messages-through-the-blackboard model (over-engineering — the Constitution requires
state-centric transformations over a shared substrate, not that every call route through it).
**Consequences.** PE-18 is built to this boundary. Enforced mechanically by DN-8 / FIX-1.

## DN-8 — Mechanical intra-platform DAG enforcement (FIX-1)
**Status:** Accepted.
**Decision.** `tools/check_boundaries.py` gains `check_intra_platform_dag()`: each
`src/noetica` subsystem may import `noetica.interfaces.*` and itself freely, and may import
ANOTHER subsystem only if declared in the policy (`INTRA_ALLOWED`, derived from Roadmap v1.1 /
DN-6). Any other cross-subsystem import **fails the build (fail-closed)**. The policy is
self-checked for acyclicity, and every subsystem directory must have a policy entry (an
undeclared directory fails). This mechanically prevents back-edges / cycles inside Noetica
(Law 9, §11.10) — in particular `reasoning→planning`, `reasoning→reflection`,
`planning→reflection`.
**Rationale.** Closes the enforcement gap found in the pre-PE-18 review: the *layer* DAG
(Noetica vs reference/domain) was enforced, but *intra-Noetica* subsystem acyclicity was not.
§11.10 mandates mechanical enforcement of the DAG.
**Alternatives rejected.** Relying on roadmap discipline alone (not fail-closed); ranking by
PE number (PE order ≠ dependency order, e.g. `state` (PE-2) depends on `provenance` (PE-3) —
the policy uses declared dependency adjacency instead).
**Consequences.** Adds `tests/architecture/test_intra_platform_dag.py` with fail-closed proofs.
No roadmap, interface, or mechanism change.
