"""Constitution enforcement tests (§11.10). Wrap tools/check_boundaries.py so the
platform test suite fails on any boundary violation. These are enforcement checks,
not platform mechanisms."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import check_boundaries as cb  # noqa: E402


def test_platform_never_imports_reference_legacy_or_domain():
    v = cb.check_platform_imports()
    assert v == [], "Boundary violations (Law 4/9, D11):\n" + "\n".join(v)


def test_reference_is_not_executable_platform_code():
    v = cb.check_reference_not_executable()
    assert v == [], "\n".join(v)


def test_boundary_checker_cli_exits_clean():
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "check_boundaries.py")],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
