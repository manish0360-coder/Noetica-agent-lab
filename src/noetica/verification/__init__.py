"""Noetica · verification — Verification protocol support (§6.11).

Noetica owns the verification PROTOCOL (`Verifier`/`Verdict`, in the interface surface);
the concrete ORACLE is domain-owned (Law 15). PE-8 provides only the deterministic
`ReferenceVerifier` — the fake verifier Noetica self-tests run against (Law 20), never a
real domain oracle. No engineering/manufacturing/heuristic/simulation logic.
"""
from __future__ import annotations

from noetica.verification.reference import ReferenceVerifier, always

__all__ = ["ReferenceVerifier", "always"]
