"""FIX-1 / DN-8 — mechanical intra-Noetica DAG enforcement (Law 9, §11.10).

Proves the checker (a) passes on the current tree, (b) encodes the reasoning boundaries,
and (c) FAILS CLOSED on injected back-edges (reasoning->planning, reasoning->reflection,
planning->reflection).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import check_boundaries as cb  # noqa: E402


def test_intra_platform_dag_is_clean() -> None:
    assert cb.check_intra_platform_dag() == []


def test_policy_is_acyclic() -> None:
    assert cb._policy_cycle() is None


def test_reasoning_boundaries_encoded() -> None:
    # Law 9 / DN-7: reasoning must not depend on planning or reflection; planning not on reflection.
    assert "planning" not in cb.INTRA_ALLOWED["reasoning"]
    assert "reflection" not in cb.INTRA_ALLOWED["reasoning"]
    assert "reflection" not in cb.INTRA_ALLOWED["planning"]
    assert cb.INTRA_ALLOWED["reasoning"] == {"state", "context", "router", "budget"}


def _probe(subsystem: str, module: str) -> list[str]:
    probe = ROOT / "src" / "noetica" / subsystem / "_probe_backedge.py"
    probe.write_text(f"from noetica.{module} import _x  # injected back-edge\n", encoding="utf-8")
    try:
        return cb.check_intra_platform_dag()
    finally:
        probe.unlink()


def test_fail_closed_reasoning_cannot_import_planning() -> None:
    v = _probe("reasoning", "planning")
    assert any("reasoning" in s and "planning" in s for s in v), v


def test_fail_closed_reasoning_cannot_import_reflection() -> None:
    v = _probe("reasoning", "reflection")
    assert any("reasoning" in s and "reflection" in s for s in v), v


def test_fail_closed_planning_cannot_import_reflection() -> None:
    v = _probe("planning", "reflection")
    assert any("planning" in s and "reflection" in s for s in v), v


def test_fail_closed_cli_exits_nonzero_on_back_edge() -> None:
    probe = ROOT / "src" / "noetica" / "reasoning" / "_probe_cli.py"
    probe.write_text("from noetica.reflection import _x\n", encoding="utf-8")
    try:
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "check_boundaries.py")],
            capture_output=True, text=True,
        )
        assert result.returncode == 1
        assert "reasoning" in result.stdout and "reflection" in result.stdout
    finally:
        probe.unlink()
