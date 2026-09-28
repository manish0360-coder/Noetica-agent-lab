"""Release gate (DN-9): the ``noetica`` wheel is a real, self-contained, installable package.

Builds the wheel from this repository, audits its contents and metadata, installs it into a fresh
virtual environment (no system site-packages) and, from a neutral working directory with no
``PYTHONPATH`` and no repository path on ``sys.path``:

- imports ``noetica``, every public subsystem package and every module below them;
- proves they were imported from the installed wheel (not the source tree), that the installed
  version equals ``noetica.__version__`` and the source version, and that nothing from MiniFlyWire,
  Velith, Mini Prometheus, ``reference/`` or the MiniNoetica legacy was imported or needed;
- runs the platform behaviour tests (``tests/noetica``) against the installed wheel, outside the
  repository, so the test bootstrap's ``src/`` path insertion plays no part.

Standard library only. Run from any directory: ``python tools/verify_installed_wheel.py``.
Needs network access for the isolated build backend and for pytest. Exit 0 = every check passed.
"""

from __future__ import annotations

import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import venv
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "noetica"
# The public surface: the interface package plus the 21 Constitution Part VI subsystems.
PUBLIC_PACKAGES = (
    "interfaces", "state", "provenance", "episodes", "observability", "budget", "datacontracts",
    "verification", "guardrails", "router", "compute", "tools", "knowledge", "memory", "skills",
    "context", "evaluation", "reasoning", "planning", "reflection", "runtime", "sdk",
)
# Never a dependency of the platform (Handbook Laws 4 and 9; DN-2/DN-4; D11).
FORBIDDEN_TOP = {
    "miniflywire", "velith", "mini_prometheus", "reference", "core", "phase2_memory", "agent_zero",
}
# Machine-specific paths and credential material that must never ship in the wheel.
LEAK_PATTERNS = [
    re.compile(p)
    for p in (
        r"[A-Za-z]:\\(?:Users|Projects)\\",
        r"/home/[a-z]",
        r"/Users/[A-Za-z]",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"\bgh[pousr]_[A-Za-z0-9]{20,}",
        r"\bAKIA[0-9A-Z]{16}\b",
    )
]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
failures: list[str] = []


def check(ok: bool, label: str) -> None:
    print(("PASS  " if ok else "FAIL  ") + label)
    if not ok:
        failures.append(label)


def run(
    cmd: list[str], cwd: Path | None = None, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, check=False, cwd=cwd, env=env)


def source_version() -> str | None:
    text = (ROOT / "src" / PACKAGE / "__init__.py").read_text(encoding="utf-8")
    match = re.search(r'^__version__ = "([^"]*)"$', text, re.MULTILINE)
    return match.group(1) if match else None


def top_level_imports(source: str) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module.split(".")[0])
    return names


def audit_wheel(wheel: Path, version: str | None) -> None:
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        dist_info = f"{PACKAGE}-{version}.dist-info/"
        check(
            all(n.startswith((f"{PACKAGE}/", dist_info)) for n in names),
            "the wheel contains only the noetica package and its dist-info",
        )
        # Repository-level directories must never ship (noetica/tools/ is the Tool Runtime subsystem
        # and is public; only a top-level tools/ would be the repository's enforcement scripts).
        repo_dirs = {"tests", "tools", "docs", "reference", "examples", "configs", "plugins"}
        check(
            not any(n.split("/")[0] in repo_dirs for n in names)
            and not any(part in ("__pycache__", ".git") for n in names for part in n.split("/"))
            and not any(n.endswith((".pyc", ".pyo")) for n in names),
            "no tests, tools, docs, reference, cache or source-control files are packaged",
        )
        check(f"{PACKAGE}/py.typed" in names, "the PEP 561 py.typed marker is packaged")
        check(
            all(f"{PACKAGE}/{p}/__init__.py" in names for p in PUBLIC_PACKAGES),
            f"all {len(PUBLIC_PACKAGES)} public subsystem packages are packaged",
        )
        metadata = archive.read(f"{dist_info}METADATA").decode("utf-8")
        fields = dict(
            line.split(": ", 1) for line in metadata.splitlines() if ": " in line and not line[0].isspace()
        )
        check(
            fields.get("Name") == PACKAGE and fields.get("Version") == version,
            f"metadata names noetica {version}",
        )
        check("Requires-Python" in fields, f"metadata declares Requires-Python ({fields.get('Requires-Python')})")
        check("Requires-Dist" not in metadata, "metadata declares no runtime dependency")
        imported: set[str] = set()
        leaks: list[str] = []
        for name in names:
            if name.endswith("/"):
                continue
            text = archive.read(name).decode("utf-8", errors="replace")
            leaks += [f"{name}: {p.pattern}" for p in LEAK_PATTERNS if p.search(text)]
            if name.endswith(".py"):
                imported |= top_level_imports(text)
        check(not leaks, "no machine-specific path or credential material is packaged" + (f" {leaks}" if leaks else ""))
        foreign = sorted(imported - set(sys.stdlib_module_names) - {PACKAGE, "__future__"})
        check(not foreign, "every packaged module imports only noetica and the standard library" + (f" {foreign}" if foreign else ""))
        check(not (imported & FORBIDDEN_TOP), "no packaged module imports MiniFlyWire, Velith, Mini Prometheus, reference/ or legacy code")


PROBE = r"""
import importlib, importlib.metadata, importlib.util, json, pkgutil, sys
import noetica
public = sys.argv[1].split(",")
loaded, errors = [], []
for name in public:
    importlib.import_module(f"noetica.{name}")
for info in pkgutil.walk_packages(noetica.__path__, "noetica."):
    try:
        importlib.import_module(info.name)
        loaded.append(info.name)
    except Exception as exc:
        errors.append(f"{info.name}: {exc!r}")
print(json.dumps({
    "file": noetica.__file__,
    "version": noetica.__version__,
    "metadata_version": importlib.metadata.version("noetica"),
    "modules": sorted(loaded),
    "errors": errors,
    "sys_path": sys.path,
    "top_level_loaded": sorted({m.split(".")[0] for m in sys.modules}),
    "findable": {m: importlib.util.find_spec(m) is not None for m in sys.argv[2].split(",")},
}))
"""


def main() -> int:
    version = source_version()
    check(version is not None and bool(SEMVER.match(version)), f"source version is a release version ({version})")
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name)
        build = run([sys.executable, "-m", "pip", "wheel", str(ROOT), "--no-deps", "-q", "-w", str(tmp / "dist")])
        wheels = sorted((tmp / "dist").glob(f"{PACKAGE}-*.whl"))
        check(build.returncode == 0 and len(wheels) == 1, "the wheel builds")
        if failures:
            print(build.stdout[-2000:], build.stderr[-2000:])
            return 1
        wheel = wheels[0]
        print(f"      wheel: {wheel.name}")
        check(wheel.name == f"{PACKAGE}-{version}-py3-none-any.whl", "the wheel is a pure-Python py3-none-any wheel of this version")
        audit_wheel(wheel, version)

        env_dir = tmp / "venv"
        venv.create(env_dir, with_pip=True, system_site_packages=False)
        python = str(env_dir / ("Scripts" if os.name == "nt" else "bin") / "python")
        install = run([python, "-m", "pip", "install", "-q", "--no-index", "--no-deps", str(wheel)])
        check(install.returncode == 0, "the wheel installs into a clean virtual environment (no index, no dependencies)")

        neutral = tmp / "neutral"
        neutral.mkdir()
        env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "PYTHONHOME")}
        (tmp / "probe.py").write_text(PROBE, encoding="utf-8")
        probe = run(
            [python, str(tmp / "probe.py"), ",".join(PUBLIC_PACKAGES), ",".join(sorted(FORBIDDEN_TOP))],
            cwd=neutral,
            env=env,
        )
        check(probe.returncode == 0, "noetica and every public subsystem import from the installed wheel")
        if probe.returncode != 0:
            print(probe.stderr[-3000:])
            return 1
        found = json.loads(probe.stdout.strip().splitlines()[-1])
        site = str(env_dir.resolve())
        root = str(ROOT)
        check(str(Path(found["file"]).resolve()).startswith(site), "noetica is imported from the virtual environment, not the source tree")
        check(not any(p and str(Path(p).resolve()).startswith(root) for p in found["sys_path"]), "no repository path is on sys.path")
        check(not found["errors"], f"every module below noetica imports ({len(found['modules'])} modules)" + (f" {found['errors']}" if found["errors"] else ""))
        check(found["version"] == found["metadata_version"] == version, f"installed version, noetica.__version__ and source agree ({found['metadata_version']})")
        check(not (set(found["top_level_loaded"]) & FORBIDDEN_TOP), "importing the whole platform loads nothing forbidden")
        check(not any(found["findable"].values()), "the clean environment has no MiniFlyWire, Velith, Mini Prometheus or reference package: none is needed")

        tests = tmp / "installed-tests"
        shutil.copytree(ROOT / "tests" / "noetica", tests / "noetica", ignore=shutil.ignore_patterns("__pycache__"))
        pytest_install = run([python, "-m", "pip", "install", "-q", "pytest"])
        suite = run(
            [python, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--rootdir", str(tests), str(tests / "noetica")],
            cwd=tests,
            env=env,
        )
        summary = (suite.stdout.strip().splitlines() or [""])[-1]
        check(
            pytest_install.returncode == 0 and suite.returncode == 0,
            f"the platform behaviour tests pass against the installed wheel ({summary})",
        )
        check(list(neutral.iterdir()) == [], "nothing is written to the working directory")

    print(f"{len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
