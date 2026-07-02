# src/noetica/datacontracts — Data Contract & Versioning

**Constitution:** §4.3 (Experience Flow is contract-governed), Law 21 (Data Contract Law),
§11.7 (versioning), §11.10 (data-contract check), §11.11 (lifecycle operates on contracts).

## Purpose
The framework that makes the Experience Flow contract-governed. Every episode, dataset,
and derived-question payload carries a `schema_version`; a schema change requires a new
version **and** a registered forward migration; a consumer reads against a declared
contract version. Upward data contracts are held to the same rigor as downward interfaces.

## Responsibilities
- Represent versions (`Version`: semantic major.minor.patch, comparable).
- Register contract versions and **forward migrations** between them.
- `migrate()` / `read()`: bring a payload from its declared `schema_version` to a target
  version by applying the registered migration chain (stamping the version at each step).
- `assert_migratable()`: Law 21 governance — every registered version must be reachable by
  forward migration (no version gap without a migration).
- Reject: missing `schema_version`, unknown version, downgrade, or missing migration path.

## Non-responsibilities (NOT here)
- **Concrete domain schemas** (episode/dataset content) — domain-owned; the episode schema
  itself lives in `noetica.episodes`.
- **Data lifecycle** (compression/retention/pruning) — §11.11, gated **PE-G2**.
- Router, compute, memory, knowledge, context, reasoning, planning, runtime.

## Dependencies
- Python standard library only. Structurally relates to
  `noetica.interfaces.datacontract.DataContract` (the `SCHEMA_VERSION` marker).
- **No other platform mechanism** (Tier-1), no other layer, no `reference/`.

## Consumers
- Episode/Memory schema evolution; the Experience Flow (Velith → Noetica → MiniFlyWire).
- The §11.10 data-contract CI check builds on `assert_migratable`.

## Constitution references
§4.3 · Law 21 · §11.7 · §11.10 · §11.11.

## Future implementation milestones
- **Now (PE-7):** `Version`, `DataContractRegistry` (register/migrate/read/assert).
- **Later (by extraction, Law 8):** registration of the concrete platform schemas as they
  evolve; the Data Lifecycle framework (PE-G2, §11.11) operating on these contracts.
