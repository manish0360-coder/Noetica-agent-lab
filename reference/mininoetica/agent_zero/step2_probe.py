from core.llm import call_model

# A prompt that tends to trigger reasoning, so we can see if <think> leaks into content.
result = call_model(
    messages=[{"role": "user",
               "content": "A farmer has 17 sheep. All but 9 run away. "
                          "How many are left? Think it through, then answer."}],
    system="",
)

text = result["text"]
print("RAW REPETITION CHECK")
print("has <think>:", "<think>" in text.lower())
print("has </think>:", "</think>" in text.lower())
print("---- FULL RAW TEXT ----")
print(text)
print("---- END ----")
print("output tokens:", result["output_tokens"])