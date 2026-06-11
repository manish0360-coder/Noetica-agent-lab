# Noetica Agent Lab

Experimental AI-agent architecture for building **Noetica** — an adaptive learning intelligence engine.

---

## Vision

Noetica aims to become a personalized learning system that can:

- Understand what a student knows
- Detect misconceptions
- Track mastery over time
- Model forgetting and recall
- Plan the next best learning action
- Continuously adapt instruction

The long-term architecture consists of four cooperating agents:

1. Knowledge Agent
2. Reasoning Agent
3. Memory Agent
4. Planner Agent

---

## Current Status

### Day 1 Complete ✅

Built the foundational agent infrastructure:

- Provider-agnostic LLM seam
- Thinking / answer channel separation
- Reasoning-leak sanitizer
- Capability-aware model routing
- Structured agent loop
- Termination controls
- JSON output contracts
- Evaluation harness
- Run logging
- Multi-model benchmarking

---

## Architecture

```text
User
  │
  ▼
Agent Loop
  │
  ▼
LLM Seam
 ├── qwen3:4b (Reasoning)
 └── qwen2.5:3b (Fast Agents)
```

---

## Model Allocation Strategy

| Agent | Model |
|---------|---------|
| Knowledge Agent | qwen2.5:3b |
| Memory Agent | qwen2.5:3b |
| Planner Agent | qwen2.5:3b |
| Reasoning Agent | qwen3:4b |

---

## Day 1 Discoveries

### Thinking Channel

Reasoning models produce:

```python
{
    "answer": "...",
    "thinking": "..."
}
```

Separating these channels dramatically improves parsing reliability.

### Capability-Aware Routing

Different models support different capabilities.

The LLM seam automatically enables or disables reasoning features depending on the model being used.

### Latency Findings

CPU benchmark results:

| Model | Average Warm Latency |
|---------|---------|
| qwen3:4b | ~48 seconds |
| qwen2.5:3b | ~0.4 seconds |

This led to a hybrid model architecture where only the Reasoning Agent uses deep reasoning.

---

## Project Structure

```text
agent_zero/
    Experimental agent development

core/
    LLM seam
    Agent loop
    Shared infrastructure

data/
    Logs
    Evaluation artifacts

docs/
    Project documentation
    Development journal
```

---

## Roadmap

### Phase 1
- [x] LLM Seam
- [x] Thinking Channel Discovery
- [x] Sanitization Layer
- [x] Agent Loop
- [x] Evaluation Framework

### Phase 2
- [ ] KnowledgeState Store
- [ ] Forgetting Model
- [ ] Memory Agent

### Phase 3
- [ ] Knowledge Agent

### Phase 4
- [ ] Reasoning Agent

### Phase 5
- [ ] Planner Agent

### Phase 6
- [ ] Full Multi-Agent Orchestration

---

## Philosophy

Measure before optimizing.

Every architectural decision in Noetica must be backed by empirical evaluation rather than assumptions.

---

## Author

Manish Kumar

Noetica Agent Lab — Building an adaptive learning intelligence engine.