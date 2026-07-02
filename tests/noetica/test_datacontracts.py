"""PE-7 unit tests — Data Contract & Versioning (§4.3, Law 21).

Platform tests: no domain oracle, no real verifier (Law 20). Pure framework.
"""
from __future__ import annotations

import pytest

from noetica.interfaces.datacontract import DataContract
from noetica.datacontracts import (
    DataContractError,
    DataContractRegistry,
    MigrationError,
    UnknownVersionError,
    Version,
    is_data_contract,
)


def test_version_parse_compare_str() -> None:
    assert Version.parse("1.2.3") == Version(1, 2, 3)
    assert Version.parse("0.1.0") < Version.parse("0.2.0") < Version.parse("1.0.0")
    assert str(Version(0, 2, 1)) == "0.2.1"
    for bad in ("1.2", "a.b.c", "1.2.-1"):
        with pytest.raises(ValueError):
            Version.parse(bad)


def test_single_step_migration_applies_and_stamps_version() -> None:
    reg = DataContractRegistry()
    reg.register_migration("episode", "0.1.0", "0.2.0",
                           lambda p: {**p, "environment": p.get("environment", {})})
    out = reg.migrate("episode", {"schema_version": "0.1.0", "task_id": "t"}, "0.2.0")
    assert out["schema_version"] == "0.2.0" and out["task_id"] == "t"


def test_multi_step_chain() -> None:
    reg = DataContractRegistry()
    reg.register_migration("c", "0.1.0", "0.2.0", lambda p: {**p, "a": 1})
    reg.register_migration("c", "0.2.0", "0.3.0", lambda p: {**p, "b": 2})
    out = reg.migrate("c", {"schema_version": "0.1.0"}, "0.3.0")
    assert out == {"schema_version": "0.3.0", "a": 1, "b": 2}


def test_read_is_migrate_to_expected_version() -> None:
    reg = DataContractRegistry()
    reg.register_migration("c", "0.1.0", "0.2.0", lambda p: dict(p))
    assert reg.read("c", {"schema_version": "0.1.0"}, "0.2.0")["schema_version"] == "0.2.0"


def test_same_version_is_identity() -> None:
    reg = DataContractRegistry()
    reg.register_version("c", "1.0.0")
    assert reg.migrate("c", {"schema_version": "1.0.0", "x": 1}, "1.0.0") == {
        "schema_version": "1.0.0", "x": 1}


def test_missing_schema_version_rejected() -> None:
    reg = DataContractRegistry()
    reg.register_version("c", "0.1.0")
    with pytest.raises(DataContractError):
        reg.migrate("c", {"no_version": True}, "0.1.0")


def test_downgrade_rejected() -> None:
    reg = DataContractRegistry()
    reg.register_migration("c", "0.1.0", "0.2.0", lambda p: dict(p))
    with pytest.raises(MigrationError):
        reg.migrate("c", {"schema_version": "0.2.0"}, "0.1.0")


def test_unknown_version_rejected() -> None:
    reg = DataContractRegistry()
    reg.register_version("c", "0.1.0")
    with pytest.raises(UnknownVersionError):
        reg.migrate("c", {"schema_version": "0.1.0"}, "9.9.9")


def test_missing_migration_path_rejected() -> None:
    reg = DataContractRegistry()
    reg.register_version("c", "0.1.0")
    reg.register_version("c", "0.2.0")   # version exists but NO migration edge
    with pytest.raises(MigrationError):
        reg.migrate("c", {"schema_version": "0.1.0"}, "0.2.0")


def test_assert_migratable_law21_governance() -> None:
    reg = DataContractRegistry()
    reg.register_migration("ok", "0.1.0", "0.2.0", lambda p: dict(p))
    reg.assert_migratable("ok")          # complete chain -> passes
    reg.register_version("gap", "0.1.0")
    reg.register_version("gap", "0.2.0") # gap with no migration -> violation
    with pytest.raises(MigrationError):
        reg.assert_migratable("gap")


def test_is_data_contract_marker() -> None:
    class WithVersion:
        SCHEMA_VERSION = "0.1.0"
    assert is_data_contract(WithVersion()) is True
    assert is_data_contract({"schema_version": "0.1.0"}) is False   # dict key != attribute
    assert isinstance(WithVersion(), DataContract)                  # runtime_checkable marker
