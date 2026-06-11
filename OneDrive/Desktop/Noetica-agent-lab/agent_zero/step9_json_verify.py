"""
JSON contract verification for qwen2.5:3b.

Before wiring this model into Memory and Planner agents, we verify it can
reliably produce the structured output those agents depend on.

Nothing in this file changes the architecture. It only measures behavior.
"""
import json
from core.llm import call_model
from core.agent import _extract_json   # our existing JSON extractor from step7

FAST_MODEL = "qwen2.5:3b"


# ── Helpers ───────────────────────────────────────────────────────────────────

def try_parse(text: str) -> tuple:
    """Attempt to extract and parse JSON from raw model output.

    Returns (parsed_dict, error_string).
    On success: ({"key": value, ...}, "")
    On failure: (None, "reason it failed")

    Why return a tuple instead of raising? Because in a test harness we want
    to count failures, not crash on them. Each failed parse is a data point.
    """
    try:
        return json.loads(_extract_json(text)), ""
    except (ValueError, json.JSONDecodeError) as e:
        return None, str(e)


def check(label: str, cond: bool) -> None:
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")


def run_schema_test(name, system, prompt, required_fields, type_checks, n=3):
    """Run n trials of a structured-output schema test.

    Args:
        name:            Human label for this test.
        system:          System prompt defining the exact JSON contract.
        prompt:          User message the model responds to.
        required_fields: List of field names that MUST be in the output.
                         A missing field is a contract violation — the downstream
                         agent will crash trying to read it.
        type_checks:     Dict of {field_name: expected_type}.
                         Types matter because the forgetting model does arithmetic
                         on mastery scores — a string "0.6" will crash it.
        n:               Number of trials. We need >1 because qwen2.5:3b is
                         fast enough that running 3 costs under 3 seconds total.
    """
    print(f"\n{'=' * 55}")
    print(f"SCHEMA TEST: {name}  (n={n}, model={FAST_MODEL})")

    valid_count = fields_count = types_count = 0

    for i in range(n):
        r = call_model(
            messages=[{"role": "user", "content": prompt}],
            system=system,
            think=True,       # capability guard silently disables for qwen2.5:3b
            model=FAST_MODEL,
            max_tokens=256,   # structured JSON should be short; cap prevents runaway prose
        )

        parsed, err = try_parse(r["answer"])

        valid   = parsed is not None
        # All required keys must be present — a missing key means the downstream
        # agent crashes when it tries to read it.
        fields_ok = valid and all(f in parsed for f in required_fields)
        # Each checked field must match its expected type.
        # isinstance(value, (int, float)) handles both 0.5 and 1 correctly.
        # Note: in Python, bool is a subclass of int, so we check bool first
        # for the `correct` field to avoid True/False being accepted as ints.
        types_ok = fields_ok and all(
            isinstance(parsed[f], t)
            for f, t in type_checks.items()
            if f in parsed
        )

        if valid:      valid_count  += 1
        if fields_ok:  fields_count += 1
        if types_ok:   types_count  += 1

        # ✓ = full pass, ~ = valid JSON but field/type issue, ✗ = no JSON
        symbol = "✓" if types_ok else ("~" if valid else "✗")
        output_preview = str(parsed) if parsed else f"RAW: {r['answer'][:80]}"
        print(f"  run {i + 1} [{symbol}]: {output_preview}")
        if err:
            print(f"           error: {err}")

    print(f"  ---")
    check(f"valid JSON    >= 2/{n}", valid_count  >= 2)
    check(f"fields present >= 2/{n}", fields_count >= 2)
    check(f"types correct  >= 2/{n}", types_count  >= 2)

    return valid_count, fields_count, types_count


# ── Schema Test 1: Memory Agent output ───────────────────────────────────────
# The Memory Agent must return this shape after analyzing a student answer.
# `mastery` feeds directly into the forgetting model (must be numeric).
# `correct` drives the update rule (must be boolean).
# `misconception` will be stored in the learner's history (must be string).
run_schema_test(
    name     = "Memory Agent — concept mastery record",
    system   = """\
You extract learning data from student answers.
Respond with ONLY this JSON. No prose, no markdown, no explanation:
{"concept": "<topic name>", "correct": <true or false>, "mastery": <float 0.0 to 1.0>, "misconception": "<one phrase or empty string>"}""",
    prompt   = 'Student was asked: "What is 1/2 + 1/4?" Student answered: "3/6". Evaluate.',
    required_fields = ["concept", "correct", "mastery", "misconception"],
    type_checks     = {
        "correct":      bool,          # must be True/False, not "true" string
        "mastery":      (int, float),  # numeric; 0.5 or 0 both acceptable
        "concept":      str,
        "misconception": str,
    },
)

# ── Schema Test 2: Planner Agent output ──────────────────────────────────────
# The Planner must return one of three actions: review / advance / remediate.
# The orchestrator routes the next step based on `next_action` — it must be
# a clean string the orchestrator can match exactly, not a paragraph.
run_schema_test(
    name     = "Planner Agent — next learning action",
    system   = """\
You decide the next learning action for a student.
Respond with ONLY this JSON. No prose, no markdown, no explanation:
{"next_action": "<review or advance or remediate>", "reason": "<one sentence>", "urgency": "<low or medium or high>"}""",
    prompt   = "Concept: fraction addition. Mastery score: 0.2. The student has failed this concept 3 times in a row.",
    required_fields = ["next_action", "reason", "urgency"],
    type_checks     = {
        "next_action": str,
        "reason":      str,
        "urgency":     str,
    },
)

# ── Schema Test 3: Enum discipline ───────────────────────────────────────────
# This is the hardest constraint for a small model: returning ONLY one of
# a fixed set of values. If the model says "medium-hard" or "moderate",
# the orchestrator's if/elif chain misses it silently.
# We test this separately because it's the most common small-model failure mode.
print(f"\n{'=' * 55}")
print(f"ENUM TEST: Does qwen2.5:3b respect controlled vocabulary?  (n=3)")

VALID_ACTIONS = {"review", "advance", "remediate"}
enum_pass = 0

for i in range(3):
    r = call_model(
        messages=[{"role": "user",
                   "content": "Student mastery: 0.9. Student has passed the last 4 questions correctly."}],
        system="""\
Decide next action. Respond with ONLY this JSON:
{"next_action": "<review or advance or remediate>"}""",
        think=True,
        model=FAST_MODEL,
        max_tokens=64,
    )
    parsed, _ = try_parse(r["answer"])
    action = parsed.get("next_action", "") if parsed else ""
    valid_enum = action in VALID_ACTIONS
    if valid_enum:
        enum_pass += 1
    symbol = "✓" if valid_enum else "✗"
    print(f"  run {i + 1} [{symbol}]: next_action={repr(action)}")

check(f"enum value in valid set >= 2/3", enum_pass >= 2)


# ── Parser Test: _extract_json against all known output shapes ───────────────
# These are NOT model calls. This tests our parser deterministically against
# the real shapes qwen models have been observed to produce.
# If the parser fails on a shape here, it will fail silently in production.
# This is the same discipline as step6_test_clean.
print(f"\n{'=' * 55}")
print("PARSER TEST: _extract_json against known output shapes (no model calls)")

parser_cases = [
    # (description,          raw_input,                                    expect_success)
    ("clean JSON",           '{"status": "ok", "value": 42}',              True),
    ("prose prefix",         'Here you go: {"status": "ok"}',              True),
    ("fenced json",          '```json\n{"status": "ok"}\n```',             True),
    ("fenced no lang",       '```\n{"status": "ok"}\n```',                 True),
    ("trailing prose",       '{"status": "ok"} Hope that helps!',          True),
    ("nested JSON",          '{"a": {"b": 1}, "c": [1,2]}',               True),
    ("pure prose",           "The answer is forty-two.",                    False),
    ("empty string",         "",                                            False),
    ("orphan close tag",     '</think>\n{"status": "ok"}',                 True),
]

parser_all_pass = True
for desc, raw, expect_ok in parser_cases:
    parsed, err = try_parse(raw)
    got_ok = parsed is not None
    passed = got_ok == expect_ok
    if not passed:
        parser_all_pass = False
    status = "PASS" if passed else "FAIL"
    result_str = f"parsed={list(parsed.keys())}" if parsed else f"failed ({err[:35]})"
    print(f"  [{status}] {desc:<22} → {result_str}")

check("all parser cases correct", parser_all_pass)

print(f"\nDone. data/agent_runs.jsonl NOT written — this test bypasses run_agent intentionally.")