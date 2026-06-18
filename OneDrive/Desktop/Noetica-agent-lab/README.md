# 🧠 Noetica


![Python](https://img.shields.io/badge/Python-3.10-blue)
![Tests](https://img.shields.io/badge/Tests-58%20Passed-success)
![Status](https://img.shields.io/badge/Status-Active%20Research-orange)
![Architecture](https://img.shields.io/badge/Architecture-Modular-purple)
![Local%20LLM](https://img.shields.io/badge/Local%20LLM-Ollama-green)


> **Building an Evidence-Based Learning Intelligence System**
>
> *From AI-assisted answer evaluation toward adaptive cognitive learning systems.*


Noetica is a research-oriented AI engineering laboratory focused on building cognitive learning systems from first principles. Rather than beginning with high-level agent frameworks, the project incrementally develops and validates the core primitives required for adaptive intelligence.


## 📌 Current Status

| Property | Value |
|----------|-------|
| 🔬 Project Stage | Active Research |
| 🧠 Current Phase | Phase 2 – Memory Agent |
| 🧪 Test Status | 58 Passed · 5 Skipped |
| 🤖 Models | Qwen3:4B, Qwen2.5:3B |
| 🛠️ Methodology | Test-Driven Development |
| 🏗️ Architecture | Modular Cognitive Architecture |



---

<div align="center">

## 🔬 Research First • 📊 Measurement Before Intelligence • 🤖 Local AI • 🧩 Explainable Architecture

</div>

---

# 📑 Table of Contents

- 📌 [Current Status](#-current-status)
- 📸 [Project Snapshot](#-project-snapshot)
- 🧠 [Why Noetica?](#-why-noetica)
- 🚨 [The Problem](#-the-problem)
- 💡 [Core Insight](#-core-insight)
- 🔬 [Research Foundation](#-research-foundation)
- 🏗️ [System Architecture](#-system-architecture)
- ⚙️ [Current Implementation](#-current-implementation)
- 📂 [Project Structure](#-project-structure)
- 🎯 [Engineering Principles](#-engineering-principles)
- 🛠️ [Technology Stack](#️-technology-stack)
- 🧪 [Testing Strategy](#-testing-strategy)
- 📈 [Roadmap](#-roadmap)
- 🚀 [Future Vision](#-future-vision)
- 📚 [Documentation](#-documentation)
- 👨‍💻 [Author](#-author)

---

---

# 📸 Project Snapshot

## 🗂️ Repository Structure

![Repository Structure](assets/screenshots/project_structure.png)

---

## 🧪 Automated Test Suite

![Test Results](assets/screenshots/test_results.png)

---


# 🧠 Why Noetica?

Artificial Intelligence can now generate essays, answer questions, summarize books, and solve programming problems.

Yet one fundamental question remains largely unanswered:

> [!IMPORTANT]
> ### **How do we know whether someone has actually learned?**

Most AI tutoring systems evaluate a single answer in isolation. They rarely distinguish between observable performance and underlying knowledge, cannot explain why a learner struggles, and generally lack a principled model of long-term learning.

Noetica is an experimental AI research project exploring a different direction.

Instead of beginning with assumptions about intelligence, Noetica begins with **measurement**.

The project investigates how observable learning signals—such as correctness, misconceptions, review history, and forgetting—can be transformed into structured representations that may eventually support adaptive educational systems.

Rather than building another chatbot, Noetica is being developed as a **research-first cognitive architecture** where every future capability must be justified by measurable evidence.

---

# 🚨 The Problem

Current AI-powered educational systems are remarkably good at generating information, but they remain surprisingly limited at understanding learning.

## ✅ Today's AI systems can

- Generate explanations
- Answer questions
- Evaluate a single response
- Produce personalized feedback

However, these capabilities are largely **stateless**.

Each interaction is treated as an isolated event rather than part of a learner's long-term cognitive journey.

## ❓ Questions today's AI still cannot answer

- Has this learner improved over time?
- Is this mistake new or recurring?
- Has the learner forgotten a previously mastered concept?
- Which misconception is repeatedly blocking progress?
- What concept should be studied next?
- How confident should the system be in its recommendations?

These questions require more than language generation.

They require **persistent memory**, **structured measurement**, **longitudinal observation**, and **careful reasoning about uncertainty**.

Noetica explores whether these missing capabilities can be built incrementally through measurable, deterministic components rather than assumed intelligence.

---

# 💡 Core Insight

> [!TIP]
> ## Learning cannot be modeled unless it is first measured.

Instead of attempting to build a complete cognitive architecture from the beginning, Noetica decomposes the problem into smaller, observable components.

## 🔍 Current research investigates

- 📖 How should learner knowledge be represented?
- 📈 How can mastery change over time?
- 🧠 How should forgetting be modeled?
- ✅ Which observations are trustworthy?
- ⚖️ Which signals should never be inferred without evidence?

Only after these questions have measurable answers does the project move toward higher-level reasoning and planning.

This philosophy influences every engineering decision inside Noetica—from **deterministic algorithms**, **versioned experiments**, and **test-driven development** to the explicit separation between **observation** and **inference**.


---

# 🔬 Research Foundation

Unlike most AI projects that begin with implementation, **Noetica began with research**.

Before writing production code, the project focused on understanding a much deeper question:

> **Can learning be measured before it is modeled?**

Over several weeks, Noetica evolved through multiple research documents, technical audits, design reviews, and validation studies before the first production components were implemented.

This research-first approach helps ensure that every engineering decision is grounded in measurable evidence rather than assumptions.

## 📚 Research Journey

```text
             💡 Initial Idea
                    │
                    ▼
        📄 Founder Decision Memo
                    │
                    ▼
      📝 Product Requirements (PRD)
                    │
                    ▼
      🔬 Measurement Science Research
                    │
                    ▼
        🧠 Bridge Hypothesis Design
                    │
                    ▼
     🛡️ Technical & Product Audits
                    │
                    ▼
       👨‍🏫 Concierge Pilot Design
                    │
                    ▼
        🏗️ System Architecture
                    │
                    ▼
        ⚙️ Implementation Begins
```

## 🎯 Research Philosophy

Every major capability inside Noetica follows the same engineering process:

```
Observation
      │
      ▼
Measurement
      │
      ▼
Validation
      │
      ▼
Architecture
      │
      ▼
Implementation
      │
      ▼
Testing
```

Rather than asking,

> **"How can we build an intelligent tutor?"**

Noetica asks,

> **"What can we measure reliably enough to justify intelligence?"**

That distinction defines the entire project.


---

# 🏗️ System Architecture

Noetica is being developed as a **modular cognitive architecture**.

Rather than building one monolithic AI system, the project separates learning into independent components, each responsible for a specific cognitive function.

This design makes every subsystem measurable, testable, and replaceable without affecting the rest of the architecture.

## 🎯 Long-Term Cognitive Architecture

```text
                             👤 Student
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │     Agent Orchestrator │
                    └─────────────┬──────────┘
                                  │
          ┌───────────────────────┼────────────────────────┐
          │                       │                        │
          ▼                       ▼                        ▼
   🧠 Memory Agent         📚 Knowledge Agent      🤔 Reasoning Agent
          │                       │                        │
          └───────────────────────┼────────────────────────┘
                                  │
                                  ▼
                          🗺️ Planner Agent
                                  │
                                  ▼
                         🎯 Learning Strategy
```

---

## 🧩 Current Development Status

At the current stage of development, Noetica is **not yet operating as a complete multi-agent system**.

Instead, each cognitive subsystem is being designed, implemented, and validated independently before orchestration.

This approach follows an important engineering principle:

> **Validate individual intelligence before coordinating collective intelligence.**

---

# 🎯 Engineering Philosophy

Noetica is not just an AI application.

It is an engineering journey to understand **how intelligent systems are built from first principles**.

Instead of relying on high-level agent frameworks, every core primitive is implemented manually before introducing abstraction.

This project deliberately postpones frameworks such as **LangChain**, **LangGraph**, and **CrewAI** until the underlying concepts have been fully understood and implemented.

The objective is not simply to build an AI system.

The objective is to understand **why** every component exists.

---

## 🧱 Build Order

```text
LLM Calls
      │
      ▼
Agent Loop
      │
      ▼
Structured Output
      │
      ▼
Memory
      │
      ▼
Knowledge State
      │
      ▼
Forgetting Model
      │
      ▼
Retrieval (RAG)
      │
      ▼
Tool Use
      │
      ▼
Single Agent
      │
      ▼
Multi-Agent System
      │
      ▼
Mini Noetica
```

---

## 🚀 Development Principles

- 🧠 Learn primitives before frameworks.
- 🧪 Test every subsystem independently.
- 📊 Measure before making intelligence claims.
- 🔄 Build modular, replaceable components.
- 🔍 Prefer deterministic engineering over hidden behavior.
- 📈 Validate every milestone before moving forward.



## ⚙️ Current Implemented Architecture

```text
                     👤 User
                        │
                        ▼
               🤖 Agent Loop
                        │
                        ▼
                 ⚙️ LLM Interface
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
      🧠 Qwen3:4B             ⚡ Qwen2.5:3B
 (Reasoning Tasks)        (Fast Structured Tasks)
                        │
                        ▼
              🧠 Memory Agent
                        │
                        ▼
               📚 Knowledge State
                        │
                        ▼
               🕒 Forgetting Model
                        │
                        ▼
              📊 Learner State Output
```

---

## 🏛️ Architectural Principles

The architecture follows five fundamental principles.

| Principle | Description |
|-----------|-------------|
| 🧩 Modular Design | Every cognitive capability is implemented as an independent subsystem. |
| 🧪 Test-Driven Development | Every module is validated through deterministic tests before integration. |
| 📊 Measurement Before Intelligence | Observable evidence is collected before higher-level reasoning is introduced. |
| 🔄 Replaceable Components | Any module can evolve without rewriting the entire architecture. |
| 🔍 Explainability | Every decision should be traceable and understandable rather than hidden inside a black box. |


---

# ⚙️ Current Implementation

Noetica is currently in the **foundational engineering phase**, where every cognitive primitive is implemented and validated independently before being integrated into a complete cognitive architecture.

The current implementation focuses on building reliable, deterministic AI infrastructure rather than prematurely combining multiple agents.

---

## ✅ Completed Components

### 🤖 Agent Foundation

- ✅ Local LLM integration through Ollama
- ✅ Provider-agnostic LLM interface
- ✅ Structured prompt pipeline
- ✅ Deterministic response handling
- ✅ Capability-aware model routing

---

### 🧠 Memory System

The Memory Agent is responsible for maintaining learner-specific information across interactions.

Current capabilities include:

- ✅ Persistent learner state
- ✅ Knowledge state tracking
- ✅ Memory update pipeline
- ✅ State serialization
- ✅ Forgetting model integration

---

### 📚 Knowledge Representation

Noetica represents learner understanding using structured knowledge states instead of relying solely on conversation history.

Current implementation includes:

- ✅ Knowledge State model
- ✅ Confidence representation
- ✅ Concept tracking
- ✅ Evidence-based updates
- ✅ Structured learner profile

---

### 🧪 Evaluation Pipeline

Every response produced by the system follows a structured evaluation workflow.

Current implementation includes:

- ✅ Structured verdict generation
- ✅ JSON contract validation
- ✅ Deterministic parsing
- ✅ Evaluation contracts
- ✅ Response normalization

---

### 🔍 Testing Infrastructure

The project follows **Test-Driven Development (TDD)**.

Implemented testing includes:

- ✅ Unit tests
- ✅ Integration tests
- ✅ Contract tests
- ✅ Migration-safe tests
- ✅ Regression testing

Every major subsystem is validated independently before integration.

---

## 🚧 Currently In Progress

The following components are actively under development.

- 🚧 Knowledge State refinement
- 🚧 Long-term memory refinement
- 🚧 Retrieval pipeline
- 🚧 Planner integration
- 🚧 Agent orchestration

---

## ⏳ Planned Components

The following systems are part of the long-term roadmap.

- ⏳ Reasoning Agent
- ⏳ Planning Agent
- ⏳ Multi-Agent orchestration
- ⏳ Adaptive learning strategies
- ⏳ Autonomous learning workflows
- ⏳ Research evaluation benchmarks

---

> [!NOTE]
>
> **Noetica intentionally avoids implementing complex multi-agent behavior until every foundational subsystem has been independently designed, tested, and validated.**


---

# 📂 Project Structure

The repository is organized around **modular AI engineering principles**, where each directory has a single, well-defined responsibility.

```text
Noetica/
│
├── agent_zero/          # Core agent execution pipeline
├── core/                # Shared infrastructure and LLM interface
├── data/                # Local datasets and persistent storage
├── docs/                # Architecture and project documentation
├── phase2_memory/       # Memory Agent implementation
├── tests/               # Unit, integration, and contract tests
├── README.md

```

---

## 🧩 Directory Overview

| Directory | Purpose |
|-----------|---------|
| 🤖 **agent_zero/** | Implements the foundational agent loop responsible for orchestrating interactions with the language model. |
| ⚙️ **core/** | Shared infrastructure including configuration, provider interfaces, utilities, contracts, and reusable components. |
| 💾 **data/** | Stores learner data, experiment outputs, and persistent information required by the system. |
| 📚 **docs/** | Contains research documents, architecture notes, engineering decisions, and supporting documentation. |
| 🧠 **phase2_memory/** | Implements learner memory, knowledge state tracking, confidence updates, and forgetting mechanisms. |
| 🧪 **tests/** | Comprehensive automated testing covering unit tests, integration tests, contracts, and regression validation. |

---

## 🎯 Repository Design Principles

The repository follows several important software engineering principles.

### 🧩 Single Responsibility

Every directory has one clearly defined responsibility.

---

### 🔄 Modular Development

Subsystems are implemented independently before being integrated into larger cognitive workflows.

---

### 🧪 Test Before Integration

Every module is validated independently through automated tests before becoming part of the larger architecture.

---

### 📈 Incremental Evolution

Rather than building one large AI system, Noetica grows through independently verifiable milestones.

This allows every architectural decision to be measured, evaluated, and improved without introducing unnecessary complexity.


---

# 🛠️ Technology Stack

Noetica is intentionally built using a **minimal, research-focused technology stack**. Every technology has been selected to support transparency, reproducibility, and modular AI engineering rather than rapid prototyping.

| Layer | Technology | Purpose |
|--------|------------|---------|
| 🐍 Programming Language | Python 3 | Core application logic and AI infrastructure |
| 🤖 Local LLM Runtime | Ollama | Local inference and model management |
| 🧠 Language Models | Qwen3:4B, Qwen2.5:3B | Reasoning and structured language tasks |
| 📡 LLM Interface | Provider-Agnostic Abstraction | Enables future support for multiple model providers |
| 💾 Data Storage | JSON, SQLite | Persistent learner state and structured memory |
| 🧪 Testing Framework | Pytest | Unit, integration, and contract testing |
| 🔄 Version Control | Git & GitHub | Source code management and collaboration |
| 📝 Documentation | Markdown | Technical documentation and architecture |

---

## 🎯 Technology Selection Philosophy

Instead of maximizing the number of technologies, Noetica minimizes unnecessary complexity.

Every technology is selected using three principles:

- ✅ **Simple enough to understand deeply**
- ✅ **Modular enough to replace later**
- ✅ **Reliable enough for deterministic engineering**

This philosophy keeps the project focused on **AI system design**, rather than framework-specific implementation details.

---

## 🚫 Technologies Intentionally Deferred

One of the defining characteristics of Noetica is **knowing what not to use yet**.

The project deliberately postpones higher-level AI frameworks until the underlying concepts have been implemented from first principles.

Examples include:

- ⏳ LangChain
- ⏳ LangGraph
- ⏳ CrewAI
- ⏳ AutoGen

The objective is to understand **how these frameworks work internally** before adopting them.


---

# 🧪 Testing Strategy

Noetica follows a **Test-Driven Development (TDD)** approach where every major subsystem is validated independently before integration.

The goal is not simply to verify that code executes correctly, but to ensure that every cognitive primitive behaves **deterministically**, **consistently**, and **predictably**.

---

## 🎯 Testing Philosophy

Instead of testing the entire AI system as one large application, Noetica validates each subsystem individually before combining them into larger cognitive workflows.

This provides:

- ✅ Easier debugging
- ✅ Reliable integration
- ✅ Safer refactoring
- ✅ Deterministic behavior
- ✅ Reproducible experiments

---

## 🔬 Current Test Coverage

| Test Category | Purpose |
|--------------|---------|
| 🧪 Unit Tests | Validate individual functions and components |
| 🔗 Integration Tests | Verify interaction between multiple subsystems |
| 📜 Contract Tests | Ensure structured JSON responses follow predefined schemas |
| 🔄 Regression Tests | Prevent previously solved bugs from reappearing |
| 🛡️ Migration Tests | Verify architectural changes do not break existing functionality |

---

## 📈 Validation Workflow

```text
Write Requirement
        │
        ▼
Design Interface
        │
        ▼
Write Tests
        │
        ▼
Implement Feature
        │
        ▼
Run Validation
        │
        ▼
Integrate into System
```

---




---

# 📈 Development Roadmap

Noetica is being developed incrementally through **independently verifiable engineering milestones**.

Rather than implementing a complete AI system at once, every phase introduces one cognitive capability, validates it thoroughly, and only then proceeds to the next stage.

---

## 🚀 Project Evolution

| Phase | Status | Objective |
|--------|:------:|-----------|
| ✅ Phase 1 | Complete | Local LLM integration and Agent Foundation |
| ✅ Phase 2 | Complete | Memory Agent and persistent learner state |
| 🚧 Phase 3 | In Progress | Knowledge State and structured learner representation |
| ⏳ Phase 4 | Planned | Retrieval-Augmented Generation (RAG) |
| ⏳ Phase 5 | Planned | Tool Use and external capability integration |
| ⏳ Phase 6 | Planned | Reasoning Agent |
| ⏳ Phase 7 | Planned | Planner Agent |
| ⏳ Phase 8 | Planned | Multi-Agent orchestration |
| ⏳ Phase 9 | Planned | Adaptive learning workflows |
| ⏳ Phase 10 | Planned | Research evaluation and benchmarking |

---

## 🗺️ Long-Term Vision

```text
LLM
 │
 ▼
Agent Foundation
 │
 ▼
Memory
 │
 ▼
Knowledge State
 │
 ▼
Retrieval
 │
 ▼
Tool Use
 │
 ▼
Reasoning
 │
 ▼
Planning
 │
 ▼
Multi-Agent Intelligence
 │
 ▼
Adaptive Learning System
```

---

## 🎯 Milestone Philosophy

Each milestone must satisfy three requirements before the next phase begins.

- ✅ Functionally complete
- ✅ Fully tested
- ✅ Architecturally validated

This disciplined development process ensures that future cognitive capabilities are built on stable and well-understood foundations rather than accumulated complexity.

> [!IMPORTANT]
>
> **Every completed milestone becomes a permanent building block for the next stage of Noetica's evolution.**


---

# 🎓 Key Engineering Lessons

Building Noetica has been more than writing code—it has been an exercise in understanding how intelligent systems should be engineered from first principles.

Throughout development, several important engineering lessons emerged.

---

## 🧠 Intelligence Requires Infrastructure

One of the earliest discoveries was that **language models are fundamentally stateless**.

Any system expected to demonstrate learning, adaptation, or long-term reasoning must explicitly manage its own memory, knowledge representation, and state.

---

## 📊 Measurement Comes Before Intelligence

A recurring principle throughout Noetica is:

> **What cannot be measured should not be claimed.**

Instead of attempting to simulate intelligence directly, the project first focuses on collecting reliable evidence about learner behavior.

Only then can higher-level reasoning become meaningful.

---

## 🧩 Modular Systems Scale Better

Breaking the architecture into independent cognitive subsystems makes development significantly easier.

Each subsystem can be:

- independently designed
- independently tested
- independently improved
- independently replaced

without rewriting the entire architecture.

---

## 🧪 Testing Is Part of the Architecture

Testing was treated as an architectural decision rather than a development task.

Reliable AI systems require deterministic validation before introducing increasingly complex behaviors.

---

## 🚀 Frameworks Should Follow Understanding

Instead of beginning with high-level agent frameworks, Noetica intentionally builds every primitive manually.

Understanding **why** a framework exists is more valuable than simply learning **how** to use it.

---

## 💡 The Biggest Lesson

The most valuable realization during this project was:

> **Building intelligent systems is not primarily an AI problem.**

It is a systems engineering problem involving architecture, measurement, state management, validation, and careful incremental design.


---

# 🚀 Future Vision

Noetica is not intended to become another conversational AI assistant.

The long-term vision is to develop an **evidence-based cognitive learning architecture** capable of understanding how learners acquire, retain, and apply knowledge over time.

Rather than optimizing for conversation quality alone, the project explores how AI systems can support **measurable learning**, **adaptive guidance**, and **transparent reasoning**.

---

## 🌍 Long-Term Vision

The future evolution of Noetica aims to combine several independent cognitive capabilities into a unified learning system.

```text
                👤 Learner
                     │
                     ▼
          🧠 Memory & Knowledge
                     │
                     ▼
          📊 Learning Measurement
                     │
                     ▼
          🤔 Cognitive Reasoning
                     │
                     ▼
           🗺️ Adaptive Planning
                     │
                     ▼
        🎯 Personalized Learning
                     │
                     ▼
     📈 Continuous Learning Improvement
```

---

## 🔬 Research Directions

Future research areas include:

- 🧠 Long-term learner modeling
- 📚 Dynamic knowledge graph construction
- 🤔 Explainable reasoning pipelines
- 📊 Confidence estimation
- 🎯 Adaptive study planning
- 🔄 Continuous memory consolidation
- 🌐 Multi-agent collaboration
- 📈 Learning outcome evaluation

---

## 🎯 Guiding Principle

Noetica will continue to evolve according to one simple principle:

> **Every new capability must be supported by measurable evidence, validated engineering, and transparent reasoning.**

The objective is not to build the largest AI system.

The objective is to build one that is **understandable, measurable, and scientifically grounded.**


---

# 📚 Documentation

Noetica is developed as both an **engineering project** and a **research initiative**.

To make the project easier to understand and contribute to, the documentation is organized into multiple levels of technical depth.

| Document | Description |
|----------|-------------|
| 📖 **README.md** | High-level overview, project motivation, architecture summary, and setup instructions. |
| 🏗️ **ARCHITECTURE.md** | Detailed explanation of the system architecture, cognitive components, and data flow. |
| 📘 **TECHNICAL_DOSSIER.md** | In-depth engineering documentation covering algorithms, implementation details, and design decisions. |
| 🧪 **ENGINEERING_JOURNAL.md** *(Planned)* | Development history, experiments, lessons learned, and architectural evolution. |

---

## 📂 Supporting Resources

The repository also includes supporting materials such as:

- 📸 Screenshots of the current implementation
- 🎥 Demonstration videos and GIFs
- 📊 Architecture diagrams
- 🧪 Test outputs and validation reports
- 📝 Research notes and design documents

These resources are intended to make both the engineering process and research decisions transparent and reproducible.

---

## 🎯 Documentation Philosophy

The documentation follows the same philosophy as the software itself:

- 📊 Explain before optimizing.
- 🔬 Measure before claiming.
- 🧩 Build before abstracting.
- 🧪 Validate before integrating.

The goal is not only to present the final system, but also to document the engineering journey behind its development.


---

# 👨‍💻 About the Author

Hi! I'm **Manish Kumar**, an AI Engineer passionate about building intelligent systems from **first principles**.

Rather than relying solely on high-level AI frameworks, I enjoy understanding how modern AI systems work internally—from language model interfaces and memory architectures to reasoning pipelines, planning systems, and multi-agent coordination.

Noetica represents my ongoing journey of learning, researching, and engineering AI systems that are **measurable**, **explainable**, and **modular**.

---

## 🎯 Research Interests

- AI Research Engineering
- Large Language Models (LLMs)
- Cognitive Architectures
- AI Agents & Multi-Agent Systems

---

## 🌱 Current Focus

I'm currently focused on building AI systems that combine:

- Long-term memory
- Knowledge representation
- Structured reasoning
- Adaptive planning
- Explainable decision making

My long-term goal is to contribute to cutting-edge AI research and engineering, building systems that are both scientifically grounded and practically useful.

---

## 📫 Connect With Me

- 💻 **GitHub:** https://github.com/manish0360-coder
- 💼 **LinkedIn:** *(Coming Soon)*
- 📧 **Email:** manishyaduvansh0360@gmail.com

---

<div align="center">

### ⭐ If you found this project interesting, consider giving it a star!

**Thank you for visiting Noetica.**

*"Building AI one primitive at a time."*

</div>