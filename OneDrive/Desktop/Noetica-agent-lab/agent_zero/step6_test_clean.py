from core.llm import _clean_answer

cases = {
    "orphan_close": "Okay let me think. Wait, 9 are left.</think>\n\n9",
    "full_block":   "<think>lots of reasoning here\nmore</think>The answer is 9.",
    "clean":        "The answer is 9.",
    "nested_noise": "intro <think>step1\nstep2</think> middle </think> 9",
}

for name, raw in cases.items():
    out = _clean_answer(raw)
    print(f"{name:14} -> {out!r}")