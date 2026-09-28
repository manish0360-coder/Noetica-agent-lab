# Release Notes — noetica 1.0.0

**Tag:** `v1.0.0` · **Package:** `noetica` 1.0.0 · **Decision:** DN-9 · **Status:** Released.

## Summary

**Noetica is now an installable versioned package.** This release packages the frozen
`platform-engineering-v1` platform, PE-1 to PE-21, **unchanged**, as a standard Python wheel. No
interface, mechanism, test or boundary changed.

## Package

- **Wheel:** `noetica-1.0.0-py3-none-any.whl`. Pure Python; ships exactly `noetica/` plus the PEP 561
  `py.typed` marker.
- **Runtime dependencies:** none (standard library only).
- **Python:** `>= 3.10`, tested on 3.10, 3.11, 3.12, 3.13 and 3.14. The floor comes from the source: the
  runtime PEP 604 union `Activation` in `runtime/runtime.py` needs 3.10, and the suite fails on 3.9.
- **Build:** PEP 517, with hatchling pinned to 1.32.4. The version comes from `noetica.__version__`.
- **Public surface:** `noetica` and its 22 packages — `interfaces`, `state`, `provenance`, `episodes`,
  `observability`, `budget`, `datacontracts`, `verification`, `guardrails`, `router`, `compute`,
  `tools`, `knowledge`, `memory`, `skills`, `context`, `evaluation`, `reasoning`, `planning`,
  `reflection`, `runtime` and `sdk`.
- **Install (pinned):** `pip install "noetica @ git+https://github.com/manish0360-coder/Noetica-agent-lab@v1.0.0"`.

## Verification

- `tools/verify_installed_wheel.py` (new) runs 23 checks.
  - **Wheel contents:** only `noetica/` and its dist-info. It includes `py.typed` and all 22 packages, and
    no tests, tools, docs, `reference/`, caches or source-control files.
  - **Metadata:** name and version, `Requires-Python`, and no `Requires-Dist`.
  - **Hygiene:** no machine paths or credential material. Every packaged module imports only `noetica`
    and the standard library, and nothing from MiniFlyWire, Velith, Mini Prometheus, `reference/` or
    legacy code.
  - **Clean install:** it installs with no package index into a fresh virtual environment. From a
    neutral directory, with no `PYTHONPATH` and no repository path on `sys.path`, all 88 modules import
    from the installed wheel.
  - **Consistency:** the installed version, `__version__` and the source version agree. Nothing
    forbidden is loaded or needed.
  - **Behaviour:** the 166 platform behaviour tests pass against the installed wheel.
- CI `package.yml`, on Python 3.10–3.14: the full suite (181 tests) from the source tree, plus the
  verifier.
- Constitution boundary checks and the 15 architecture tests (`constitution.yml`) are unchanged.

## Compatibility

The interface surface is frozen since PE-1, and changes require a superseding decision or a CAP.
SemVer 1.0.0 records that stability.

## Not included

- Integration with Velith or Mini Prometheus.
- Any promoted cognitive mechanism (the Primitive Registry is empty).
- The gated mechanisms PE-G1 to PE-G5.
- Publication to PyPI.
