"""
Tests for the Verdict dataclass — the typed contract between the Reasoning
Agent (produces it) and the Memory Agent (consumes it).

Pure data. No LLM, no store, no I/O. Fully deterministic.
"""
import pytest
from phase2_memory.verdict import Verdict


# ── Construction & defaults ──────────────────────────────────────────────────

def test_minimal_construction_requires_only_concept_and_correct():
    """A Verdict must be constructable with just the two fields Memory needs."""
    v = Verdict(concept="fraction addition", correct=True)
    assert v.concept == "fraction addition"
    assert v.correct is True


def test_defaults_are_set_for_unproduced_fields():
    """Fields the Reasoning Agent will later fill must have safe defaults now."""
    v = Verdict(concept="fraction addition", correct=True)
    assert v.mistake_type  == ""
    assert v.misconception == ""
    assert v.confidence    == 1.0
    assert v.source        == "manual"


def test_incorrect_verdict_can_carry_mistake_details():
    """A wrong answer may carry a mistake_type and misconception."""
    v = Verdict(
        concept="fraction addition",
        correct=False,
        mistake_type="added_denominators",
        misconception="added numerators and denominators directly",
        confidence=0.9,
        source="reasoning_agent",
    )
    assert v.correct is False
    assert v.mistake_type  == "added_denominators"
    assert v.misconception == "added numerators and denominators directly"
    assert v.confidence    == 0.9
    assert v.source        == "reasoning_agent"


# ── Validation: internal consistency ─────────────────────────────────────────

def test_correct_verdict_with_mistake_type_raises():
    """A correct answer carrying a mistake_type is contradictory → reject it."""
    with pytest.raises(ValueError):
        Verdict(concept="fraction addition", correct=True, mistake_type="added_denominators")


def test_correct_verdict_with_misconception_raises():
    """A correct answer carrying a misconception is contradictory → reject it."""
    with pytest.raises(ValueError):
        Verdict(concept="fraction addition", correct=True, misconception="some error")


def test_confidence_out_of_range_raises():
    """Confidence must be a probability in [0.0, 1.0]."""
    with pytest.raises(ValueError):
        Verdict(concept="fraction addition", correct=True, confidence=1.5)
    with pytest.raises(ValueError):
        Verdict(concept="fraction addition", correct=True, confidence=-0.1)


def test_empty_concept_raises():
    """A verdict with no concept is meaningless — reject it."""
    with pytest.raises(ValueError):
        Verdict(concept="", correct=True)


# ── Type integrity ────────────────────────────────────────────────────────────

def test_correct_must_be_bool():
    """correct must be a real bool, not a truthy string or int.

    This guards the exact bug from Day 2: a string 'false' is truthy and would
    silently corrupt the store's update rule.
    """
    with pytest.raises((ValueError, TypeError)):
        Verdict(concept="fraction addition", correct="false")