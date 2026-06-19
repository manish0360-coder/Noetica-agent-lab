# Noetica Agent Lab - Project State

## Project Vision

Noetica is an experimental cognitive architecture designed to evolve beyond a simple chatbot.

Long-term goal:

* Reasoning Agent
* Planner Agent
* Memory Agent
* Evaluator Agent

working together through a shared control loop.

Current focus is building the foundational infrastructure required before multi-agent behavior is introduced.

---

# Current Architecture

```text
Noetica
    ↓
Seam (core/llm.py)
    ↓
Ollama
    ↓
Qwen3:4b
```

The seam acts as the boundary between Noetica and the model.

All model-specific quirks are handled here so the rest of the system remains stable.

---

# Development Journal

## Step 1 — Connect Model

Goal:

Connect Noetica to a local language model.

Completed:

* Installed Ollama
* Downloaded Qwen3:4b
* Verified local inference
* Connected Python application to Ollama API

Key Lesson:

A model is the brain. Noetica is the system that uses the brain.

---

## Step 2 — Find Thinking Field

Experiment:

Investigated where Qwen stores reasoning.

Discovery:

Qwen3 stores reasoning separately from answers.

Observed:

```python
{
    "thinking": "...",
    "content": ""
}
```

instead of:

```python
{
    "content": "<think>...</think> answer"
}
```

Key Lesson:

Never assume where information is stored.
Inspect the raw response first.

---

## Step 3 — Fix Seam

Problem:

The seam only read:

```python
content
```

and ignored reasoning.

Solution:

Redesigned seam contract.

Current contract:

```python
{
    "answer": str,
    "thinking": str,
    "stop_reason": str,
    "input_tokens": int,
    "output_tokens": int
}
```

Additional Fix:

Increased token budget from:

```python
512
```

to:

```python
2048
```

Result:

Reasoning and answers are now captured separately.

Key Lesson:

A seam protects the rest of the system from model changes.

---

## Step 4 — Reasoning Leakage

Experiment:

Compared:

```python
think=True
```

vs

```python
think=False
```

Discovery:

Disabling the structured thinking field did not eliminate reasoning.

Instead reasoning leaked into:

```python
answer
```

channel.

Observed output contained:

```text
</think>
```

and large reasoning traces.

Key Lesson:

Reasoning generation and reasoning routing are different problems.

---

## Step 5 — Diagnose Leak

Investigation:

Examined raw model responses.

Findings:

* thinking field absent when think=False
* orphan </think> tags present
* content channel polluted by reasoning artifacts

Conclusion:

Raw answer channel cannot be trusted.

Key Lesson:

Diagnose before fixing.

Evidence before assumptions.

---

## Step 6 — Build and Test Sanitizer

Goal:

Guarantee a clean answer channel.

Implemented:

```python
_clean_answer()
```

which removes:

* complete <think>...</think> blocks
* orphan </think> tags

Tests Passed:

* orphan_close
* full_block
* clean
* nested_noise

Result:

Answer channel now has deterministic cleanup behavior.

Key Lesson:

Trust tests, not assumptions.

---

## Step 7 — Agent Loop Design

Status:

Designed but not yet fully executed.

Goal:

Transform Noetica from:

```text
Question → Answer
```

into:

```text
Goal
 ↓
Think
 ↓
Decide
 ↓
Continue or Stop
```

Core Concepts:

* messages (state)
* trace (observability)
* max_steps (safety)
* status = final | continue
* stop_reason monitoring

Research Finding:

Agent termination and agent success are different concepts.

Example:

Agent may terminate successfully while still being wrong.

Future Evaluator Agent will verify correctness.

---

# Lessons Learned

1. Always inspect raw responses.
2. Never trust model output structure.
3. Separate reasoning from answers.
4. Normalize outputs at the seam.
5. Test deterministic logic independently from the model.
6. Log everything important.
7. Termination != correctness.

---

# Current Status

Completed:

✓ Model Integration

✓ Thinking Channel Discovery

✓ Seam Redesign

✓ Token Budget Fix

✓ Reasoning Leak Investigation

✓ Sanitizer Implementation

✓ Sanitizer Testing

✓ Agent Loop Design

In Progress:

→ Step 7 Agent Zero Execution

Next Major Goal:

Run the first real Agent Zero loop and collect metrics.

---

# Future Roadmap

Phase 1

* Agent Zero
* Logging
* Metrics
* Termination Analysis

Phase 2

* Planner Agent

Phase 3

* Memory Agent

Phase 4

* Tool Use

Phase 5

* Evaluator Agent

Phase 6

* Multi-Agent Cognitive Architecture

Long-Term Vision:

Noetica becomes a research platform for reasoning, planning, memory, evaluation, and autonomous learning.
