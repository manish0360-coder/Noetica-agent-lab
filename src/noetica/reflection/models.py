"""Reflection value type (self-critique output; form only)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

SCHEMA_VERSION = "0.1.0"


@dataclass(frozen=True)
class Revision:
    """The proposed revision from self-critique: whether to revise, the attempt inspected,
    and grounded feedback."""

    revise: bool
    attempt: Any
    feedback: str
    schema_version: str = SCHEMA_VERSION
