"""PE-21 — anti-homunculus: the integrator implements/imports no cognition.

runtime/ and sdk/ must not import the reasoning/planning/reflection MECHANISMS; cognition is
injected via interfaces only (spec §16, §1.9/§6.7).
"""
from __future__ import annotations

import ast
import pathlib

SRC = pathlib.Path(__file__).resolve().parents[2] / "src" / "noetica"
_FORBIDDEN = {"reasoning", "planning", "reflection"}


def _mechanism_imports(subsystem: str) -> set[str]:
    found: set[str] = set()
    for py in (SRC / subsystem).rglob("*.py"):
        for node in ast.walk(ast.parse(py.read_text(encoding="utf-8"))):
            mods = []
            if isinstance(node, ast.Import):
                mods = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module and not (node.level or 0):
                mods = [node.module]
            for m in mods:
                parts = m.split(".")
                if len(parts) >= 2 and parts[0] == "noetica" and parts[1] in _FORBIDDEN:
                    found.add(parts[1])
    return found


def test_runtime_imports_no_cognition_mechanism() -> None:
    assert _mechanism_imports("runtime") == set()


def test_sdk_imports_no_cognition_mechanism() -> None:
    assert _mechanism_imports("sdk") == set()
