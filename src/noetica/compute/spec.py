"""Vendor-neutral compute work spec and lifecycle status.

Purpose: describe a unit of compute work independent of any vendor, and the lifecycle
    states the broker tracks. Infrastructure (cloud/K8s/GPU/edge) is external to the four
    layers (§6.21); this is only the abstract description.
Owner: Noetica (Layer 2).
Consumer: ComputeBroker; domain execution adapters; Velith; Mini Prometheus.
Constitution: §6.21 (Amendment 3, Infrastructure Ownership); Law 21 (schema_version).
Future implementation owner: Noetica (spec); domains (concrete adapters).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

SCHEMA_VERSION = "0.1.0"


class WorkStatus(str, Enum):
    """Lifecycle states the broker controls (execution completion is adapter/external)."""

    SCHEDULED = "SCHEDULED"
    PLACED = "PLACED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class ComputeSpec:
    """A vendor-neutral description of compute work + its estimated cost."""

    kind: str
    estimated_cost: float
    payload: Mapping[str, Any] = field(default_factory=dict)
    schema_version: str = SCHEMA_VERSION
