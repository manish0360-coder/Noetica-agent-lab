import time
from core.llm import call_model

# The exact same question used in step7_eval.
# Holding the question constant is what makes model the only variable.
# If we changed the question per model, we couldn't attribute differences
# to the model — they might just be easier/harder questions.
GOAL = "A farmer has 17 sheep. All but 9 run away. How many are left?"

# Both models we want to compare.
# The seam's capability guard handles the think=True/False difference
# automatically — we pass the same call to both.
MODELS = ["qwen3:4b", "qwen2.5:3b"]

for model_name in MODELS:
    print(f"\n{'=' * 50}")
    print(f"MODEL: {model_name}")

    # Accumulators — we run 3 trials per model.
    # A single run on CPU inference can vary 10–20 seconds.
    # Three runs give us an average that's meaningful,
    # rather than a single point that might be an outlier.
    times, tokens, answers, parse_ok = [], [], [], []

    for i in range(3):
        start = time.perf_counter()   # monotonic, high-resolution — never jumps backward

        r = call_model(
            messages=[{"role": "user", "content": GOAL}],
            system="Answer with ONLY a number. No explanation.",
            # We pass think=True to BOTH models deliberately.
            # The seam's capability guard converts it to False for qwen2.5:3b.
            # This tests the guard under real conditions, not a workaround.
            think=True,
            model=model_name,
        )

        # wall_ms = total time from call entry to return, in milliseconds.
        # This includes Ollama IPC, generation, and our parsing.
        # It is the number the user experiences — more honest than tok/s alone.
        wall_ms = round((time.perf_counter() - start) * 1000)

        times.append(wall_ms)
        tokens.append(r["output_tokens"] or 0)
        answers.append(r["answer"])

        # parse_ok = did the answer channel return anything at all?
        # Empty string means the seam got nothing back from the model.
        # This is a different failure from "wrong answer" — we track both separately.
        parse_ok.append(bool(r["answer"].strip()))

        # thinking_len is the key diagnostic for the capability guard.
        # qwen3:4b  → should be ~2399 (thinking channel active)
        # qwen2.5:3b → must be 0 (no thinking channel; guard fired)
        # Non-zero thinking_len on qwen2.5:3b means the guard is broken.
        print(f"  run {i + 1}: "
              f"wall={wall_ms}ms | "
              f"tok_out={r['output_tokens']} | "
              f"thinking_len={len(r['thinking'])} | "
              f"answer={repr(r['answer'][:60])}")

    print(f"  --- summary ---")
    print(f"  avg wall : {sum(times) // len(times)}ms")
    print(f"  avg tok  : {sum(tokens) // len(tokens)}")

    # Correctness: does the answer contain "9"?
    # We use 'in' not '==' because the model might say "9 sheep" or "9." —
    # both are correct and both contain the digit.
    # The 'if a' guard skips empty answers so they don't count as wrong;
    # empty answers are already caught by parse_ok.
    correct = sum("9" in a for a in answers if a)
    print(f"  correct  : {correct}/3")
    print(f"  parse_ok : {sum(parse_ok)}/3")