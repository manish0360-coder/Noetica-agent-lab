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


class MemoryAgent:
    """Coordinates extraction → normalization → store → forgetting.

    Owns sequencing and two guards only:
      - correct is None  → flag, skip store
      - concept unknown  → flag, skip store
    All real logic lives in the subsystems it calls.
    """

    def __init__(self, store):
        self.store = store

    def analyze(self, question: str, student_answer: str) -> dict:
        # [1] Extraction (mocked in tests, real qwen2.5:3b in production)
        ext = extract_answer_analysis(question, student_answer)
        correct       = ext["correct"]
        misconception = ext["misconception"]

        # Guard 1: could not determine correctness → never update the store
        if correct is None:
            return _flagged_record(ext["raw_concept"], None, misconception,
                                   "extraction_failed_or_no_correctness")

        # [2] Normalization
        concept = normalize_concept(ext["raw_concept"])

        # Guard 2: off-curriculum → never write a junk row
        if concept == UNKNOWN:
            return _flagged_record(UNKNOWN, correct, misconception,
                                   "concept_not_in_curriculum")

        # [3] Store owns the mastery math
        record = self.store.update(concept, bool(correct))

        # [4] Forgetting model owns recall
        recall = recall_with_status(record)

        # [5] Assemble enriched record (sequencing only)
        return {
            "concept":       concept,
            "correct":       bool(correct),
            "mastery":       record["mastery"],
            "recall":        recall["recall"],
            "basis":         recall["basis"],
            "misconception": misconception,
            "flagged":       False,
            "flag_reason":   None,
        }