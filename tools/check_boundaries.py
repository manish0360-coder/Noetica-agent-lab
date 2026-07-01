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

Exit 0 = clean. Exit 1 = one or more violations (build must fail).
"""
from __future__ import annotations
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Top-level modules the PLATFORM (src/noetica) and platform tests may never import.
FORBIDDEN_TOP = {
    "reference",                                   # Law 4 / D11 — reference never imported
    "core", "phase2_memory", "agent_zero",         # MiniNoetica legacy (D11)
    "velith", "mini_prometheus",                   # domain layers — no upward/domain import (Law 9)
}

# Directories whose .py files are subject to the platform import rules.
PLATFORM_DIRS = [ROOT / "src" / "noetica", ROOT / "tests"]


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


def main() -> int:
    violations: list[str] = []
    violations += check_platform_imports()
    violations += check_reference_not_executable()
    if violations:
        print("CONSTITUTION BOUNDARY VIOLATIONS (build fails):")
        for v in violations:
            print(f"  ✗ {v}")
        return 1
    print("Constitution boundary checks: PASS "
          "(no reference/legacy/domain imports in the platform; reference excluded from suite)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
