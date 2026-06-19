"""Confirm qwen3:4b is a reliable correctness judge on the BARE prompt,
across several fraction cases, with latency. This is the model we'd assign
to the judgment sub-task — verify before committing."""
import time
from core.llm import call_model

SYS = 'Is the student answer mathematically correct? Respond ONLY: {"correct": true} or {"correct": false}'
CASES = [
    ("1/2 + 1/4", "3/4", True), ("1/2 + 1/4", "3/6", False),
    ("1/3 + 1/3", "2/3", True), ("2/5 + 1/5", "3/10", False),
    ("1/2 + 1/2", "1", True),   ("3/4 - 1/4", "1/2", True),
]
for q, ans, truth in CASES:
    t = time.perf_counter()
    r = call_model(messages=[{"role":"user","content":f'Question: "{q}" Student answered: "{ans}".'}],
                   system=SYS, think=True, model="qwen3:4b", max_tokens=1024)
    ms = round((time.perf_counter()-t)*1000)
    print(f"  {q}={ans} truth={truth} -> {r['answer'][:40]!r} | {ms}ms | stop={r['stop_reason']}")