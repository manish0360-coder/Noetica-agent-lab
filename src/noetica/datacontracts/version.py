"""Semantic version value type for data contracts.

Purpose: a comparable major.minor.patch version so schema evolution is ordered and
    forward-only migrations can be reasoned about.
Owner: Noetica (Layer 2).
Consumer: the DataContractRegistry; Episode/Memory schema evolution; Experience Flow.
Constitution: §4.3; Law 21; §11.7.
Future implementation owner: Noetica.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Version:
    """Semantic version (major, minor, patch). Ordered for forward-migration reasoning."""

    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, s: str) -> "Version":
        parts = s.split(".")
        if len(parts) != 3:
            raise ValueError(f"invalid semantic version: {s!r} (expected major.minor.patch)")
        try:
            nums = [int(p) for p in parts]
        except ValueError as e:
            raise ValueError(f"invalid semantic version: {s!r}") from e
        if any(n < 0 for n in nums):
            raise ValueError(f"version components must be non-negative: {s!r}")
        return cls(nums[0], nums[1], nums[2])

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
