"""
Step 2: Memory Agent consuming a Verdict.

Pure and deterministic — no LLM anywhere. Real in-memory store, real
normalization, real forgetting model. We test the wiring and the one
remaining guard (unknown concept).
"""
import pytest
from phase2_memory.verdict import Verdict
from phase2_memory.memory_agent import MemoryAgent
from phase2_memory.knowledge_state import KnowledgeState, INITIAL_MASTERY


@pytest.fixture
def agent():
    store = KnowledgeState(db_path=":memory:")
    a = MemoryAgent(store=store)
    yield a
    store.close()


# ── Happy paths ──────────────────────────────────────────────────────────────

def test_correct_verdict_raises_mastery(agent):
    """A correct verdict updates the store and raises mastery."""
    v = Verdict(concept="fraction addition", correct=True)
    rec = agent.update_from_verdict(v)

    assert rec["concept"] == "fraction addition"
    assert rec["correct"] is True
    assert rec["mastery"] > INITIAL_MASTERY
    assert rec["flagged"] is False
    for k in ("concept", "correct", "mastery", "recall", "basis", "misconception", "flagged"):
        assert k in rec


def test_incorrect_verdict_lowers_mastery_and_counts_mistake(agent):
    """An incorrect verdict lowers mastery, increments mistake_count, and
    carries the misconception through to the enriched record."""
    v = Verdict(
        concept="fraction addition", correct=False,
        mistake_type="added_denominators",
        misconception="added numerators and denominators",
    )
    rec = agent.update_from_verdict(v)

    assert rec["correct"] is False
    assert rec["mastery"] < INITIAL_MASTERY
    assert agent.store.get("fraction addition")["mistake_count"] == 1
    assert rec["misconception"] == "added numerators and denominators"


# ── Normalization wired end-to-end (the deferred split-key bug) ──────────────

def test_noncanonical_concept_updates_single_row(agent):
    """A Verdict with a non-canonical concept string must map to ONE store row."""
    agent.update_from_verdict(Verdict(concept="Fractions Addition", correct=True))
    agent.update_from_verdict(Verdict(concept="fraction addition", correct=True))

    rows = agent.store.get_all()
    assert len(rows) == 1
    assert rows[0]["review_count"] == 2


# ── The one remaining guard: unknown concept ─────────────────────────────────

def test_unknown_concept_is_flagged_and_skips_store(agent):
    """An off-curriculum concept must flag and write NO row."""
    v = Verdict(concept="the capital of France", correct=True)
    rec = agent.update_from_verdict(v)

    assert rec["flagged"] is True
    assert rec["concept"] == "unknown"
    assert agent.store.get_all() == []


# ── Verdict metadata propagation ─────────────────────────────────────────────

def test_verdict_source_and_confidence_available_in_record(agent):
    """source and confidence should ride through to the record for tracing
    and future Planner weighting — even though the store doesn't use them."""
    v = Verdict(concept="fraction addition", correct=False,
                mistake_type="x", misconception="y",
                confidence=0.8, source="reasoning_agent")
    rec = agent.update_from_verdict(v)

    assert rec["confidence"] == 0.8
    assert rec["source"] == "reasoning_agent"