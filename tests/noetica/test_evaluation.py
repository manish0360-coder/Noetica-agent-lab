"""PE-17 unit tests — Evaluation Harness & Held-out Lock (§6.10).

Platform tests use ONLY the ReferenceVerifier (Law 20).
"""
from __future__ import annotations

import dataclasses

import pytest

from noetica.evaluation import (
    Arm,
    EvaluationHarness,
    FrozenEvaluationViolation,
    HeldoutDataset,
    HeldoutViolation,
)
from noetica.interfaces.episode import Episode
from noetica.interfaces.evaluation import EvalHarness
from noetica.interfaces.provenance import Provenance
from noetica.interfaces.verification import Verdict, VerdictStatus
from noetica.memory import InMemoryMemoryStore, UnfilteredWriteFilter
from noetica.state import InMemoryStateSubstrate
from noetica.verification import ReferenceVerifier


def _heldout() -> HeldoutDataset:
    return HeldoutDataset(tasks=("t0", "t1", "t2", "t3"))


def test_harness_satisfies_interface() -> None:
    h = EvaluationHarness(ReferenceVerifier(), _heldout())
    assert isinstance(h, EvalHarness)


def test_frozen_run_measures_pass_rate() -> None:
    verifier = ReferenceVerifier(
        default=Verdict(status=VerdictStatus.PASSED),
        script={"t1": Verdict(status=VerdictStatus.FAILED),
                "t3": Verdict(status=VerdictStatus.FAILED)},
    )
    h = EvaluationHarness(verifier, _heldout())
    h.register_arm("A2", Arm(name="A2", solver=lambda task: "candidate"))
    result = h.run()
    assert result.metrics["A2.pass_rate"] == 0.5      # 2 of 4 PASSED
    assert result.metrics["A2.n"] == 4.0


def test_held_out_dataset_is_immutable() -> None:
    ds = _heldout()
    with pytest.raises(dataclasses.FrozenInstanceError):
        ds.tasks = ()  # type: ignore[misc]
    assert "t0" in ds and len(ds) == 4


def test_provenance_recorded_for_each_eval() -> None:
    h = EvaluationHarness(ReferenceVerifier(), _heldout())
    h.register_arm("A", Arm(name="A", solver=lambda task: "c"))
    h.run()
    eps = h.episodes()
    assert len(eps) == 4
    assert all(e.provenance is not None and e.provenance.source == "eval" for e in eps)
    assert eps[0].provenance.transform == "arm:A"


def test_held_out_lock_blocks_leak_into_memory() -> None:
    mem = InMemoryMemoryStore(UnfilteredWriteFilter())

    def cheating_solver(task: str) -> str:
        # A misbehaving arm tries to write the held-out task into its memory.
        mem.write(Episode(task_id=task, verdict=Verdict(status=VerdictStatus.PASSED),
                          provenance=Provenance(source="cheat", transform="leak")))
        return "c"

    h = EvaluationHarness(ReferenceVerifier(), _heldout())
    h.register_arm("cheat", Arm(name="cheat", solver=cheating_solver, memory=mem))
    with pytest.raises(HeldoutViolation):
        h.run()


def test_frozen_violation_on_state_write() -> None:
    state = InMemoryStateSubstrate()

    def state_writing_solver(task: str) -> str:
        state.put("leak", task, Provenance(source="cheat", transform="write"))
        return "c"

    h = EvaluationHarness(ReferenceVerifier(), _heldout())
    h.register_arm("s", Arm(name="s", solver=state_writing_solver, state=state))
    with pytest.raises(FrozenEvaluationViolation):
        h.run()


def test_well_behaved_arm_leaves_mechanisms_unchanged() -> None:
    mem = InMemoryMemoryStore(UnfilteredWriteFilter())
    mem.write(Episode(task_id="train", verdict=Verdict(status=VerdictStatus.PASSED),
                     provenance=Provenance(source="s", transform="t")))
    state = InMemoryStateSubstrate()
    state.put("seed", 1, Provenance(source="s", transform="t"))
    before_mem, before_rev = len(mem), state.revision

    h = EvaluationHarness(ReferenceVerifier(), _heldout())
    h.register_arm("A", Arm(name="A", solver=lambda task: "c", memory=mem, state=state))
    h.run()
    assert len(mem) == before_mem and state.revision == before_rev   # never improved/mutated


def test_duplicate_arm_and_bad_config() -> None:
    h = EvaluationHarness(ReferenceVerifier(), _heldout())
    h.register_arm("A", Arm(name="A", solver=lambda t: "c"))
    with pytest.raises(Exception):
        h.register_arm("A", Arm(name="A", solver=lambda t: "c"))
    with pytest.raises(TypeError):
        h.register_arm("B", "not-an-arm")
