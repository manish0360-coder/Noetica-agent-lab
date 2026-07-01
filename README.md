# Noetica — Agent Intelligence Platform

**Layer 2 of the MiniFlyWire → Noetica → Velith → Mini Prometheus ecosystem.**
Noetica is the **domain-agnostic platform**: it owns reusable *mechanisms*, typed
*interfaces*, and the shared *state substrate*. It contains **no** engineering or
manufacturing content, no domain verifier/oracle, and no central "mind"
(the Prime Directive of Noetica, Constitution §6).

> Governing authority: **`docs/constitution/HANDBOOK_v1.1.md`** (RATIFIED, frozen).
> This repository and every file in it conform to it. Architecture is not redesigned here.

## Status

**Pre-implementation platform skeleton.** The canonical structure, interface namespace,
and constitutional boundaries exist and are mechanically enforced. Mechanisms are **not**
built speculatively: each is added only when a real consumer needs it and a credible
second is on the horizon — the platform **grows by extraction** (Law 8, §13.6). Empty
subsystem packages are honest placeholders, never stubs pretending to work.

See **`ROADMAP.md`** for the sequence, **`docs/registry/PRIMITIVE_REGISTRY.md`** for what
(if anything) has been promoted/extracted, and **`docs/decisions/DECISIONS.md`** for the
Noetica decision ledger.

## Repository structure

```
src/noetica/         Layer 2 platform. Subsystem packages map 1:1 to Constitution Part VI:
  interfaces/        typed public contracts (Verifier, MemoryStore, Plan, Tool, ...)
  state/ provenance/ runtime/ memory/ knowledge/ context/ reasoning/ planning/
  reflection/ evaluation/ verification/ tools/ skills/ budget/ router/ guardrails/
  observability/ sdk/ compute/ datacontracts/
tests/
  noetica/           platform tests (reference/fake verifier only — Law 20)
  architecture/      CONSTITUTION-ENFORCEMENT tests (import DAG, boundaries)
docs/                Noetica-owned docs: constitution/ decisions/ registry/ vision/
                     audits/ transformation/
tools/               constitutional enforcement scripts (check_boundaries.py)
examples/ configs/ plugins/
reference/           READ-ONLY, zero-coupling. Never imported by src/ (CI-enforced):
  miniflywire/       MiniFlyWire research corpus (owner: MiniFlyWire)
  mininoetica/       MiniNoetica education code (owner: MiniNoetica; D11)
  velith/            Velith engineering docs (owner: Velith, separate repo)
```

## Constitutional boundaries (mechanically enforced)

CI fails the build (`.github/workflows/constitution.yml`) if any of these break:

- `src/noetica` (or tests) imports anything from `reference/` — Law 4, D11
- the platform imports a legacy or domain module (`core`, `phase2_memory`, `agent_zero`,
  `velith`, `mini_prometheus`) — Law 9 (strict acyclic dependency DAG)
- `reference/` becomes executable platform code (it is excluded from the test suite)

Run locally: `python tools/check_boundaries.py` · tests: `pytest tests/architecture`.

## What Noetica is not

Not a chatbot, not an agent framework, not an LLM wrapper, not a domain application.
Engineering content lives in **Velith** (a separate repository that consumes Noetica);
cognitive research lives in **MiniFlyWire** (a separate lab whose validated mechanisms
Noetica re-implements, never imports — §4.1 Knowledge Flow).

## License / quality bar

Production-quality platform code, provenance and observability from the first commit
(§6.2, Principle 7). Research-grade reference material is quarantined under `reference/`.
