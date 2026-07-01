"""
Day 2 capstone: full memory subsystem on REAL qwen2.5:3b.

Runs two real student answers (same concept) through the full chain:
Extraction → Normalization → KnowledgeState → Forgetting → Enriched Record.

Evidence Day 2 is complete:
  - one concept, two real answers
  - mastery moves DOWN (wrong) then UP (correct)
  - exactly ONE store row
  - recall computed with a basis
  - both records unflagged
"""
from phase2_memory.knowledge_state import KnowledgeState
from phase2_memory.memory_agent import MemoryAgent


def show(label, rec):
    print(f"\n--- {label} ---")
    print(f"  concept     : {rec['concept']}")
    print(f"  correct     : {rec['correct']}")
    print(f"  mastery     : {rec['mastery']}")
    print(f"  recall      : {rec['recall']}")
    print(f"  basis       : {rec['basis']}")
    print(f"  misconception: {rec['misconception']!r}")
    print(f"  flagged     : {rec['flagged']}")


store = KnowledgeState(db_path=":memory:")
agent = MemoryAgent(store=store)

print("Running two real student answers through the full memory subsystem...")
print("(real qwen2.5:3b — first call includes model load, ~15s)")

# Answer 1 — WRONG: adds numerators and denominators
rec1 = agent.analyze("What is 1/2 + 1/4?", "3/6")
show("Answer 1: '3/6' (incorrect)", rec1)

# Answer 2 — CORRECT, same concept
rec2 = agent.analyze("What is 1/2 + 1/4?", "3/4")
show("Answer 2: '3/4' (correct)", rec2)

# ── Evidence checks ──────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("DAY 2 EVIDENCE CHECKS")

rows = store.get_all()
checks = [
    ("answer 1 judged incorrect",        rec1["correct"] is False),
    ("answer 2 judged correct",          rec2["correct"] is True),
    ("both unflagged",                   not rec1["flagged"] and not rec2["flagged"]),
    ("same concept both times",          rec1["concept"] == rec2["concept"]),
    ("exactly ONE store row",            len(rows) == 1),
    ("mastery rose after correct answer", rec2["mastery"] > rec1["mastery"]),
    ("recall computed (not None)",       rec2["recall"] is not None),
    ("review_count == 2",                rows[0]["review_count"] == 2),
    ("mistake_count == 1",               rows[0]["mistake_count"] == 1),
]
for label, ok in checks:
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")

store.close()
print("\nDay 2 capstone complete." if all(c[1] for c in checks)
      else "\nSome checks FAILED — inspect records above.")