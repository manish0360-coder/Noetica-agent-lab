# reference/miniflywire — MiniFlyWire Research (Reference Copies)

> **Canonical owner: MiniFlyWire.** Noetica does **not** own this research.

## What this directory is

Synchronized **reference copies** of MiniFlyWire's research corpus — the ecosystem's
cognitive science: research problem, ontology, computational theory, axioms, the
laboratory notebook, and framing documents. They are kept inside the Noetica
repository **only so contributors can read the specifications** they must
re-implement. They are read-only here.

## Ownership and boundary rules (from the Constitution)

- **Canonical owner: MiniFlyWire.** These are reference / synchronized copies; the
  canonical source lives in the separate MiniFlyWire research lab
  (**§11.9 — "MiniFlyWire stays separate"**). When that standalone repository exists,
  it is authoritative and this directory is its mirror.
- **Noetica never owns this research.** Ownership does not transfer by virtue of the
  files sitting in this repo (**§9.2 responsibility matrix — Cognitive research /
  validated-mechanism discovery: Owner = MiniFlyWire**).
- **No implementation may import `reference/miniflywire`.** Nothing in `src/` (or any
  layer) imports this directory. *"Nothing in the ecosystem imports MiniFlyWire"*
  (**Law 4 — MiniFlyWire never becomes production; never imported**). A CI boundary
  check (added in M7) fails the build on any `src/ -> reference/` import.
- **Promotion happens only through validated re-implementation.** A mechanism enters
  Noetica **by re-implementation from a validated specification**, never by copying or
  importing this code/text (**§4.1 Knowledge Flow**, **Law 7 — Promotion requires
  validation and re-implementation**). It must first pass MiniFlyWire's promotion gate
  (§5.5).

## Constitution references

- **§4.1 — Knowledge Flow** (MiniFlyWire → Noetica by re-implementation, never import)
- **Law 4** — MiniFlyWire never becomes production and is never imported
- **Law 7** — Promotion requires validation and re-implementation
- **§11.9** — MiniFlyWire stays a separate repository (research-grade)
- **§9.2** — Responsibility matrix: cognitive research is owned by MiniFlyWire

*Read-only reference. Do not edit these copies to change the science — changes to the
research are made in the canonical MiniFlyWire lab and synced here.*
