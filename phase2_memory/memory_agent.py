"""
Memory Agent — Step 2: extraction.

Extracts {raw_concept, correct, misconception} from a student answer using
qwen2.5:3b. This is the ONLY non-deterministic part of the Memory Agent.
Step 3 will wire normalization + store + forgetting around this.

Contract: extract_answer_analysis ALWAYS returns a dict with keys
raw_concept (str), correct (bool|None), misconception (str).
On any parse failure it returns EXTRACTION_FAILED — it never raises.
"""
import json
from core.llm import call_model
from core.agent import _extract_json

FAST_MODEL = "qwen2.5:3b"

# Returned when the model output cannot be parsed. correct=None signals
# "could not determine" so the pipeline can flag rather than crash.
EXTRACTION_FAILED = {
    "raw_concept": "",
    "correct": None,
    "misconception": "",
}

EXTRACTION_SYSTEM = """\
You extract learning data from a student's answer.
Respond with ONLY this JSON. No prose, no markdown, no explanation:
{"concept": "<topic name>", "correct": <true or false>, "misconception": "<one phrase or empty string>"}"""


def extract_answer_analysis(question: str, student_answer: str) -> dict:
    """Call the model and return parsed extraction, or EXTRACTION_FAILED.

    Never raises — a bad extraction is data (a flagged record), not a crash.
    """
    prompt = f'Student was asked: "{question}" Student answered: "{student_answer}" Evaluate.'

    result = call_model(
        messages=[{"role": "user", "content": prompt}],
        system=EXTRACTION_SYSTEM,
        think=True,            # capability guard disables for qwen2.5:3b
        model=FAST_MODEL,
        max_tokens=256,
    )

    try:
        parsed = json.loads(_extract_json(result["answer"]))
    except (ValueError, json.JSONDecodeError):
        return dict(EXTRACTION_FAILED)   # copy so callers can't mutate the constant

    return {
        "raw_concept":   parsed.get("concept", ""),
        "correct":       parsed.get("correct", None),
        "misconception": parsed.get("misconception", ""),
    }


from phase2_memory.concepts import normalize_concept, UNKNOWN
from phase2_memory.forgetting import recall_with_status


def _flagged_record(concept, correct, misconception, reason):
    """A record the pipeline produced but did NOT commit to the store."""
    return {
        "concept": concept,
        "correct": correct,
        "mastery": None,
        "recall": None,
        "basis": None,
        "misconception": misconception,
        "flagged": True,
        "flag_reason": reason,
    }



from phase2_memory.verdict import Verdict


def _flagged_record(verdict, concept, reason):
    """A record produced but NOT committed to the store."""
    return {
        "concept": concept,
        "correct": verdict.correct,
        "mastery": None,
        "recall": None,
        "basis": None,
        "misconception": verdict.misconception,
        "confidence": verdict.confidence,
        "source": verdict.source,
        "flagged": True,
        "flag_reason": reason,
    }


class MemoryAgent:
    """Consumes a Verdict and updates learner state.

    Pure and deterministic — no LLM. Owns sequencing only:
      normalize concept → (guard: unknown) → store.update → recall → enrich.
    The store owns mastery math; the forgetting model owns recall.
    """

    def __init__(self, store):
        self.store = store

    def update_from_verdict(self, verdict: Verdict) -> dict:
        # [1] Normalize the concept to a canonical curriculum key.
        concept = normalize_concept(verdict.concept)

        # Guard: off-curriculum → flag, write nothing.
        if concept == UNKNOWN:
            return _flagged_record(verdict, UNKNOWN, "concept_not_in_curriculum")

        # [2] Store owns the mastery math.
        record = self.store.update(concept, verdict.correct)

        # [3] Forgetting model owns recall.
        recall = recall_with_status(record)

        # [4] Assemble enriched record (sequencing only).
        return {
            "concept":       concept,
            "correct":       verdict.correct,
            "mastery":       record["mastery"],
            "recall":        recall["recall"],
            "basis":         recall["basis"],
            "misconception": verdict.misconception,
            "confidence":    verdict.confidence,
            "source":        verdict.source,
            "flagged":       False,
            "flag_reason":   None,
        }