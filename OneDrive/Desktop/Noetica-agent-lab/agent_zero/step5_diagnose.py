import ollama

resp = ollama.chat(
    model="qwen3:4b",
    messages=[{"role": "user",
               "content": "A farmer has 17 sheep. All but 9 run away. How many are left?"}],
    think=False,
    options={"temperature": 0, "num_predict": 2048},
)

msg = resp.message
content = msg.content or ""
thinking = getattr(msg, "thinking", None)

print("done_reason:", resp.done_reason)
print("thinking field is None?:", thinking is None)
print("thinking field len:", len(thinking or ""))
print("content has <think> tag?:", "<think>" in content)
print("content has </think> tag?:", "</think>" in content)
print("content length (chars):", len(content))
print("---- LAST 200 CHARS OF CONTENT ----")
print(repr(content[-200:]))