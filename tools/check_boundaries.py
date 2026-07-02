#!/usr/bin/env python3
"""Constitutional boundary enforcement — static import + packaging checks.

This is ENFORCEMENT TOOLING, not a platform mechanism (Constitution §11.10). It
mechanically enforces the boundaries the Handbook declares, so the build fails the
moment a violation is introduced.

Enforced rules:
  1. src/noetica imports nothing from reference/            (Law 4, D11)
  2. no forbidden dependency direction / no legacy/domain    (Law 3/5/9)
     import from the platform: reference, core, phase2_memory,
     agent_zero (MiniNoetica), velith, mini_prometheus (domains)
  3. package DAG holds: the platform (src/noetica) and the
     platform tests (tests/) never import reference code      (Law 9/12/19)
  4. reference code is not executable platform code:
     reference/ is excluded from the pytest test suite         (D11, §11.9)
  5. INTRA-PLATFORM subsystem DAG (FIX-1, DN-8): a src/noetica
     subsystem may import only its declared dependency
     subsystems (Roadmap v1.1) + noetica.interfaces + itself.
     Mechanically prevents back-edges / cyclic dependencies
     inside Noetica (Law 9) — e.g. reasoning->planning,
     reasoning->reflection, planning->reflection.

Exit 0 = clean. Exit 1 = one or more violations (build must fail).
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_NOETICA = ROOT / "src" / "noetica"

# Top-level modules the PLATFORM (src/noetica) and platform tests may never import.
FORBIDDEN_TOP = {
    "reference",                                   # Law 4 / D11 — reference never imported
    "core", "phase2_memory", "agent_zero",         # MiniNoetica legacy (D11)
    "velith", "mini_prometheus",                   # domain layers — no upward/domain import (Law 9)
}

# Directories whose .py files are subject to the platform import rules.
PLATFORM_DIRS = [ROOT / "src" / "noetica", ROOT / "tests"]

# ── Intra-Noetica subsystem dependency policy (FIX-1) ─────────────────────────────
# Derived STRICTLY from Platform Engineering Roadmap v1.1 hard-dependencies (DN-6). A
# subsystem may import `noetica.interfaces.*` and itself freely; it may import ANOTHER
# noetica subsystem only if that subsystem is listed here. Because the policy is a DAG,
# no cyclic dependency (Law 9) can be introduced — a back-edge is a forbidden import.
# `INTEGRATOR` = the PE-21 developer surface / agent lifecycle: may import any subsystem
# (nothing imports it, so no cycle).
INTEGRATOR = "*"

INTRA_ALLOWED: dict[str, set[str]] = {
    "interfaces":    set(),
    "provenance":    set(),
    "state":         {"provenance"},
    "episodes":      {"provenance"},
    "observability": set(),
    "budget":        set(),
    "datacontracts": set(),
    "verification":  set(),
    "guardrails":    set(),
    "router":        {"budget"},
    "compute":       {"budget"},
    "tools":         {"budget"},
    "knowledge":     {"state", "provenance"},
    "memory":        {"episodes", "provenance"},
    "skills":        {"tools", "state"},
    "context":       {"memory", "knowledge", "state"},
    "evaluation":    {"memory", "episodes", "verification", "state"},
    "reasoning":     {"state", "context", "router", "budget"},
    "planning":      {"reasoning", "state"},
    "reflection":    {"reasoning", "episodes", "state"},
    "runtime":       {INTEGRATOR},
    "sdk":           {INTEGRATOR},
}


def _top_level_imports(pyfile: Path) -> tuple[set[str], str | None]:
    try:
        tree = ast.parse(pyfile.read_text(encoding="utf-8"))
    except SyntaxError as e:
        return set(), f"{pyfile.relative_to(ROOT)}: syntax error: {e}"
    tops: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                tops.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if (node.level or 0) > 0:
                continue  # relative import within a package — always legal
            if node.module:
                tops.add(node.module.split(".")[0])
    return tops, None


def check_platform_imports() -> list[str]:
    violations: list[str] = []
    for base in PLATFORM_DIRS:
        if not base.exists():
            continue
        for py in sorted(base.rglob("*.py")):
            tops, err = _top_level_imports(py)
            if err:
                violations.append(err)
                continue
            for bad in sorted(tops & FORBIDDEN_TOP):
                violations.append(
                    f"{py.relative_to(ROOT)} imports forbidden top-level '{bad}' "
                    f"(Constitution Law 4/9, D11)"
                )
    return violations


def check_reference_not_executable() -> list[str]:
    violations: list[str] = []
    cfg = ROOT / "pytest.ini"
    if not cfg.exists():
        return ["pytest.ini missing — cannot prove reference/ is excluded from the suite"]
    text = cfg.read_text(encoding="utf-8")
    testpaths = ""
    norecurse = ""
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("testpaths"):
            testpaths = s.split("=", 1)[1].strip() if "=" in s else ""
        if s.startswith("norecursedirs"):
            norecurse = s.split("=", 1)[1].strip() if "=" in s else ""
    if "reference" in testpaths:
        violations.append("pytest.ini testpaths includes reference/ — reference is not executable platform code (D11)")
    if "reference" not in norecurse:
        violations.append("pytest.ini norecursedirs must list 'reference' so reference code is never collected (D11, §11.9)")
    return violations


# ── FIX-1: intra-platform subsystem DAG ────────────────────────────────────────────
def _subsystem_of(pyfile: Path) -> str | None:
    """The src/noetica subsystem a file belongs to (None for files directly in src/noetica)."""
    rel = pyfile.relative_to(SRC_NOETICA).parts
    return rel[0] if len(rel) > 1 else None


def _imported_noetica_subsystems(pyfile: Path) -> tuple[set[str], str | None]:
    try:
        tree = ast.parse(pyfile.read_text(encoding="utf-8"))
    except SyntaxError as e:
        return set(), f"{pyfile.relative_to(ROOT)}: syntax error: {e}"
    subs: set[str] = set()
    for node in ast.walk(tree):
        modules: list[str] = []
        if isinstance(node, ast.Import):
            modules = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and not (node.level or 0) and node.module:
            modules = [node.module]
        for module in modules:
            parts = module.split(".")
            if len(parts) >= 2 and parts[0] == "noetica":
                subs.add(parts[1])
    return subs, None


def _policy_cycle() -> list[str] | None:
    """Detect a cycle in INTRA_ALLOWED (a self-check that the policy is a DAG)."""
    subsystems = set(INTRA_ALLOWED)
    color: dict[str, int] = {}  # 0=unvisited,1=in-stack,2=done

    integrators = {n for n, a in INTRA_ALLOWED.items() if INTEGRATOR in a}

    def edges(node: str) -> set[str]:
        allowed = INTRA_ALLOWED.get(node, set())
        if INTEGRATOR in allowed:
            # Integrators (PE-21) may import any NON-integrator subsystem; they never
            # import each other, so no cycle arises among them.
            return {s for s in subsystems if s != node and s not in integrators}
        return allowed

    def dfs(node: str, stack: list[str]) -> list[str] | None:
        color[node] = 1
        stack.append(node)
        for nxt in sorted(edges(node)):
            if color.get(nxt, 0) == 1:
                return stack[stack.index(nxt):] + [nxt]
            if color.get(nxt, 0) == 0:
                found = dfs(nxt, stack)
                if found:
                    return found
        stack.pop()
        color[node] = 2
        return None

    for s in sorted(subsystems):
        if color.get(s, 0) == 0:
            found = dfs(s, [])
            if found:
                return found
    return None


def check_intra_platform_dag() -> list[str]:
    violations: list[str] = []
    if not SRC_NOETICA.exists():
        return violations
    # (a) fail-closed: every subsystem directory must be declared in the policy.
    for path in sorted(SRC_NOETICA.iterdir()):
        if path.is_dir() and not path.name.startswith("__") and path.name not in INTRA_ALLOWED:
            violations.append(
                f"subsystem '{path.name}' has no intra-platform dependency policy entry "
                f"(add it to INTRA_ALLOWED, Roadmap v1.1) — fail-closed"
            )
    # (b) the policy itself must be acyclic.
    cycle = _policy_cycle()
    if cycle is not None:
        violations.append(f"intra-platform dependency policy contains a cycle: {' -> '.join(cycle)}")
    # (c) every actual cross-subsystem import must be allowed.
    for pyfile in sorted(SRC_NOETICA.rglob("*.py")):
        subsystem = _subsystem_of(pyfile)
        if subsystem is None or subsystem not in INTRA_ALLOWED:
            continue
        allowed = INTRA_ALLOWED[subsystem]
        if INTEGRATOR in allowed:
            continue
        imported, err = _imported_noetica_subsystems(pyfile)
        if err:
            violations.append(err)
            continue
        for target in sorted(imported):
            if target == subsystem or target == "interfaces":
                continue
            if target not in allowed:
                violations.append(
                    f"{pyfile.relative_to(ROOT)}: subsystem '{subsystem}' imports '{target}' — "
                    f"not a declared dependency (Law 9 DAG; allowed: {sorted(allowed)})"
                )
    return violations


def main() -> int:
    violations: list[str] = []
    violations += check_platform_imports()
    violations += check_reference_not_executable()
    violations += check_intra_platform_dag()
    if violations:
        print("CONSTITUTION BOUNDARY VIOLATIONS (build fails):")
        for v in violations:
            print(f"  ✗ {v}")
        return 1
    print("Constitution boundary checks: PASS "
          "(no reference/legacy/domain imports; reference excluded from suite; "
          "intra-platform subsystem DAG acyclic)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
