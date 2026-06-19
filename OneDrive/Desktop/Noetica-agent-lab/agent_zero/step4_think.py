from core.llm import call_model

q = [{"role": "user", "content": "A farmer has 17 sheep. All but 9 run away. How many are left?"}]

print("=== think=True ===")
r1 = call_model(q, think=True)
print("answer:", repr(r1["answer"])[:120])
print("thinking len:", len(r1["thinking"]), "| output tokens:", r1["output_tokens"])

print("\n=== think=False ===")
r2 = call_model(q, system="Answer with only the number. No explanation.", think=False)
print("answer:", repr(r2["answer"]))
print("thinking len:", len(r2["thinking"]), "| output tokens:", r2["output_tokens"])