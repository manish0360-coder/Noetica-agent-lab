from core.llm import call_model

result = call_model(
    messages=[
        {
            "role": "user",
            "content": "A farmer has 17 sheep. All but 9 run away. How many are left?"
        }
    ]
)

print("STOP REASON:", result["stop_reason"])
print("ANSWER:", repr(result["answer"]))
print("THINKING len:", len(result["thinking"]))
print("TOKENS out:", result["output_tokens"])