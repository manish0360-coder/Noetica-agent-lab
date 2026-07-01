# reference/velith — Velith Engineering Documents (Reference, Read-Only)

> **Canonical owner: Velith** — a **separate repository** (Layer 3, Engineering
> Intelligence). Noetica does **not** own these documents and never imports them.

## What this directory is

Velith-authored governance and milestone documents that were tangled into this
repository's history during early development. **Velith is a separate project and
repository** that *consumes* Noetica through published interfaces (§4.2 Code Flow,
§2.3). Its canonical documents live in the Velith repository; the copies here are
**reference copies**, retained for provenance — these are the decisions (D1–D21) and
milestone specs (M0–M2) whose *reusable mechanisms* seed Noetica by **extraction**
(N.3), never by import.

Contents: `DECISIONS.md` (D1–D21), `PROJECT_STATE.md`, `M0_SPEC.md`, `M1_SPEC.md`,
`M1_IMPLEMENTATION_HANDOFF.md`, `M2_SPEC.md`, `M2_IMPLEMENTATION_HANDOFF.md`, `NOTES.md`.

## Ownership and boundary rules (from the Constitution)

- **Canonical owner: Velith** (separate repository; §11.9 packaging; §2.3 charter).
  Ownership does not transfer to Noetica by these files living here.
- **No implementation may import `reference/velith`.** Nothing in `src/` imports it
  (Law 4/9); the CI boundary check (`tools/check_boundaries.py`) fails the build on any
  `src/ -> reference/` import.
- **Mechanisms move up only by extraction.** A Velith mechanism enters Noetica behind
  a versioned interface only with a real consumer + a credible second (Law 8, §11.4,
  N.3) — never by importing these documents or their code.
- **Amendment A1:** documentation owned by another layer lives under
  `reference/<layer>/`, never in the Noetica namespace.

## Constitution references

- **§4.2 — Code Flow** (Velith consumes Noetica; interface owned above, impl below)
- **§2.3 — Velith charter**; **N.3 — reconciliation** (mechanisms extracted to Noetica)
- **Law 8** — platform grows by extraction; **Law 9 / §11.9** — DAG + separate packaging
- **Amendment A1** — cross-layer document ownership (this transformation)

*Read-only reference. Not executable platform code. The authoritative, current versions
live in the separate Velith repository.*
