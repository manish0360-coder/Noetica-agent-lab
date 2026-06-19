"""
KnowledgeState: persistent learner store.

The ground truth about what one student knows.
One row per concept. One database file per student.

Design constraints:
  - No LLM dependency. Pure SQLite + Python.
  - The Memory Agent calls update(concept, correct) — it does NOT set mastery directly.
  - Mastery is owned by this store and updated by deterministic rules.
  - The forgetting model reads mastery + last_reviewed_at but never writes here.
"""
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

# ── Constants ─────────────────────────────────────────────────────────────────

# Starting mastery for a concept the student has never been tested on.
# 0.1 means "we know nothing yet, assume very low" — not 0.0 which would imply
# the student definitely knows nothing.
INITIAL_MASTERY = 0.1

# Asymptotic growth rate on a correct answer.
# new = old + LEARNING_RATE * (1.0 - old)
# Grows fast when low, slows near 1.0. Mirrors real learning curves.
LEARNING_RATE = 0.2

# Proportional decay on an incorrect answer.
# new = old * DECAY_FACTOR
# A student at 0.6 drops to 0.36. At 0.9 drops to 0.54.
DECAY_FACTOR = 0.6


class KnowledgeState:
    """Persistent store for a single learner's concept mastery.

    Usage:
        ks = KnowledgeState("data/student_123.db")
        record = ks.update("fraction addition", correct=False)
        print(record["mastery"])   # updated mastery float
        ks.close()
    """

    def __init__(self, db_path: str = "data/noetica.db"):
        # ":memory:" is a valid SQLite path — creates a temporary in-memory DB.
        # Tests use this so they never touch disk and never interfere with each other.
        Path(db_path).parent.mkdir(parents=True, exist_ok=True) if db_path != ":memory:" else None
        self.conn = sqlite3.connect(db_path)

        # Row factory makes rows behave like dicts: row["mastery"] instead of row[1].
        # Without this, SQLite returns plain tuples — fragile if schema order changes.
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        """Create schema on first connection. Safe to call on existing databases."""
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS knowledge_state (
                concept           TEXT    PRIMARY KEY,
                mastery           REAL    NOT NULL DEFAULT 0.1,
                review_count      INTEGER NOT NULL DEFAULT 0,
                mistake_count     INTEGER NOT NULL DEFAULT 0,
                last_reviewed_at  TEXT,
                created_at        TEXT    NOT NULL
            );
        """)
        self.conn.commit()

    def _now(self) -> str:
        """UTC timestamp in ISO 8601 format. Always UTC — never local time.

        Why UTC: if a student reviews at 11pm in India and we store local time,
        then calculate "days since review" from a server in the US, the math is
        wrong. UTC is the only safe choice for time arithmetic.
        """
        return datetime.now(timezone.utc).isoformat()

    # ── Read operations ───────────────────────────────────────────────────────

    def get(self, concept: str) -> dict | None:
        """Return the current record for a concept.

        Returns None if the concept has never been seen.
        The Memory Agent checks for None to decide whether to initialize.
        """
        row = self.conn.execute(
            "SELECT * FROM knowledge_state WHERE concept = ?",
            (concept,)
        ).fetchone()
        return dict(row) if row else None

    def get_or_init(self, concept: str) -> dict:
        """Return record for concept, creating it with defaults if unseen.

        The Memory Agent calls this before every update — it needs a record
        to exist before it can compute the delta from the old mastery.
        Calling this twice on the same concept is safe (idempotent).
        """
        existing = self.get(concept)
        if existing:
            return existing

        now = self._now()
        self.conn.execute(
            """INSERT INTO knowledge_state
               (concept, mastery, review_count, mistake_count, last_reviewed_at, created_at)
               VALUES (?, ?, 0, 0, NULL, ?)""",
            (concept, INITIAL_MASTERY, now),
        )
        self.conn.commit()
        return self.get(concept)

    def get_all(self) -> list[dict]:
        """Return all concept records, ordered by mastery ascending.

        Lowest mastery first = concepts that need the most attention first.
        The Planner Agent uses this ordering to decide what to work on next.
        When mastery is equal, lowest review_count comes first — less practiced.
        """
        rows = self.conn.execute(
            """SELECT * FROM knowledge_state
               ORDER BY mastery ASC, review_count ASC"""
        ).fetchall()
        return [dict(r) for r in rows]

    # ── Write operations ──────────────────────────────────────────────────────

    def update(self, concept: str, correct: bool) -> dict:
        """Update mastery after a student answers a question.

        This is the ONLY way mastery changes. The Memory Agent calls this
        after qwen2.5:3b returns correct: bool. The model never sets mastery
        directly — it only judges correctness. This function owns the math.

        Returns the updated record so the caller can pass it immediately
        to the forgetting model without a second read.
        """
        record = self.get_or_init(concept)
        old_mastery = record["mastery"]

        if correct:
            new_mastery = old_mastery + LEARNING_RATE * (1.0 - old_mastery)
        else:
            new_mastery = old_mastery * DECAY_FACTOR

        # Clamp to [0.0, 1.0]. The formulas are mathematically bounded but
        # floating point arithmetic can produce 1.0000000000000002.
        new_mastery = round(min(1.0, max(0.0, new_mastery)), 6)

        self.conn.execute(
            """UPDATE knowledge_state
               SET mastery          = ?,
                   review_count     = review_count + 1,
                   mistake_count    = mistake_count + ?,
                   last_reviewed_at = ?
               WHERE concept        = ?""",
            (new_mastery, 0 if correct else 1, self._now(), concept),
        )
        self.conn.commit()
        return self.get(concept)

    # ── Utility ───────────────────────────────────────────────────────────────

    def reset(self, concept: str) -> None:
        """Remove a concept record entirely. Used in tests only."""
        self.conn.execute(
            "DELETE FROM knowledge_state WHERE concept = ?", (concept,)
        )
        self.conn.commit()

    def close(self) -> None:
        """Close the database connection cleanly."""
        self.conn.close()