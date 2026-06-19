"""Isolate: is wrong correctness-judgment a model ceiling or a prompt problem?
Tests qwen2.5:3b AND qwen3:4b, each on a bare correctness question vs our
extraction prompt. Pure call_model — bypasses the Memory Agent entirely."""
from core.llm import call_model

CASES = [
    ("1/2 + 1/4", "3/4", True),   # correct
    ("1/2 + 1/4", "3/6", False),  # wrong
]

# Prompt A: minimal, single-purpose — "just judge correctness"
SYS_A = 'Is the student answer mathematically correct? Respond ONLY: {"correct": true} or {"correct": false}'

# Prompt B: our current extraction prompt (multi-task)
SYS_B = ('You extract learning data from a student\'s answer. Respond with ONLY this JSON: '
         '{"concept":"<topic>","correct":<true or false>,"misconception":"<phrase or empty>"}')

for model in ["qwen2.5:3b", "qwen3:4b"]:
    for label, sys in [("A: bare judge", SYS_A), ("B: extraction", SYS_B)]:
        print(f"\n=== {model} | {label} ===")
        for q, ans, truth in CASES:
            r = call_model(
                messages=[{"role":"user","content":f'Question: "{q}" Student answered: "{ans}".'}],
                system=sys, think=True, model=model, max_tokens=512,
            )
            print(f"  {q}={ans} (truth={truth}) -> {r['answer'][:90]}")