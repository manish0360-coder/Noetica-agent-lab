"""
Deterministic tests for the forgetting model.

'Deterministic' = same result every single time. No randomness, and we never
use the real clock — we always inject a fake 'now' so the math is predictable.
"""
import math
from datetime import datetime, timezone, timedelta
import pytest
from phase2_memory.forgetting import (
    recall_probability, half_life_days, recall_for_record,
    HALF_LIFE_SCALE, MIN_HALF_LIFE,
)


def test_recall_is_one_at_zero_elapsed():
    """No time has passed, so the student remembers everything → 1.0."""
    assert recall_probability(0.5, 0) == 1.0


def test_recall_is_half_at_half_life():
    """The headline property: at the half-life, exactly half is remembered."""
    mastery = 0.5
    hl = half_life_days(mastery)
    assert recall_probability(mastery, hl) == pytest.approx(0.5)


def test_recall_decays_monotonically():
    """As more days pass, recall must always go DOWN, never up."""
    prev = 1.1
    for days in range(0, 30, 2):
        r = recall_probability(0.5, days)
        assert r < prev
        prev = r


def test_higher_mastery_decays_slower():
    """After the same time, a better-learned fact is remembered better."""
    days = 5
    low_mastery  = recall_probability(0.2, days)
    high_mastery = recall_probability(0.9, days)
    assert high_mastery > low_mastery


def test_half_life_floor_prevents_div_by_zero():
    """Even at mastery 0.0, the floor stops a crash from dividing by zero."""
    assert half_life_days(0.0) == MIN_HALF_LIFE
    r = recall_probability(0.0, 1.0)   # must not raise an error
    assert 0.0 <= r <= 1.0


def test_negative_elapsed_clamped_to_one():
    """A backwards clock can't give more than perfect recall → stays 1.0."""
    assert recall_probability(0.5, -3) == 1.0


def test_recall_never_exceeds_one_or_below_zero():
    """No matter the inputs, recall must always stay between 0.0 and 1.0."""
    for mastery in (0.0, 0.3, 0.7, 1.0):
        for days in (0, 1, 10, 100, 1000):
            r = recall_probability(mastery, days)
            assert 0.0 <= r <= 1.0


# ── record-level tests: works with KnowledgeState's dict shape ───────────────

def test_never_reviewed_record_returns_mastery():
    """A concept never reviewed has no decay clock → recall equals mastery."""
    record = {"mastery": 0.1, "last_reviewed_at": None}
    assert recall_for_record(record) == 0.1


def test_reviewed_record_decays_over_time():
    """A reviewed concept loses recall as our fake 'now' moves forward."""
    reviewed = datetime(2026, 1, 1, tzinfo=timezone.utc)
    record = {"mastery": 0.5, "last_reviewed_at": reviewed.isoformat()}

    same_day = recall_for_record(record, now=reviewed)
    five_days_later = recall_for_record(record, now=reviewed + timedelta(days=5))

    assert same_day == pytest.approx(1.0)
    assert five_days_later < same_day


def test_record_recall_matches_half_life_point():
    """At exactly the half-life, a real record reads ~0.5 — end-to-end check."""
    mastery = 0.6
    reviewed = datetime(2026, 1, 1, tzinfo=timezone.utc)
    hl = half_life_days(mastery)
    record = {"mastery": mastery, "last_reviewed_at": reviewed.isoformat()}

    at_half_life = recall_for_record(record, now=reviewed + timedelta(days=hl))
    assert at_half_life == pytest.approx(0.5, abs=0.01)

def test_naive_now_does_not_crash():
    from datetime import datetime
    reviewed = datetime(2026, 1, 1, tzinfo=timezone.utc)
    record = {"mastery": 0.5, "last_reviewed_at": reviewed.isoformat()}
    r = recall_for_record(record, now=datetime(2026, 1, 6))  # naive!
    assert 0.0 <= r <= 1.0

def test_recall_with_status_distinguishes_cases():
    from phase2_memory.forgetting import recall_with_status
    never = {"mastery": 0.1, "last_reviewed_at": None}
    reviewed = {"mastery": 0.5, "last_reviewed_at": "2026-01-01T00:00:00+00:00"}
    assert recall_with_status(never)["basis"] == "never_reviewed"
    assert recall_with_status(reviewed)["basis"] == "decayed"