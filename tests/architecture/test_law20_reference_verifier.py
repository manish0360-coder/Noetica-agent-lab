"""Law 20 enforcement — Noetica ships ONLY a reference/fake verifier; never a domain oracle.

Scans the platform source for any class implementing `verify(...)` (excluding the frozen
interface Protocol) and asserts the only one is ReferenceVerifier (§6.11, Law 15, Law 20).
"""
from __future__ import annotations

import ast
import pathlib

from noetica.interfaces.verification import Verifier
from noetica.verification import ReferenceVerifier

SRC = pathlib.Path(__file__).resolve().parents[2] / "src" / "noetica"


def _classes_defining_verify() -> dict[str, str]:
    found: dict[str, str] = {}
    for py in SRC.rglob("*.py"):
        if "interfaces" in py.parts:        # skip the protocol definition (contract, not oracle)
            continue
        tree = ast.parse(py.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == "verify":
                        found[node.name] = str(py.relative_to(SRC))
    return found


def test_reference_verifier_satisfies_protocol() -> None:
    assert isinstance(ReferenceVerifier(), Verifier)


def test_platform_ships_only_the_reference_verifier() -> None:
    verifiers = _classes_defining_verify()
    assert set(verifiers) == {"ReferenceVerifier"}, (
        "Law 20/15: the platform must ship only the reference/fake verifier "
        f"(no domain oracle in src/noetica). Found: {verifiers}"
    )
