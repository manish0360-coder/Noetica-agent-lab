import re

import ollama

MODEL = "qwen3:4b"  # smaller than qwen3 to speed up dev iterations; upgrade for final evaluation

THINKING_MODELS = {"qwen3:4b"}

_THINK_BLOCK = re.compile(r"<think>.*?</think>", re.DOTALL)  # full block, if both tags present


def _clean_answer(text: str) -> str:
    """Guarantee a clean answer channel regardless of leaked reasoning markup.

    Qwen3 was trained to wrap reasoning in <think>...</think>. With think=False,
    Ollama suppresses the structured field but the model still leaks the markup
    into content — sometimes a full block, sometimes an orphan </think>.
    This is the single chokepoint that makes the answer channel trustworthy.
    """
    text = _THINK_BLOCK.sub("", text)          # remove complete <think>...</think> blocks
    if "</think>" in text:                      # orphan closing tag: keep only what's AFTER it
        text = text.split("</think>")[-1]
    return text.strip()


def call_model(messages: list[dict], system: str = "",
               max_tokens: int = 2048, think: bool = True,
               model: str = MODEL) -> dict:

    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.extend(messages)

    # Capability guard: never send think=True to a model that doesn't support it.
    # Degrades silently — the caller's intent is preserved where possible.
    effective_think = think and (model in THINKING_MODELS)

    resp = ollama.chat(
        model=model,
        messages=msgs,
        think=effective_think,
        options={
            "temperature": 0,
            "num_predict": max_tokens,
        },
    )

    msg = resp.message
    return {
        "answer":       _clean_answer(msg.content or ""),
        "thinking":     (getattr(msg, "thinking", None) or "").strip(),
        "stop_reason":  resp.done_reason,
        "input_tokens": resp.prompt_eval_count,
        "output_tokens": resp.eval_count,
    }