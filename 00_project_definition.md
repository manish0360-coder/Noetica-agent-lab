# 1. Purpose of this Document

Scientific research depends on precise definitions. Before hypotheses can be proposed, experiments designed, or architectures evaluated, every researcher must share the same understanding of the fundamental concepts being studied.

The purpose of this document is to establish the official terminology used throughout the MiniFlyWire research program.

This document does not describe implementation details, software architecture, programming languages, or engineering decisions. Instead, it defines the scientific meaning of the core concepts that guide the project.

These definitions provide a common vocabulary for future research documents, experimental protocols, benchmarks, implementation decisions, and scientific publications.

If a concept is not defined here, it should not become part of the research architecture until a clear, computationally meaningful definition has been established.

This document serves as the reference foundation for MiniFlyWire, Noetica, and Mini Prometheus. All future research documents should remain consistent with the terminology established here unless a formal revision is approved through the project's research review process.


# 2. Definition of MiniFlyWire

MiniFlyWire is a computational laboratory for experimental artificial cognition.

It is designed to provide a controlled, observable, and reproducible environment in which computational mechanisms of cognition can be proposed, implemented, measured, compared, and experimentally evaluated.

MiniFlyWire is not intended to be a biologically accurate brain simulator, nor is it intended to be a production artificial intelligence system.

Instead, it serves as an experimental platform for investigating how different computational mechanisms influence the emergence, organization, interpretation, and transfer of internal knowledge representations.

The primary purpose of MiniFlyWire is not to maximize benchmark performance, but to increase scientific understanding of artificial cognition through controlled experimentation.

Every cognitive mechanism introduced into MiniFlyWire must be supported by a clearly defined hypothesis, measurable evaluation criteria, reproducible experiments, and explicit comparisons against appropriate baseline architectures.

Within the broader Mini Prometheus ecosystem, MiniFlyWire functions as the experimental research laboratory in which cognitive theories are scientifically evaluated before they become part of larger cognitive architectures or real-world intelligent systems.


# 3. Definition of Representation

A representation is an internal computational structure that encodes information about entities, relationships, events, or processes in a form that can influence future computation.

Representations are not the external world itself. They are internal models constructed by a cognitive system to support prediction, memory, reasoning, planning, decision-making, and learning.

A representation may take many computational forms, including but not limited to vector embeddings, graphs, symbolic structures, probabilistic models, latent states, or other information-bearing structures. No single computational form is assumed to be universally correct.

Within the MiniFlyWire research program, the term "representation" refers to the functional role played by an internal structure rather than its implementation.

A computational structure qualifies as a representation only if it satisfies all of the following conditions:

1. It encodes information derived from experience or inference.
2. It influences future computation or behavior.
3. It can be experimentally observed or inferred through measurable effects.
4. It can change as a consequence of learning.

Representations are therefore treated as measurable scientific objects rather than visual artifacts or implementation details.

The central objective of MiniFlyWire is not merely to create representations, but to investigate which computational mechanisms causally produce representations that become increasingly structured, interpretable, transferable, and useful across diverse tasks.
