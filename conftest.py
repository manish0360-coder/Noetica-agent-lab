"""Pytest bootstrap: put the platform package root (src/) on sys.path so tests import
`noetica` without installation or env vars. Test configuration only — not platform code.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent / "src"))
