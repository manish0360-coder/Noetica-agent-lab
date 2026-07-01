"""
judge_correctness — Day-2 BRIDGE for producing a correctness verdict.

⚠️ BRIDGE CODE. Temporary stand-in. The Reasoning Agent (Day 18) will own
correctness judgment as part of richer error analysis. When it exists, DELETE
this file and route verdict production through the Reasoning Agent.

Scope limits (documented debt):
  - judges ONLY correctness — no mistake_type, no misconception
  - uses qwen3:4b (~20-53s latency); acceptable for batch capstone, not interactive
  - returns None on any parse failure → the CALLER must NOT construct a Verdict
"""
import json
from core.llm import call_model
from core.agent import _extract_json

JUDGE_MODEL = "qwen3:4b"   # proven 6/6 on fraction correctness; qwen2.5 cannot do this

JUDGE_SYSTEM = (
    'Is the student answer mathematically correct? '
    'Respond ONLY: {"correct": true} or {"correct": false}'
)


def judge_correctness(question: str, student_answer: str) -> bool | None:
    """Judge whether a student's answer is correct.

    Returns True/False on a clean judgment, or None if the model output
    cannot be parsed into a boolean. None means 'could not determine' — the
    caller must NOT build a Verdict from it.
    """
    result = call_model(
        messages=[{"role": "user",
                   "content": f'Question: "{question}" Student answered: "{student_answer}".'}],
        system=JUDGE_SYSTEM,
        think=True,
        model=JUDGE_MODEL,
        max_tokens=1024,
    )

    try:
        parsed = json.loads(_extract_json(result["answer"]))
    except (ValueError, json.JSONDecodeError):
        return None

    value = parsed.get("correct", None)
    return value if isinstance(value, bool) else None