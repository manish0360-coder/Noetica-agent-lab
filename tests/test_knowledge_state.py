"""
Deterministic tests for KnowledgeState.

Rules:
  - No LLM, no network, no randomness, no disk.
  - Every test uses db_path=":memory:" — a fresh SQLite database in RAM.
  - Tests are fully independent — order doesn't matter.
  - Every test asserts on the math, not just "it didn't crash."
"""
import pytest
from phase2_memory.knowledge_state import (
    KnowledgeState,
    INITIAL_MASTERY,
    LEARNING_RATE,
    DECAY_FACTOR,
)


@pytest.fixture
def ks():
    """A fresh in-memory KnowledgeState for each test.

    yield gives the store to the test; everything after yield runs on teardown.
    This pattern guarantees close() is always called, even if the test fails.
    """
    store = KnowledgeState(db_path=":memory:")
    yield store
    store.close()


# ── Existence and initialization ─────────────────────────────────────────────

def test_unseen_concept_returns_none(ks):
    """get() on a concept we've never touched must return None — not a default."""
    assert ks.get("fraction addition") is None


def test_get_or_init_creates_correct_defaults(ks):
    """First call to get_or_init must create a record with exact default values."""
    record = ks.get_or_init("fraction addition")

    assert record["concept"]          == "fraction addition"
    assert record["mastery"]          == INITIAL_MASTERY
    assert record["review_count"]     == 0
    assert record["mistake_count"]    == 0
    assert record["last_reviewed_at"] is None   # never reviewed yet
    assert record["created_at"]       is not None


def test_get_or_init_is_idempotent(ks):
    """Calling get_or_init twice must not create two rows or change created_at."""
    r1 = ks.get_or_init("fractions")
    r2 = ks.get_or_init("fractions")

    assert r1["created_at"] == r2["created_at"]
    assert len(ks.get_all()) == 1


# ── Mastery update math ───────────────────────────────────────────────────────

def test_correct_answer_increases_mastery(ks):
    """A correct answer must increase mastery by exactly the defined formula."""
    record = ks.update("fractions", correct=True)
    expected = round(INITIAL_MASTERY + LEARNING_RATE * (1.0 - INITIAL_MASTERY), 6)

    assert record["mastery"] == expected
    assert record["mastery"] >  INITIAL_MASTERY


def test_incorrect_answer_decreases_mastery(ks):
    """An incorrect answer must decrease mastery by exactly the defined formula."""
    record = ks.update("fractions", correct=False)
    expected = round(INITIAL_MASTERY * DECAY_FACTOR, 6)

    assert record["mastery"] == expected
    assert record["mastery"] <  INITIAL_MASTERY


def test_mastery_never_exceeds_one(ks):
    """Mastery must never exceed 1.0, no matter how many correct answers."""
    for _ in range(30):
        ks.update("fractions", correct=True)

    record = ks.get("fractions")
    assert record["mastery"] <= 1.0
    assert record["mastery"] >  0.95   # should be near-mastered after 30 correct


def test_mastery_never_goes_below_zero(ks):
    """Mastery must never go below 0.0, no matter how many incorrect answers."""
    for _ in range(30):
        ks.update("fractions", correct=False)

    record = ks.get("fractions")
    assert record["mastery"] >= 0.0


def test_mastery_growth_is_asymptotic(ks):
    """Each correct answer adds less than the previous — growth slows near 1.0."""
    ks.get_or_init("fractions")

    gains = []
    for _ in range(5):
        before = ks.get("fractions")["mastery"]
        ks.update("fractions", correct=True)
        after = ks.get("fractions")["mastery"]
        gains.append(after - before)

    # Each gain should be smaller than the previous (asymptotic growth).
    for i in range(1, len(gains)):
        assert gains[i] < gains[i - 1], f"gain {i} ({gains[i]}) >= gain {i-1} ({gains[i-1]})"


# ── Counter correctness ───────────────────────────────────────────────────────

def test_review_count_increments_on_every_answer(ks):
    """review_count must increment for BOTH correct and incorrect answers."""
    ks.update("fractions", correct=True)
    ks.update("fractions", correct=False)
    ks.update("fractions", correct=True)

    assert ks.get("fractions")["review_count"] == 3


def test_mistake_count_increments_only_on_incorrect(ks):
    """mistake_count must only increment on incorrect answers."""
    ks.update("fractions", correct=True)   # no mistake
    ks.update("fractions", correct=False)  # mistake
    ks.update("fractions", correct=False)  # mistake

    record = ks.get("fractions")
    assert record["mistake_count"] == 2
    assert record["review_count"]  == 3   # both are reviews


def test_last_reviewed_at_is_none_before_first_update(ks):
    """last_reviewed_at must be None until the first update."""
    ks.get_or_init("fractions")
    assert ks.get("fractions")["last_reviewed_at"] is None


def test_last_reviewed_at_is_set_after_update(ks):
    """last_reviewed_at must be set after the first update."""
    ks.update("fractions", correct=True)
    assert ks.get("fractions")["last_reviewed_at"] is not None


# ── Multi-concept isolation ───────────────────────────────────────────────────

def test_concepts_are_independent(ks):
    """Updating one concept must not affect any other concept."""
    ks.update("fractions", correct=True)
    ks.update("decimals",  correct=False)

    fractions = ks.get("fractions")
    decimals  = ks.get("decimals")

    assert fractions["mastery"] > INITIAL_MASTERY
    assert decimals["mastery"]  < INITIAL_MASTERY


def test_get_all_orders_by_mastery_ascending(ks):
    """get_all must return weakest concepts first — those needing most attention."""
    # Build a strong concept
    for _ in range(8):
        ks.update("easy topic", correct=True)

    # Build a weak concept
    ks.get_or_init("hard topic")

    records = ks.get_all()
    assert records[0]["concept"] == "hard topic"   # weakest first
    assert records[-1]["concept"] == "easy topic"  # strongest last


# ── Utility operations ────────────────────────────────────────────────────────

def test_reset_removes_concept_completely(ks):
    """reset must delete the row so get returns None afterward."""
    ks.update("fractions", correct=True)
    assert ks.get("fractions") is not None   # exists before reset

    ks.reset("fractions")
    assert ks.get("fractions") is None       # gone after reset


def test_update_returns_record_immediately(ks):
    """update must return the updated record so callers avoid a second read."""
    record = ks.update("fractions", correct=True)

    # Returned record must match what's in the database
    stored = ks.get("fractions")
    assert record["mastery"]       == stored["mastery"]
    assert record["review_count"]  == stored["review_count"]