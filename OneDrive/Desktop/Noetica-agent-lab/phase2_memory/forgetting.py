"""
Forgetting model: time-decayed recall probability.

Pure functions only. No database, no LLM, no files, no clock surprises.
Give it a concept's mastery and when it was last reviewed; it tells you how
much the student remembers RIGHT NOW.

Two words that sound similar but mean different things:
  mastery = how well the fact was LEARNED   (a big or small bucket)
  recall  = how well it's REMEMBERED now    (water left in the bucket)

mastery only changes when the student is tested (the update rule in
KnowledgeState). recall changes every second as time passes — so we never
store it, we compute it fresh whenever someone asks.

NOTE: the constants below are PLACEHOLDERS. They make the curve the right
SHAPE, but whether 10 days is the real half-life of a mastered concept is
unknown until Noetica sees real students. Do not treat them as validated.
"""
import math
from datetime import datetime, timezone

# A fully-mastered concept (mastery = 1.0) is half-forgotten after this many days.
HALF_LIFE_SCALE = 10.0   # days

# The smallest possible half-life. Stops us dividing by almost-zero when
# mastery is tiny (a barely-learned fact still takes SOME time to forget).
MIN_HALF_LIFE = 0.5      # days


def half_life_days(mastery: float) -> float:
    """How many days until half the memory is gone, for a given mastery.

    Bigger bucket (higher mastery) = longer half-life = forgets slower.
    The max(...) makes sure we never go below the floor, even at mastery 0.
    """
    return max(MIN_HALF_LIFE, HALF_LIFE_SCALE * mastery)


def recall_probability(mastery: float, days_elapsed: float) -> float:
    """How much is remembered now, as a number from 0.0 to 1.0.

    The formula: recall = exp( -ln(2) * days / half_life )

    Why this exact formula? Because of one magic property:
    when days_elapsed equals the half_life, the answer is EXACTLY 0.5.
    That's what "half-life" means — half gone. The math guarantees it.

    Special case: if days_elapsed is 0 or negative (no time passed, or a
    clock glitch made time go backwards), nothing has leaked yet, so recall
    is a perfect 1.0. We never return more than 1.0.
    """
    if days_elapsed <= 0:
        return 1.0
    hl = half_life_days(mastery)
    return math.exp(-math.log(2) * days_elapsed / hl)


def _parse_iso(ts: str) -> datetime:
    """Turn a stored timestamp string back into a real date object.

    KnowledgeState saves times like '2026-01-01T10:00:00+00:00'.
    Some systems write 'Z' at the end to mean UTC; we swap it for '+00:00'
    so Python's parser is happy either way.
    """
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def recall_for_record(record: dict, now: datetime | None = None) -> float:
    """Compute recall directly from a KnowledgeState record (a dict).

    This is the function the Memory Agent will actually call. It pulls the
    two fields it needs out of the record and does the work.

    The tricky case: a concept that was created but NEVER reviewed has
    last_reviewed_at = None. There's no "start time" to measure leaking from.
    So we just return its mastery — an unreviewed fact's "remembered now"
    is simply how well it was first set, with no time to decay.

    'now' can be passed in so tests can pretend it's any date they want,
    instead of depending on the real clock (which would make tests flaky).
    """
    last = record.get("last_reviewed_at")
    mastery = record["mastery"]

    if last is None:
        return mastery   # never reviewed: no clock to decay from

    now = now or datetime.now(timezone.utc)
    days_elapsed = (now - _parse_iso(last)).total_seconds() / 86400.0  # seconds → days
    return recall_probability(mastery, days_elapsed)