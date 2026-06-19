import ollama

resp = ollama.chat(
    model="qwen3:4b",
    messages=[{"role": "user",
               "content": "A farmer has 17 sheep. All but 9 run away. How many are left?"}],
    options={"temperature": 0, "num_predict": 512},
)

# Print the WHOLE object so we see every field Ollama actually returns.
print(resp)
print("=" * 60)
print("CONTENT FIELD:", repr(resp["message"]["content"]))
print("MESSAGE KEYS:", list(resp["message"].keys()))