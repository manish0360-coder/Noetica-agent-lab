# Ontology of Artificial Cognition

**Status:** Draft v0.1

---

# 1. Purpose

The purpose of this ontology is to establish a precise computational language for describing artificial cognition within the MiniFlyWire research laboratory.

Rather than defining cognition as a collection of independent modules (such as memory, reasoning, planning, or attention), this ontology treats cognition as the continuous transformation of structured computational objects through well-defined operators.

This distinction provides a common scientific language for hypothesis generation, experimental design, implementation, visualization, and evaluation.

The ontology is intended to satisfy five requirements:

1. Every cognitive concept must possess a precise computational meaning.
2. Every cognitive mechanism must operate upon explicitly defined computational objects.
3. Every computational object must be experimentally observable or inferable.
4. Every proposed mechanism must be independently testable through intervention and ablation.
5. The ontology must remain independent of any particular implementation technology, allowing neural networks, symbolic systems, probabilistic models, reinforcement learning, or hybrid architectures to instantiate the same conceptual framework.

The ontology therefore serves as the formal language of the MiniFlyWire laboratory rather than as a cognitive architecture itself.


# 2. Foundational Principles

Every hypothesis, experiment, and implementation developed within the MiniFlyWire laboratory shall remain consistent with the following foundational principles.

### Principle 1 — Cognition operates on computational objects.

Artificial cognition is defined in terms of explicitly identifiable computational objects rather than loosely defined functional modules.

### Principle 2 — Computational objects are transformed by operators.

Memory, reasoning, planning, attention, perception, learning, and related cognitive functions are treated as computational operators that transform one or more computational objects.

### Principle 3 — Mechanisms are hypotheses.

Every proposed cognitive mechanism is treated as a scientific hypothesis subject to experimental validation, causal intervention, and possible rejection.

### Principle 4 — Explanation takes priority over performance.

Behavioral success alone does not constitute scientific understanding. Every mechanism should contribute explanatory value beyond task performance.

### Principle 5 — Ontology precedes implementation.

Computational objects and their relationships shall be defined before selecting algorithms, neural architectures, symbolic systems, or implementation technologies.

### Principle 6 — Scientific terminology takes precedence over novelty.

Whenever an established scientific concept adequately describes a computational object or mechanism, MiniFlyWire adopts the established terminology rather than introducing new names without experimental justification.

### Principle 7 — Engineering cognition requires explicit constraints.

Physical, logical, geometric, safety, manufacturing, and task-specific constraints are treated as first-class computational entities rather than implicit optimization objectives.

### Principle 8 — The ontology is implementation independent.

The ontology defines what exists within the computational theory of cognition. It does not prescribe how those objects must be implemented computationally.


# 3. Computational Objects

The MiniFlyWire ontology distinguishes computational objects according to their level of abstraction. Every higher-level representation is ultimately constructed from a finite set of irreducible computational objects.

## 3.1 Fundamental Computational Objects

Fundamental Computational Objects are the smallest meaningful computational entities defined by the ontology. They are treated as irreducible within the scope of the MiniFlyWire theory and serve as the building blocks from which all higher-level cognitive representations are constructed.

### Entity

An **Entity** represents any identifiable object, concept, agent, resource, or physical component that exists within the modeled domain.

Examples include physical objects, abstract concepts, manufactured components, human users, autonomous agents, materials, tools, and environments.

### Relation

A **Relation** defines a meaningful connection between two or more entities.

Relations describe structural, semantic, spatial, temporal, functional, causal, or organizational dependencies without prescribing how computation is performed.

### Constraint

A **Constraint** specifies the conditions under which entities, relations, or transitions remain valid.

Constraints represent physical laws, logical consistency, safety requirements, manufacturing limitations, resource bounds, geometric restrictions, or task-specific requirements.

Within MiniFlyWire, constraints are treated as first-class computational objects rather than implicit optimization objectives.

### Transition

A **Transition** defines a valid transformation between computational states.

Transitions describe how entities and their relationships may evolve under specific conditions while preserving the structural rules defined by the ontology.

Transitions represent knowledge about possible change rather than the computational execution of change itself.


## 3.2 Universal Properties

Universal Properties are mathematical attributes that parameterize Fundamental Computational Objects.

Unlike computational objects, properties cannot exist independently. Every property is associated with one or more entities, relations, constraints, or transitions and provides additional quantitative or qualitative information about those objects.

Examples of universal properties include, but are not limited to:

* Uncertainty
* Confidence
* Probability
* Precision
* Reliability
* Temporal validity
* Provenance

The ontology intentionally distinguishes computational objects from their properties.

For example, an Entity may possess uncertainty, a Relation may possess confidence, and a Transition may possess probability, but uncertainty, confidence, and probability do not exist independently as computational objects.

This distinction preserves a clear separation between structural knowledge and the mathematical quantities used to characterize that knowledge.


## 3.3 Composite Computational Objects

Composite Computational Objects are higher-level representations constructed from Fundamental Computational Objects and their associated properties. They organize knowledge into structures that support reasoning, planning, prediction, learning, and decision making.

### Structured Generative World Model

The **Structured Generative World Model** is the persistent computational representation of the agent's understanding of its domain.

Its purpose is to represent what is possible, valid, and causally consistent within the environment being modeled.

The Structured Generative World Model is constructed from entities, relations, constraints, and transitions together with their associated properties. It evolves gradually through learning and serves as the long-term knowledge structure upon which cognitive processes operate.

The World Model is intended to capture relatively stable knowledge rather than transient situational information.

---

### Cognitive State

The **Cognitive State** is the transient computational representation of the agent's current interpretation of the world.

Its purpose is to represent what the agent currently believes, intends, attends to, plans, and considers relevant while interacting with its environment.

The Cognitive State contains the active subset of information required for ongoing cognition, including current beliefs, goals, hypotheses, working memory, active plans, and state-specific uncertainty.

Unlike the Structured Generative World Model, the Cognitive State changes continuously as new observations are perceived, decisions are made, actions are executed, and evidence is evaluated.

The Cognitive State therefore represents the agent's moment-to-moment situational awareness rather than its long-term understanding of the world.


# 4. Computational Operators

## 4.1 Fundamental Computational Operators

* Perception
* Inference
* Execution
* Learning

## 4.2 Computational Mechanisms

* Attention
* Evaluation
* Credit Assignment
* Precision Weighting

## 4.3 Computational Strategies

* Curiosity
* Goal Selection
* Exploration

