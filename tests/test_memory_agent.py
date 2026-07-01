"""
Tests for Memory Agent Step 2: extraction (the LLM call in isolation).

Strategy: mock call_model so extraction logic is deterministic. One live
smoke test (marked) hits the real model to verify real output is parseable.
"""
import pytest
import phase2_memory.memory_agent as ma
from phase2_memory.memory_agent import extract_answer_analysis, EXTRACTION_FAILED


def _mock_model(answer_text):
    """Build a fake call_model that returns a fixed answer string."""
    def _fake(messages, system="", max_tokens=2048, think=True, model=None):
        return {
            "answer": answer_text,
            "thinking": "",
            "stop_reason": "stop",
            "input_tokens": 10,
            "output_tokens": 10,
        }
    return _fake


# ── Happy path ────────────────────────────────────────────────────────────────

def test_valid_json_parsed_with_correct_types(monkeypatch):
    """Clean JSON from the model → dict with all 3 fields, correct types."""
    monkeypatch.setattr(ma, "call_model", _mock_model(
        '{"concept": "fraction addition", "correct": false, "misconception": "added denominators"}'
    ))
    result = extract_answer_analysis("What is 1/2 + 1/4?", "3/6")

    assert result["raw_concept"]   == "fraction addition"
    assert result["correct"]       is False         # genuine bool, not "false"
    assert result["misconception"] == "added denominators"


def test_json_wrapped_in_prose_is_recovered(monkeypatch):
    """Model adds chatter around the JSON → _extract_json still recovers it."""
    monkeypatch.setattr(ma, "call_model", _mock_model(
        'Here is my analysis: {"concept": "fractions", "correct": true, "misconception": ""}  Done!'
    ))
    result = extract_answer_analysis("q", "a")

    assert result["raw_concept"] == "fractions"
    assert result["correct"]     is True


# ── Failure path — must never crash ──────────────────────────────────────────

def test_malformed_json_returns_safe_sentinel(monkeypatch):
    """Unparseable model output → safe sentinel, NOT an exception.

    The pipeline must keep moving; a bad extraction becomes a flagged
    'failed' record, never a crash mid-orchestration.
    """
    monkeypatch.setattr(ma, "call_model", _mock_model("I think the student is confused about math."))
    result = extract_answer_analysis("q", "a")

    assert result == EXTRACTION_FAILED
    assert result["correct"] is None        # None = "could not determine"


def test_missing_fields_filled_with_defaults(monkeypatch):
    """Valid JSON but missing keys → defaults, not KeyError downstream."""
    monkeypatch.setattr(ma, "call_model", _mock_model('{"concept": "fractions"}'))
    result = extract_answer_analysis("q", "a")

    assert result["raw_concept"]   == "fractions"
    assert result["correct"]       is None      # missing → None
    assert result["misconception"] == ""        # missing → empty string


# ── Live smoke test (real model) ─────────────────────────────────────────────

@pytest.mark.live
def test_live_extraction_returns_parseable_fields():
    """Real qwen2.5:3b must return the three fields, parseable.

    Verifies the long-standing assumption that real LLM output matches our
    test inputs. Run with: pytest -m live
    """
    result = extract_answer_analysis(
        "What is 1/2 + 1/4?", "3/6"
    )
    assert result is not EXTRACTION_FAILED
    assert isinstance(result["raw_concept"], str) and result["raw_concept"]
    assert result["correct"] in (True, False)   # must be a real judgment