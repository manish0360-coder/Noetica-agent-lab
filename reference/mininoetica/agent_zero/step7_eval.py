import core.agent as agent_module
from core.agent import run_agent


def check(label: str, cond: bool) -> None:
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")


def run_suite(name, goal, check_fn, n=3, max_steps=5):
    """Run n trials and report pass rate — not a single brittle boolean."""
    print(f"\n{'=' * 55}")
    print(f"SUITE: {name}  (n={n}, max_steps={max_steps})")

    results = [run_agent(goal, max_steps=max_steps, check_fn=check_fn)
               for _ in range(n)]

    verified = [r["success"] for r in results if r["success"] is not None]
    pass_rate = sum(verified) / len(verified) if verified else None

    for i, r in enumerate(results, 1):
        print(f"  run {i}: "
              f"term={r['terminated_reason']:<10} | "
              f"success={str(r['success']):<5} | "
              f"steps={r['steps_taken']} | "
              f"wall={r['wall_ms']}ms | "
              f"tok_out={r['total_output_tokens']}")

    print(f"  pass_rate : "
          f"{pass_rate:.0%}" if pass_rate is not None else "  pass_rate : unverified")

    check("all runs terminate within budget",
          all(r["steps_taken"] <= max_steps for r in results))
    check("no truncations",
          all(r["terminated_reason"] != "truncated" for r in results))
    check("all records have answer key",
          all("answer" in r for r in results))
    if pass_rate is not None:
        check("pass_rate >= 0.67  (2 of 3 correct)",
              pass_rate >= 0.67)

    return results


# ── Suite 1: correctness anchor (trivial arithmetic) ──────────────────────────
run_suite(
    name      = "sheep riddle",
    goal      = "A farmer has 17 sheep. All but 9 run away. How many are left?",
    check_fn  = lambda ans: ans is not None and "9" in ans,
    n         = 3,
)

# ── Suite 2: prose output (does the loop corrupt non-numeric answers?) ─────────
run_suite(
    name      = "short explanation",
    goal      = "In two sentences, explain why the sky is blue.",
    check_fn  = lambda ans: ans is not None and len(ans.split()) >= 10,
    n         = 2,
)

# ── Suite 3: deterministic cap test (zero model calls) ────────────────────────
print(f"\n{'=' * 55}")
print("SUITE: cap enforcement  (mocked — no model call)")

_original = agent_module.call_model
agent_module.call_model = lambda *a, **k: {
    "answer":       '{"status":"continue","note":"never done"}',
    "thinking":     "",
    "stop_reason":  "stop",
    "input_tokens": 1,
    "output_tokens": 1,
}
r = run_agent("loop forever", max_steps=3)
agent_module.call_model = _original          # restore immediately

check("terminated_reason == max_steps",  r["terminated_reason"] == "max_steps")
check("steps_taken == 3",               r["steps_taken"] == 3)
check("answer is None",                 r["answer"] is None)
check("success is None (unverified)",   r["success"] is None)
check("continue_count == 3",            r["continue_count"] == 3)

print(f"\nAll runs logged → data/agent_runs.jsonl")