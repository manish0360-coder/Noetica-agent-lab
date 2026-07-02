"""Noetica · datacontracts — Data Contract & Versioning (§4.3, Law 21).

The framework governing the Experience Flow's schemas: every payload carries a
`schema_version`; a schema change requires a new version and a registered forward
migration path; consumers read against a declared version. PE-7 provides `Version` and
`DataContractRegistry`. Domain-agnostic; no concrete domain schemas.
"""
from __future__ import annotations

from noetica.datacontracts.registry import (
    DataContractError,
    DataContractRegistry,
    Migration,
    MigrationError,
    UnknownContractError,
    UnknownVersionError,
    is_data_contract,
)
from noetica.datacontracts.version import Version

__all__ = [
    "DataContractRegistry",
    "Version",
    "Migration",
    "is_data_contract",
    "DataContractError",
    "UnknownContractError",
    "UnknownVersionError",
    "MigrationError",
]
