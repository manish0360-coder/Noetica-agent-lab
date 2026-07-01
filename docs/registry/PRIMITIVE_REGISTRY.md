# Primitive Registry — Noetica (§11.5)

**Purpose.** The permanent, versioned registry of every **promoted primitive**
(from MiniFlyWire, by re-implementation — Law 7) and **extracted mechanism**
(from a domain consumer, by extraction — Law 8) that Noetica owns. It is the
authoritative answer to *"what mechanisms does Noetica own, why, and since when."*

> **Rule (§11.5):** nothing enters Noetica's public surface without a registry entry.

## Registry

| Name | Source | Interface | Version | Evidence / Rationale | Status |
|------|--------|-----------|---------|----------------------|--------|
| *(none yet)* | — | — | — | Platform is pre-implementation; no mechanism has a real consumer yet (Law 8). | — |

**Status: EMPTY by design.** No primitive has been promoted and no mechanism extracted,
because no consumer yet exercises one (the Velith consumer lives in a separate repo).
Entries are added only when the promotion gate (§5.5) or extraction test (§11.4) passes.

## Candidate seeds (NOT yet promoted — recorded for provenance)

These exist as patterns in `reference/` and are eligible *candidates* only; each must
pass its gate and be **re-implemented** (never imported) before it earns a registry row:

| Candidate | Origin (reference) | Would seed | Gate required |
|-----------|--------------------|------------|---------------|
| `forgetting` rule | `reference/mininoetica/phase2_memory/forgetting.py` | `noetica/memory` | MiniFlyWire promotion gate (§5.5) |
| `KnowledgeState` update rule | `reference/mininoetica/phase2_memory/knowledge_state.py` | `noetica/memory` | MiniFlyWire promotion gate |
| validated `Verdict` | `reference/mininoetica/phase2_memory/verdict.py` | `noetica/verification` | extraction test (§11.4) w/ Velith consumer |
| single-owner model call | `reference/mininoetica/core/llm.py` | `noetica/router` | extraction test (D16.4) |
| episode → JSONL | `reference/mininoetica/core/logger.py` | `noetica/observability` | extraction test |

**Permanently barred (Law 7):** `reference/mininoetica/phase2_memory/judge.py`
(LLM-as-judge) may never be promoted.
