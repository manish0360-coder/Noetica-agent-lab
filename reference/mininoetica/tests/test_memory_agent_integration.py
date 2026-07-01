"""
Memory Agent integration tests (Step 3).

Extraction is mocked (deterministic). The store is real but in-memory.
Normalization and forgetting are real (already banked). We test the WIRING
and the two guard decisions: correct=None and concept=unknown.
"""
import pytest

pytestmark = pytest.mark.skip(
    reason="analyze() superseded by update_from_verdict (Verdict migration, Option D). "
           "Retained for historical reference; remove when extraction helpers are deleted in Step 4."
)
import phase2_memory.memory_agent as ma
from phase2_memory.memory_agent import MemoryAgent
from phase2_memory.knowledge_state import KnowledgeState, INITIAL_MASTERY


def _mock_extraction(raw_concept, correct, misconception=""):
    """Patch extract_answer_analysis to return a fixed result (no LLM)."""
    def _fake(question, student_answer):
        return {"raw_concept": raw_concept, "correct": correct, "misconception": misconception}
    return _fake


@pytest.fixture
def agent():
    """A MemoryAgent backed by a fresh in-memory store per test."""
    store = KnowledgeState(db_path=":memory:")
    a = MemoryAgent(store=store)
    yield a
    store.close()


# ── Happy paths: correct vs incorrect ────────────────────────────────────────

def test_correct_answer_raises_mastery(agent, monkeypatch):
    monkeypatch.setattr(ma, "extract_answer_analysis",
                        _mock_extraction("fraction addition", True))
    rec = agent.analyze("q", "a")

    assert rec["concept"] == "fraction addition"
    assert rec["correct"] is True
    assert rec["mastery"] > INITIAL_MASTERY
    assert rec["flagged"] is False
    # all enriched fields present
    for k in ("concept", "correct", "mastery", "recall", "basis", "misconception", "flagged"):
        assert k in rec


def test_incorrect_answer_lowers_mastery_and_counts_mistake(agent, monkeypatch):
    monkeypatch.setattr(ma, "extract_answer_analysis",
                        _mock_extraction("fraction addition", False, "added denominators"))
    rec = agent.analyze("q", "a")

    assert rec["correct"] is False
    assert rec["mastery"] < INITIAL_MASTERY
    assert agent.store.get("fraction addition")["mistake_count"] == 1
    assert rec["misconception"] == "added denominators"


# ── Normalization wired end-to-end (the deferred bug, proven in pipeline) ─────

def test_noncanonical_concept_updates_single_row(agent, monkeypatch):
    """LLM says 'Fractions Addition' then 'fraction addition' → ONE store row."""
    monkeypatch.setattr(ma, "extract_answer_analysis",
                        _mock_extraction("Fractions Addition", True))
    agent.analyze("q", "a")

    monkeypatch.setattr(ma, "extract_answer_analysis",
                        _mock_extraction("fraction addition", True))
    agent.analyze("q", "a")

    assert len(agent.store.get_all()) == 1            # not split into two rows
    assert agent.store.get_all()[0]["review_count"] == 2


# ── Guard 1: correct is None must NOT touch the store ────────────────────────

def test_none_correctness_is_flagged_and_skips_store(agent, monkeypatch):
    monkeypatch.setattr(ma, "extract_answer_analysis",
                        _mock_extraction("fraction addition", None))
    rec = agent.analyze("q", "a")

    assert rec["flagged"] is True
    assert agent.store.get("fraction addition") is None   # nothing written


# ── Guard 2: unknown concept must NOT write a junk row ───────────────────────

def test_unknown_concept_is_flagged_and_skips_store(agent, monkeypatch):
    monkeypatch.setattr(ma, "extract_answer_analysis",
                        _mock_extraction("the capital of France", True))
    rec = agent.analyze("q", "a")

    assert rec["flagged"] is True
    assert rec["concept"] == "unknown"
    assert agent.store.get_all() == []                    # no junk row