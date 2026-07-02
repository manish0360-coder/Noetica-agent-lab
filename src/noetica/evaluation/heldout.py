"""Held-out dataset + lock (§5.6, D8, §11.10).

Purpose: the immutable held-out benchmark and the mechanical lock that keeps held-out data
    out of any arm's memory. Held-out data can never enter memory; enforced in code, not by
    discipline.
Owner: Noetica (Layer 2).
Consumer: EvaluationHarness; Velith configures the held-out set.
Constitution: §5.6 (mechanically-enforced held-out lock); D8; §11.10.
Future implementation owner: Noetica.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator


class HeldoutViolation(RuntimeError):
    """Raised when held-out data leaks into an arm's memory."""


@dataclass(frozen=True)
class HeldoutDataset:
    """An immutable set of held-out task ids. Frozen — mechanically protected from
    modification during evaluation."""

    tasks: tuple[str, ...] = ()
    ids: frozenset[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        # Derive the id set from tasks (immutable, deduplicated).
        object.__setattr__(self, "ids", frozenset(self.tasks))

    def __contains__(self, task_id: object) -> bool:
        return task_id in self.ids

    def __iter__(self) -> Iterator[str]:
        return iter(self.tasks)

    def __len__(self) -> int:
        return len(self.tasks)
