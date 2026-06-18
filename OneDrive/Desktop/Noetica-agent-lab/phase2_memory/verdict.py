"""
Verdict: the typed contract between the Reasoning Agent (producer) and the
Memory Agent (consumer).

Pure data with construction-time validation. No LLM, no store, no I/O.

For Day 2, Verdicts are constructed manually (source="manual") and Memory reads
only `concept` and `correct`. The remaining fields are populated by the
Reasoning Agent (Day 18) and consumed by the Planner Agent (Day 19).
"""
from dataclasses import dataclass, field


@dataclass
class Verdict:
    concept: str               # canonical concept this verdict concerns
    correct: bool              # the correctness judgment
    mistake_type: str = ""     # fixed-taxonomy label; "" if correct (Planner, Day 19)
    misconception: str = ""    # human-readable detail; "" if correct (Phase 6 output)
    confidence: float = 1.0    # judge confidence in [0,1] (Planner weighting)
    source: str = "manual"     # producer id, for cross-agent tracing

    def __post_init__(self):
        # Type integrity: correct must be a genuine bool.
        # Guards the Day-2 bug where a truthy non-bool silently corrupts mastery.
        if not isinstance(self.correct, bool):
            raise ValueError(f"correct must be bool, got {type(self.correct).__name__}")

        # A verdict about no concept is meaningless.
        if not self.concept or not self.concept.strip():
            raise ValueError("concept must be a non-empty string")

        # Confidence must be a probability.
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"confidence must be in [0.0, 1.0], got {self.confidence}")

        # Internal consistency: a correct answer cannot carry a mistake.
        if self.correct and (self.mistake_type or self.misconception):
            raise ValueError("a correct verdict cannot carry mistake_type or misconception")