import json
import re
import time
import uuid
from datetime import datetime, timezone

from core.llm import call_model
from core.logger import log_run

AGENT_SYSTEM = """You are Agent Zero, a careful reasoning agent.
Reason toward the user's goal, then respond with ONLY a JSON object — no markdown, no prose:
{"status": "final", "answer": "<your final answer>"}
Only if you genuinely need another step, respond instead:
{"status": "continue", "note": "<what remains>"}
Prefer "final" when confident."""


def _extract_json(text: str) -> str:
    """Pull a JSON object from possibly-fenced, possibly-prose model output."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text).strip()
        text = re.sub(r"```$",          "", text).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("no JSON object found")
    return text[start:end + 1]


def run_agent(
    goal:      str,
    max_steps: int  = 5,
    check_fn         = None,   # fn(answer: str) -> bool  |  None = unverified
) -> dict:
    """Run Agent Zero toward a goal.

    Returns a structured record with:
      - terminated_reason  (final | max_steps | truncated)  — HOW it stopped
      - success            (True | False | None)            — WHETHER it succeeded
    These are orthogonal. Conflating them is the bug the design review identified.
    Every run is appended to data/agent_runs.jsonl.
    """
    run_id    = str(uuid.uuid4())
    run_start = time.perf_counter()

    messages             = [{"role": "user", "content": goal}]
    trace                = []
    parse_failures       = 0
    continue_count       = 0
    total_input_tokens   = 0
    total_output_tokens  = 0
    steps_taken          = 0
    terminated_reason    = "max_steps"   # overwritten on clean exit
    answer               = None

    for step in range(1, max_steps + 1):
        steps_taken = step
        step_start  = time.perf_counter()

        result  = call_model(messages, system=AGENT_SYSTEM, think=True)
        step_ms = round((time.perf_counter() - step_start) * 1000)

        total_input_tokens  += result["input_tokens"]  or 0
        total_output_tokens += result["output_tokens"] or 0

        # ── Layer 1: decode-level health check ────────────────────────────
        # "length" = output was truncated mid-stream.
        # This is NOT task-completion; it means this call's output is likely
        # broken and we cannot safely parse it. Halt and surface loudly.
        if result["stop_reason"] == "length":
            terminated_reason = "truncated"
            trace.append({"step": step, "event": "truncated", "latency_ms": step_ms})
            break

        raw = result["answer"]

        # ── Layer 2: task-level control signal ────────────────────────────
        try:
            parsed = json.loads(_extract_json(raw))
        except (ValueError, json.JSONDecodeError):
            parse_failures += 1
            trace.append({
                "step":        step,
                "event":       "parse_fail",
                "raw_preview": raw[:160],
                "latency_ms":  step_ms,
            })
            # One repair attempt: re-inject the bad output and ask again.
            messages.append({"role": "assistant", "content": raw})
            messages.append({
                "role":    "user",
                "content": 'Respond with ONLY valid JSON: '
                           '{"status":"final","answer":"..."} '
                           'or {"status":"continue","note":"..."}',
            })
            continue

        status = parsed.get("status")
        trace.append({
            "step":        step,
            "status":      status,
            "stop_reason": result["stop_reason"],
            "tokens_in":   result["input_tokens"],
            "tokens_out":  result["output_tokens"],
            "latency_ms":  step_ms,
        })

        if status == "final":
            answer            = parsed.get("answer", "")
            terminated_reason = "final"
            break

        # status == "continue": fold note back into context and iterate.
        continue_count += 1
        messages.append({"role": "assistant", "content": raw})
        messages.append({
            "role":    "user",
            "content": "Continue. When ready, respond with the final JSON.",
        })

    wall_ms = round((time.perf_counter() - run_start) * 1000)

    # ── Termination vs. success: two orthogonal axes ──────────────────────
    # terminated_reason answers: did the loop exit cleanly?
    # success answers: was the answer actually correct?
    # check_fn is the external verifier seam — today a lambda,
    # tomorrow the Evaluator Agent.
    success = check_fn(answer) if (check_fn and answer is not None) else None

    record = {
        "run_id":              run_id,
        "timestamp":           datetime.now(timezone.utc).isoformat(),
        "goal":                goal,
        "answer":              answer,
        "terminated_reason":   terminated_reason,
        "success":             success,
        "steps_taken":         steps_taken,
        "continue_count":      continue_count,
        "parse_failures":      parse_failures,
        "total_input_tokens":  total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "wall_ms":             wall_ms,
        "trace":               trace,
    }
    log_run(record)
    return record