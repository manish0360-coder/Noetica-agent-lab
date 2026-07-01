from core.llm import call_model

result = call_model(
    messages=[{"role": "user", "content": "In one sentence, what is an AI agent?"}],
    system="You are precise. Answer in one sentence.",
)

print("TEXT:        ", result["text"])
print("STOP REASON: ", result["stop_reason"])
print("TOKENS (in): ", result["input_tokens"])
print("TOKENS (out):", result["output_tokens"])