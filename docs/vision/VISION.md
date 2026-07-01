# VISION

**Program:** PrometheusLite
**System:** Noetica
**Document status:** Founding vision. Source of truth for *why* and *toward what*. Superseded only by explicit, justified amendment recorded in `DECISIONS.md`.
**Scope of this document:** Purpose, mission, principles, and the definition of success. **Not** a README, an architecture, a roadmap, or an implementation plan. Those live in their own documents and must remain consistent with this one.

> One sentence. PrometheusLite exists to build a verification-first engineering intelligence — Noetica — that models the world and itself, learns from grounded experience, and compounds in competence over a decade, with the eventual capability to turn product intent into manufacturable physical designs.

---

## 1. Why this project exists

Engineering knowledge today does not accumulate inside our tools. A CAD kernel does not get better at design because a thousand engineers used it. A simulator does not learn which of its predictions were wrong. A language model can describe a bracket but cannot tell you, with calibrated confidence, whether the bracket it described will survive its load — and it does not remember the answer once it finds out.

The result is a structural gap: we have powerful *generators* (LLMs, parametric CAD, solvers) and powerful *checkers* (compilers, FEA, DRC), but no system that closes the loop between them, holds persistent state about the artifact being designed, reasons about its own reliability, and turns verified experience into durable, compounding competence.

PrometheusLite exists to close that loop. It is a long-term research program, not a product sprint. Its premise is that the path to real engineering intelligence is not a larger model but a **stateful, grounded, self-improving system** in which generative models are one component among several, never the architecture itself.

This is a flagship research program. It is explicitly *not* another agent framework, chatbot, CAD generator, or LLM wrapper. If a decision would make it indistinguishable from those, the decision is wrong by definition.

---

## 2. The problems in today's engineering and manufacturing systems

These are the specific failures the program is organized to attack. Each is a research target, not a complaint.

1. **No persistent state.** The artifact under design exists implicitly in prompts and scattered files. There is no single, queryable, provenance-tracked representation of "the thing." Without it, there is nothing for intelligence to be *about*.
2. **No grounding.** Generated claims are trusted by fluency, not by evidence. A confidently wrong quantitative answer is worse than no answer, yet most systems have no exogenous, immutable notion of what counts as true.
3. **No compounding.** Experience is logged, not learned from. Retrieval over past episodes is not improved competence. A system that does not get better at the task has no research moat and no path to generality.
4. **No causal model.** Correlation via a language model cannot answer "changing X changes Y *because* Z." Engineering is causal and breaks under distribution shift when treated as pattern-matching.
5. **No principled uncertainty.** "Verified vs. flagged as a guess" is a boolean where a calibrated distribution is required. Without epistemic/aleatoric separation and calibration, a system cannot decide when to gather more information.
6. **No meta-reasoning.** No policy governs how much to think, which model to call, when to simulate, and when to stop — producing either uniform under-thinking (cheap and wrong) or uniform over-thinking (correct and bankrupt).
7. **Verification treated as a free oracle.** Real engineering verification is approximate, partial, and expensive — most of all in physical and manufacturing domains. Treating it as a single trusted checker is the assumption that fails exactly where the ambition is aimed.
8. **The human left outside the loop.** The richest source of tacit engineering ground truth — the human collaborator — is modeled as an operator, not as a first-class oracle and overseer.

A system that solves only generation has solved the easy half. The hard half is framing the problem, deciding what to verify, defining "good," and learning from the answer. That hard half is the program.

---

## 3. The future we are trying to create

A future in which an engineering intelligence can take a high-level statement of *intent* — a function to be served, a set of constraints to be honored — and reason it down to a design that is **verified, explained, and manufacturable**, while honestly representing what it does not yet know.

In that future, Noetica:

- holds a persistent, multi-fidelity model of the artifact and its environment, and of *itself* and the *human* it collaborates with;
- never asserts a quantitative result it has not grounded against a real check or a faithful simulator;
- treats verification as a cost-aware decision under uncertainty, not as a free oracle;
- gets measurably better at its domain over time, because every grounded episode updates skills, concepts, and predictive models;
- proposes its own questions where the world is *learnably* uncertain, rather than only answering ours;
- improves how it designs without ever being able to modify how its success is judged or how it is overseen.

The ultimate proving ground is **physical manufacturing**: transforming product intent into designs that can actually be built. We name this as the decade's north star precisely because it is the hardest — its verification is approximate and expensive — and a system that reaches it has demonstrably solved the problems above rather than avoided them.

---

## 4. The research mission

> Build a bounded, hierarchical, compositional system that minimizes the expected description length of its **grounded** engineering experience — and demonstrate that, under faithful grounding and adequate budget, its grounded competence compounds.

Restated for the program:

- **Model** the world, the artifact, the self, and the collaborator.
- **Ground** every claim in exogenous, immutable evidence.
- **Reason** causally and plan as inference, not as retrieval.
- **Quantify** uncertainty and act to reduce the uncertainty that matters.
- **Learn** continually, compressing experience into reusable competence.
- **Discover** new engineering principles through closed experimental loops.
- **Improve** safely, behind a fixed verifier and human-oversight boundary.

This mission is **falsifiable** (see §8), which is what makes it a research program rather than an aspiration.

---

## 5. Core principles

These constrain every future decision. A proposal that violates one is rejected or must amend this document with justification.

1. **Verification-first.** A wrong answer delivered confidently is the primary failure mode. Truth is grounded in external evidence, never in the system's own fluency.
2. **State-centric, not control-flow-centric.** A persistent, provenance-tracked representation of the artifact is the substrate. Generators, solvers, planners, and verifiers are transformations over that shared state — not the architecture itself.
3. **LLMs are components, never the mind.** Frontier models are powerful priors and inference engines used as one mechanism among several. The system's identity does not depend on any single model or vendor.
4. **Generality comes from architecture and depth, not from breadth.** We design full interfaces now and add depth on a schedule. We enter through one vertical chosen for verification economics, prove the substrate there, and extend toward harder domains — so the cheap system we can build does not foreclose the general system we are aiming at.
5. **Bounded rationality is first-class.** Computation is itself a costly act. The system reasons about how much to think, which model to call, and when to stop.
6. **Grounding and oversight are immutable.** The system may improve how it designs; it may never modify how its success is judged or how it is overseen. This boundary is the core safety guarantee, not a later add-on.
7. **Provenance and observability are non-negotiable.** Every belief carries its derivation. If we cannot answer "why did it do that?", the system is a toy regardless of capability.
8. **Compounding is the test.** A system that accumulates experience without improving at the task has failed, however impressive any single output appears.
9. **Wrap, don't rebuild.** We do not build physics engines, CAD kernels, solvers, or foundation models. The novelty budget is spent on the loop that orchestrates, grounds, learns, and compounds.
10. **Honesty over impressiveness.** The program optimizes for being *correct over a decade*, not for demonstrations. Hidden assumptions are surfaced; failure conditions are stated.

---

## 6. Long-term research goals (decade horizon)

Stated as research questions the program is organized to answer, not as features to ship.

- **Grounded representation.** Can a single, typed, provenance-tracked world/design model serve as the substrate that every other capability reads and writes — across more than one engineering discipline?
- **Compounding competence.** Can verified experience be converted into durable improvement — skills, concepts, calibrated models — such that grounded accuracy per unit compute rises over time?
- **Causal engineering reasoning.** Can the system maintain interventional, not merely associational, models of design-variable-to-outcome relationships that survive distribution shift?
- **Calibrated uncertainty.** Can stated confidence be forced to track grounded accuracy, with epistemic and aleatoric uncertainty separated and acted upon?
- **Resource-rational meta-control.** Can the system learn — rather than have hand-tuned — its own policy for allocating compute, fidelity, and effort?
- **Scientific discovery.** Can it close the loop from anomaly to hypothesis to experiment to revised model, adding *new* engineering principles rather than only applying known ones?
- **Provably bounded self-improvement.** Can the system improve its own methods while a formal guarantee holds that it cannot circumvent its verifier or its human-oversight boundary?
- **Manufacturability.** Can intent be reasoned down to designs that are actually buildable, with the system honestly representing the residual uncertainty of approximate physical verification?

The honest expectation: the fully general, multi-discipline manufacturing intelligence is a funded-lab endeavor. The realistic decade target for a disciplined program is a **deep, self-improving engineering intelligence in one (or few) domains, on a domain-agnostic substrate that sits on the path toward — not a dead-end branch away from — that endpoint.** That distinction is the entire value of the program's discipline.

---

## 7. Explicitly out of scope

Naming what we will *not* do is as load-bearing as naming what we will.

- **Training foundation models.** We consume frontier and open-weight models; we do not pretrain our own. (Small task models — embeddings, rerankers, distilled experts — are in scope when justified.)
- **Building physics engines, CAD kernels, or solvers.** These are wrapped, never rebuilt.
- **Multi-discipline breadth on day one.** Generality is earned by deepening one vertical, not by spreading thin across many.
- **Chatbot or general-assistant framing.** Noetica is a reasoning-and-verification system that happens to use language models, not a conversational product.
- **A homunculus.** No single central reasoning engine that does "the real thinking" while everything serves it. Cognition is a control plane over shared state.
- **Premature scale infrastructure.** No web-scale, multi-tenant, or distributed-systems engineering until reality demands it. Single-machine discipline for years.
- **Treating verification as a free oracle.** Any design that assumes cheap, perfect ground truth — especially in physical domains — is out of scope by principle.
- **Optimizing a fixed benchmark as the goal.** Static, hand-authored metrics invite Goodharting and a false sense of progress.

Items here are out of scope *for the program's identity*, not necessarily forever; moving one in requires an amendment recorded in `DECISIONS.md`.

---

## 8. Definition of success

Success is defined at three increasing levels of ambition. The program is a success if it reaches Level 2 with a credible, demonstrated trajectory toward Level 3.

**Level 1 — Grounded loop (the floor).** Noetica takes a real task in its chosen vertical and returns a *verified* result with full provenance, calibrated uncertainty, and a known compute cost. Every quantitative claim traces to a real check. Nothing is trusted on fluency alone.

**Level 2 — Compounding intelligence (the real prize).** Across a stream of grounded episodes, the system's grounded competence *measurably improves* — its pass rate on held-out, generalization-tested tasks trends up over months, driven by learned skills, concepts, and calibrated models rather than by larger prompts. It reasons about its own reliability, decides when to stop, recovers from failure, and at least one real engineer finds it genuinely useful. This is the level at which PrometheusLite becomes a defensible research artifact.

**Level 3 — Manufacturing intelligence (the north star).** The system reasons from product intent to designs that are verified and manufacturable in a physical domain, honestly bounding the uncertainty of approximate physical verification, on a substrate that has already proven domain-agnostic.

### The falsifiable commitment

> If the program's premise is correct, then across a stream of grounded engineering episodes the **verification-measured description length of the system's experience decreases monotonically in expectation** — equivalently, grounded predictive accuracy per unit compute rises. If, under faithful grounding and an adequate budget, the system accumulates experience *without* compounding competence, the premise is **wrong**, and the architecture must be replaced, not patched.

This single measurable commitment is what makes PrometheusLite a scientific program. We will know if we are failing, and we agree in advance what failing means.

---

## 9. How this document governs

- This document defines *why* and *toward what*. It does not prescribe *how*.
- `ARCHITECTURE.md`, `ROADMAP.md`, and the research blueprints must remain consistent with the principles in §5 and the out-of-scope boundaries in §7.
- Any decision that contradicts this document is not made silently. The conflict is named, alternatives are weighed, and the resolution is recorded in `DECISIONS.md` — amending this vision only with explicit, written justification.
- The vision is allowed to change. It is not allowed to change *quietly*.