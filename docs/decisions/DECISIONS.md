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
