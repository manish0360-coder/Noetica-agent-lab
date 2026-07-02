"""ReferenceVerifier — the deterministic fake verifier for Noetica self-tests (Law 20).

Purpose: a controllable, fully deterministic stand-in for the `Verifier` protocol so
    Noetica can self-test the verification protocol and (later) the evaluation harness
    WITHOUT any domain oracle. It renders no judgment about a candidate — it returns a
    pre-configured verdict.
Owner: Noetica (Layer 2). Noetica owns the PROTOCOL and this reference; the real ORACLE
    is domain-owned (Velith SWE, later FEA/SPICE; Mini Prometheus) — never here (Law 15).
Consumer: Evaluation Harness (PE-17); platform self-tests; Memory write-filter tests.
Constitution: §6.11; Law 15 (protocol above / oracle in domain); Law 20 (self-tests use a
    reference/fake verifier, never a real domain one).
Future implementation owner: Noetica (this reference only). Domain oracles: the domains.

Scope: a deterministic reference verifier ONLY. NO engineering/manufacturing verification,
NO heuristics, NO simulation, NO Velith functionality; it never inspects the candidate's
domain meaning.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from noetica.interfaces.verification import Verdict, VerdictStatus


class ReferenceVerifier:
    """Deterministic fake verifier. Returns a configured default `Verdict`, optionally
    overridden per key by a fixed script. Same inputs + config -> same verdict."""

    def __init__(
        self,
        default: Verdict | None = None,
        script: Mapping[str, Verdict] | None = None,
        key_fn: Callable[[Any, Any], str] | None = None,
    ) -> None:
        self._default: Verdict = default if default is not None else Verdict(
            status=VerdictStatus.PASSED
        )
        self._script: dict[str, Verdict] = dict(script or {})
        self._key_fn: Callable[[Any, Any], str] = (
            key_fn if key_fn is not None else _default_key
        )

    def verify(self, task: Any, candidate: Any) -> Verdict:
        """Return the scripted verdict for this task/candidate key, else the default.

        No domain judgment: purely a deterministic lookup over the configured script.
        """
        return self._script.get(self._key_fn(task, candidate), self._default)


def _default_key(task: Any, candidate: Any) -> str:
    return str(task)


def always(status: VerdictStatus, confidence: float = 1.0) -> ReferenceVerifier:
    """A reference verifier that always returns the given status (deterministic)."""
    return ReferenceVerifier(default=Verdict(status=status, confidence=confidence))
