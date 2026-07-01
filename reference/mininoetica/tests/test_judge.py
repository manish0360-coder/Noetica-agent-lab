"""
Tests for judge_correctness — the Day-2 bridge producing the `correct` bool
a Verdict needs, using qwen3:4b (proven 6/6 on fraction judgment).

Mocked tests are deterministic. One live test (-m live) hits real qwen3:4b.
"""
import pytest
import phase2_memory.judge as judge_mod
from phase2_memory.judge import judge_correctness


def _mock_model(answer_text):
    def _fake(messages, system="", max_tokens=2048, think=True, model=None):
        return {"answer": answer_text, "thinking": "", "stop_reason": "stop",
                "input_tokens": 5, "output_tokens": 5}
    return _fake


def test_true_judgment_returns_true(monkeypatch):
    monkeypatch.setattr(judge_mod, "call_model", _mock_model('{"correct": true}'))
    assert judge_correctness("1/2 + 1/4", "3/4") is True


def test_false_judgment_returns_false(monkeypatch):
    monkeypatch.setattr(judge_mod, "call_model", _mock_model('{"correct": false}'))
    assert judge_correctness("1/2 + 1/4", "3/6") is False


def test_prose_wrapped_json_is_recovered(monkeypatch):
    monkeypatch.setattr(judge_mod, "call_model",
                        _mock_model('After checking: {"correct": true}  Done.'))
    assert judge_correctness("q", "a") is True


def test_unparseable_output_returns_none(monkeypatch):
    monkeypatch.setattr(judge_mod, "call_model",
                        _mock_model("I cannot determine this."))
    assert judge_correctness("q", "a") is None


def test_missing_correct_field_returns_none(monkeypatch):
    monkeypatch.setattr(judge_mod, "call_model", _mock_model('{"answer": "maybe"}'))
    assert judge_correctness("q", "a") is None


def test_non_bool_correct_returns_none(monkeypatch):
    monkeypatch.setattr(judge_mod, "call_model", _mock_model('{"correct": "yes"}'))
    assert judge_correctness("q", "a") is None


@pytest.mark.live
def test_live_judges_six_cases_correctly():
    cases = [
        ("1/2 + 1/4", "3/4", True),  ("1/2 + 1/4", "3/6", False),
        ("1/3 + 1/3", "2/3", True),  ("2/5 + 1/5", "3/10", False),
        ("1/2 + 1/2", "1", True),    ("3/4 - 1/4", "1/2", True),
    ]
    for q, ans, truth in cases:
        assert judge_correctness(q, ans) is truth, f"{q}={ans} expected {truth}"