# DECISIONS

**Project:** Velith
**Document type:** Permanent engineering decision record. This is a *record*, not a discussion. Each entry states a decision that has already been ratified, its rationale, the alternatives that were rejected, and its consequences.
**Status of this document:** Authoritative. A ratified decision is changed only by a new dated entry that explicitly supersedes the prior one, with justification. Decisions are never edited away silently.
**Last updated:** 2026-06-20

**Naming lineage (for the record):** This program was discussed during its review phase under the working names *PrometheusLite* / *Mini Prometheus* (program) and *Noetica* (system). The ratified flagship name is **Velith**. Where earlier internal documents (`VISION.md`, the architecture/cognitive/theory papers) use the older names, they refer to this same project unless explicitly stated otherwise.

---

## How to read this record

Each decision carries:
- **ID & title**
- **Status** (Accepted / Superseded / Postponed)
- **Decision** — what was decided, stated flatly
- **Rationale** — why
- **Alternatives rejected** — what was considered and not chosen
- **Consequences** — what this commits or forecloses

The narrative sections requested (vision, vertical, philosophy, migration, non-goals, postponements) are expressed *through* these decisions, not separately, so there is one source of truth and no drift between a summary and the record.

---

## Decision index

| ID | Title | Status |
|---|---|---|
| D1 | Project vision and research mission | Accepted |
| D2 | Verification-first philosophy | Accepted |
| D3 | Deterministic verification is mandatory at V0.1 | Accepted |
| D4 | First engineering vertical: repository-level software (SWE) | Accepted |
| D5 | Migration ladder toward manufacturing intelligence | Accepted |
| D6 | The core falsifiable experiment (the compounding hypothesis) | Accepted |
| D7 | Differential experiment design (grounding isolated as the causal variable) | Accepted |
| D8 | Methodological conditions for the experiment | Accepted |
| D9 | State-centric architecture; LLMs are components, not the architecture | Accepted |
| D10 | Free-energy theoretical framework is a research hypothesis, not a build constraint | Accepted |
| D11 | MiniNoetica is a separate, completed reference project — not a dependency | Accepted |
| D12 | M0–M10 implementation roadmap ratified; implementation has priority | Accepted |
| D13 | Engineering environment baseline | Accepted |
| D14 | Non-goals (explicitly out of scope) | Accepted |
| D15 | Decisions intentionally postponed | Postponed (by design) |
| D16 | M1 ratification clarifications (Q1–Q7) | Accepted |
| D17 | Verdict taxonomy unchanged; flakiness is metadata (M2) | Accepted |
| D18 | Determinism Levels; M2 targets Level 4 (M2) | Accepted |
| D19 | Two-phase hardened sandbox; isolation mechanism (M2) | Accepted |
| D20 | M2 explicit out-of-scope set (M2) | Accepted |
| D21 | `flaky` is provenance, not identity (M2) | Accepted |

---

## D1 — Project vision and research mission

**Status:** Accepted.

**Decision.** Velith's long-term objective is to build AI systems that **learn, reason, verify, remember, improve, and make decisions in grounded environments**. Its flagship instantiation is a **grounded, verification-first engineering intelligence** whose decade-scale north star is **manufacturing intelligence** — turning product intent into verified, manufacturable designs. The near-term substrate is a *General Engineering Intelligence* loop, not the manufacturing endpoint itself.

**Rationale.** The mission is one process: minimize the description length of *grounded* engineering experience over a hierarchical model, under a finite budget, against an immutable verifier, by composing typed transformations over one shared state. Manufacturing is named as the hardest, latest milestone precisely because its verification economics are the worst; a system that reaches it has demonstrably solved the loop rather than avoided it.

**Alternatives rejected.** Framing Velith as a chatbot, an agent framework, a CAD generator, or an LLM wrapper. All were rejected as identity-defeating (see D14).

**Consequences.** Every decision below is judged against whether it increases the probability of a grounded, compounding engineering intelligence — not against short-term capability or demo value. Full vision text lives in `VISION.md`; this record governs the decisions that implement it.

---

## D2 — Verification-first philosophy

**Status:** Accepted.

**Decision.** Truth in Velith is **exogenous and grounded**. No claim is trusted because a model produced it fluently; a claim is true only when an external verifier admits it. Verification is the load-bearing principle of the system, not a feature bolted on.

**Rationale.** A confidently wrong answer is the primary failure mode of generative systems. Grounding is also what makes the program *falsifiable* (the model can be wrong against external evidence) and what prevents the system from "improving" by corrupting its own success criterion. The verifier, and the human-oversight boundary, are fixed points outside the domain of any self-modification.

**Alternatives rejected.** Treating LLM self-assessment or verbalized confidence as a proxy for correctness; treating verification as a single trusted oracle that is always cheap and always right.

**Consequences.** Calibration, learning, and self-improvement are all defined *relative to* the verifier. The experiment (D6) is specifically designed to test whether external verification — not self-confidence — is what produces competence.

---

## D3 — Deterministic verification is mandatory at V0.1

**Status:** Accepted.

**Decision.** The V0.1 verifier must be **deterministic and have zero model-gap**: a result is computed by `compile + run hidden tests + static analysis`, with no model in the loop judging correctness. The verdict must be bit-for-bit reproducible given identical inputs, seed, and environment.

**Rationale.** The experiment that justifies the entire program (D6) measures whether *grounded* experience compounds. That measurement is only interpretable if the grounding signal is exact. Any model-based judgment in the verifier reintroduces the very model-gap the program exists to eliminate, and would make a failure-to-compound uninterpretable (architecture flaw, or just verifier noise?). In software, the verifier and the ground truth are the *same object* — a passing hidden test suite *is* correctness for the specified behavior, not a model of it.

**Alternatives rejected.** LLM-as-judge verification (this is the explicit anti-pattern; see D11). Approximate/model-based verification (FEA, SPICE) as the V0.1 ground truth — deferred to later rungs of the migration ladder where the model-gap is introduced *deliberately and after* the loop is proven (D5).

**Consequences.** Model-based judgment is permitted in the experiment **only** as the dedicated anti-grounding control arm (A3), whose entire purpose is to be beaten by deterministic verification. It is never the verifier itself.

---

## D4 — First engineering vertical: repository-level software (SWE)

**Status:** Accepted.

**Decision.** The first vertical is **repository-level software engineering**, evaluated against SWE-bench-Verified-style task sets with hidden, held-out test suites. Algorithmic problem sets (contamination-controlled, post-cutoff) are used **only as a warm-up harness**, never as the ratifying benchmark.

**Rationale.** Software uniquely satisfies the four properties the V0.1 experiment requires simultaneously: (1) zero model-gap grounding (D3); (2) an external, un-authored, held-out benchmark, defeating Goodhart; (3) high episode throughput at low cost, needed to observe a trend; (4) unsaturated headroom at the repository level, so the loop's lift is visible above noise. No other candidate vertical satisfies all four at V0.1.

**Alternatives rejected.**
- *Algorithmic-only (HumanEval/MBPP):* saturated → no headroom → compounding cannot be observed. Demoted to warm-up.
- *Electronics/PCB:* strong long-term fit, but no public held-out benchmark (re-introduces self-authoring) and functional verification (SPICE) is model-approximate. Designated the **natural second** vertical (D5), not the first.
- *HDL/firmware:* rigorous (formal/exhaustive) verification but immature benchmarks; deferred.
- *Mechanical/FEA and full manufacturing:* slow, brittle, and — fatally — the ground truth is itself approximate and partial. This is the *destination*, not the starting line. Using it first would confound the compounding signal with verifier intractability.

**Consequences.** V0.1 tests **loop mechanics, not domain knowledge**. Low *immediate* manufacturing transfer is accepted in exchange for maximum experimental cleanliness; transfer is recovered structurally via D5.

---

## D5 — Migration ladder toward manufacturing intelligence

**Status:** Accepted.

**Decision.** Generality is reached by a pre-committed migration ladder, so "software-first" can never quietly become "software-only":

1. **Software (repo-level SWE)** — prove the loop compounds; zero model-gap; external benchmark.
2. **Electronics / PCB** — first *deliberate* model-gap (approximate SPICE ground truth) and a literally manufacturable artifact (Gerbers); first internally-authored benchmark under held-out discipline.
3. **HDL / firmware** — exhaustive formal verification plus first contact with physical/timing constraints.
4. **Mechanical / FEA → manufacturing** — the north star, attempted only after the loop has survived progressively widening model-gaps.

**Rationale.** This sequence traces the verification-first thesis from *zero model-gap* to *full physical approximation* — precisely the gradient a manufacturing intelligence must climb. Starting at the bottom of that gradient is the disciplined path to the goal, not an avoidance of it. The architecture (D9) is kept domain-agnostic so each new vertical is a registration, not a rewrite.

**Alternatives rejected.** Choosing a high-transfer-but-unmeasurable vertical first (couples the hypothesis test to domain difficulty and confounds the experiment).

**Consequences.** Transfer is structural, not abandoned. Each rung reuses the measurement discipline established in D6–D8.

---

## D6 — The core falsifiable experiment (the compounding hypothesis)

**Status:** Accepted.

**Decision.** The single question V0.1 exists to answer: *Can a grounded, verification-first engineering agent measurably improve its held-out performance through verified experience?*

- **H1:** for a fixed base model and fixed per-task budget, an agent retaining **verification-filtered** experience achieves strictly higher **held-out** pass-rate after N grounded episodes than (a) the same agent at episode 0, **and** (b) control agents accumulating experience *without* the verification filter; and held-out pass-rate increases monotonically in expectation with accumulated verified experience.
- **H0:** verification-filtered experience produces no greater held-out improvement than unfiltered experience or no experience; any apparent gain is attributable to retrieval of near-duplicates, base-model variance, or benchmark noise.

**Rationale.** Every later layer (causal models, self-improvement, the cognitive plane) is *premised on compounding being real*. This experiment tests that single load-bearing assumption at the smallest, cheapest scale, in the vertical where the verifier has zero model-gap so a negative result is unambiguous. A negative result is the highest-value output: it blocks years of building on unverified ground.

**Alternatives rejected.** An absolute before/after design with no ungrounded control — rejected because it can be passed by ordinary retrieval (RAG) and would prove nothing about grounding (see D7).

**Consequences.** A negative result does not kill the project; it falsifies *this retention design* and forces re-derivation before further architecture is built. Kill criteria are pre-committed in the protocol (`RESEARCH.md`/protocol, to be recorded when written), not negotiated after seeing results.

---

## D7 — Differential experiment design (grounding isolated as the causal variable)

**Status:** Accepted.

**Decision.** The experiment is **differential**, with the experience-retention policy as the single manipulated variable, across arms:
- **A0 — Cold:** no memory (baseline + variance).
- **A1 — Unfiltered memory:** all attempts retained regardless of correctness (the RAG/null control).
- **A2 — Verified memory (treatment):** only verification-passing solutions and *verified* failure signatures retained.
- **A3 — Anti-grounding (falsification arm):** retains solutions the model *believed* correct, without running the verifier (self-confidence control).
- **A4 — Verified-success-only (ablation):** isolates the contribution of grounded *failure* learning.

The decisive criterion is **A2 strictly beats A1**. A2≈A1 is the RAG verdict (grounding adds nothing over retrieval). A2≈A3 is the self-assessment verdict (external verification adds nothing over self-confidence) and would put the entire verification-first premise (D2) in question.

**Rationale.** "Does experience help" has a cheap, useless, true answer (retrieval). The real claim is that the *verification signal* converts experience into competence. Only a control that holds retrieval identical and varies *only the write-filter* isolates grounding as the cause. The A3 arm — built to disprove our own premise — is the design's strongest credibility signal.

**Alternatives rejected.** Omitting A1 (cannot attribute improvement to grounding); omitting A3 (cannot show external verification beats self-confidence).

**Consequences.** A1 and A2 must share the *identical* retriever, embedder, and top-k; the only legal difference is the write-filter. If their retrievers ever differ, the experiment is void. This invariant is enforced as a permanent test (roadmap M6/M7).

---

## D8 — Methodological conditions for the experiment

**Status:** Accepted.

**Decision.** The experiment runs under these conditions:
1. **Fixed, deliberately non-saturating base model** — a weaker/cheaper model with headroom, measuring the *delta* the loop contributes, not absolute score. A frontier model at ceiling would mask the effect.
2. **Pre-registration freeze** of N, seed count, minimum effect size, exact arm contrasts, and metrics, hash-tagged *before* the first real Stage-1 run.
3. **Mechanically-enforced held-out lock** — held-out tasks can never enter any arm's memory; enforced in code (hash-checked exclusion), not by discipline.
4. **Frozen, checkpointed held-out evaluation** — measurement is on the *frozen* agent with memory read-only, so memorization cannot counterfeit learning.
5. **Staged spending** — Stage 1 (A0 vs A2) is a cheap go/no-go; Stage 2 (add A1, A3) is the decisive run; ablation (A4) and second-model replication follow. A Stage-1 win is explicitly *necessary-but-not-sufficient* and may never be mis-sold as confirmation.
6. **Effect size reported, not just significance** — with few seeds, magnitude and seed-spread are the primary evidence; an underpowered or noisy positive is treated as uninterpretable, not as a weak win.

**Rationale.** These are the conditions that make the result credible to a serious reviewer and that prevent the experiment from confirming itself. They also install the *measurement method* every later rung of the migration ladder (D5) will reuse.

**Consequences.** The harness is built to run all arms from the start (staging is a scheduling/spend decision, not an architectural one). Pre-registration is written against a *running* harness, never an imagined one (gate at roadmap M9).

---

## D9 — State-centric architecture; LLMs are components, not the architecture

**Status:** Accepted.

**Decision.** Velith is **state-centric**, not control-flow-centric. A persistent, typed, provenance-tracked representation of the artifact is the substrate; generators, verifiers, planners, and learners are typed transformations over that shared state. **LLMs are one mechanism among several**, never the architecture itself. Cognition (when added) is a **control plane over shared state**, never a central homunculus.

**Rationale.** Intelligence does not emerge from orchestrating stateless text-passing calls; it requires persistent state, grounding, and a loop that compounds. The state-centric inversion is what turns "a script that calls an LLM" into an operating system whose identity does not depend on any single model or vendor.

**Alternatives rejected.** Agent-graph-as-architecture; LLM-as-mind; a central reasoning engine that everything serves.

**Consequences.** Provenance and observability are first-class, non-negotiable deliverables from the first commit. The full layered design (L1–L8) and cognitive plane (C0–C10) are conceptual maps; the *code* follows a minimal V0.1 decomposition (roadmap M0–M10), with deeper layers added only after D6 is validated.

---

## D10 — Free-energy theoretical framework is a research hypothesis, not a build constraint

**Status:** Accepted.

**Decision.** The active-inference / expected-free-energy framework (in the theoretical-foundations paper) is retained as a **decade-scale falsifiable research hypothesis and a conceptual filter**. It is **forbidden from constraining any V0.1 mechanism**. No V0.1 line of code depends on the variational machinery being correct.

**Rationale.** The framework is elegant and gives the program long-term coherence, but exact free-energy minimization over a hybrid symbolic-continuous hierarchy is intractable; what gets built are approximations that stand on their own as ordinary engineering mechanisms (MDL compression + Bayesian updating + a compute budget). Until a running spike exists, the formalism drives zero implementation decisions and must not be allowed to shape the codebase prematurely.

**Alternatives rejected.** Treating the free-energy objective as a build specification (would risk years fitting engineering into a possibly-wrong abstraction); discarding it entirely (loses long-term coherence and the decade-scale falsifiable claim).

**Consequences.** The framework lives in `VISION.md`/`RESEARCH.md` as theory. The compounding experiment (D6) *is* its small-scale falsifiable test. Both the coherence the theory provides and the unblocked building the program needs are preserved.

---

## D11 — MiniNoetica is a separate, completed reference project — not a dependency

**Status:** Accepted.

**Decision.** MiniNoetica remains a **completed learning project and read-only reference repository**. It is **not a dependency of Velith** and shares no import paths with it. Velith is a new repository, side by side with MiniNoetica on disk, with zero coupling.

**Rationale.** MiniNoetica is an *education / learning-intelligence* system (it models a *student's* knowledge — theory-of-mind, the highest-risk component Velith explicitly defers). Velith is an *engineering-intelligence* system that improves *its own* verified competence. Different domain, different subject, different architecture. Critically, MiniNoetica's `judge.py` is an **LLM-as-judge**, which is the precise anti-pattern Velith's deterministic verification (D3) exists to eliminate; carrying it in would silently reintroduce the model-gap.

The value MiniNoetica delivered was the **engineering experience and reusable implementation patterns** it produced, not its educational domain. It succeeded as a 20-day learning vehicle: the deliverable of a learning sprint is the engineer it produces, not the repo it leaves behind.

**Patterns harvested (copied and adapted, never imported):**
- The LLM-call *shape* (single owner for model calls) — extended in Velith with routing + a hard cost guard.
- The episode-to-JSONL *pattern* — seeds Velith's episode store; the schema changes (engineering provenance, not student fields), the technique transfers.
- Test discipline (mocked-model integration tests, contract-between-components thinking).
- Logging pattern.

**Left behind explicitly:** all `phase2_memory/*` (student-modeling), `judge.py` (LLM-as-judge anti-pattern), and `agent_zero/step1–9` (learning archive).

**Alternatives rejected.** Extending MiniNoetica into Velith, or wiring the repos together. Rejected as negative value: dragging education-domain memory semantics into an engineering verification experiment costs more than a clean rebuild, and the boundary would erode.

**Consequences.** If a Velith file ever imports from MiniNoetica, that is the signal the boundary has been crossed and must be reverted. Pattern reuse is done by reading the old file and retyping an adapted version, not by cross-repo imports.

---

## D12 — M0–M10 implementation roadmap ratified; implementation has priority

**Status:** Accepted.

**Decision.** The M0–M10 milestone roadmap is ratified **as written**. From this point, implementation has priority over further architectural discussion unless implementation itself reveals a flaw. The roadmap delivers, in order: a runnable skeleton (M0); **one reproducible propose→verify→log episode (M1)**; a deterministic hardened verifier (M2); a provenance-complete episode store (M3); dataset loader + mechanically-enforced held-out lock (M4); batch runner + cold baseline A0 (M5); shared retrieval substrate (M6); A1/A2 write-filter policies (M7); frozen checkpointed evaluation (M8); the Stage-1 orchestrator + full A0/A2 run (M9); and Stage-1 statistics + go/no-go report (M10).

**Rationale.** The program had accumulated four conceptual frameworks and zero code; the marginal framework had negative value. The discipline now is validation-driven engineering: every milestone produces a *running system*, no milestone exists solely to produce documentation, and the first milestone ends at a real, logged, reproducible episode.

**Alternatives rejected.** Producing a fifth conceptual framework; designing all 19 module interfaces up front (abstraction-too-early — only the 2–3 interfaces the V0.1 loop exercises are built; the rest are named placeholders).

**Consequences.** Stage 2 (A1/A3), ablations (A4), and replication are specified in the same format *only after* M10's go/no-go verdict is in hand — deferred, not pre-built, per D8's staged-spending discipline.

---

## D13 — Engineering environment baseline

**Status:** Accepted.

**Decision.** Velith is built on: **WSL2 + Ubuntu** (Linux build/runtime), **Docker** (containerized deterministic verifier), **Python** (3.12 target for the Velith repo), **Git**, and **Ollama** (local model serving). The deterministic verifier (D3, roadmap M2) runs inside a Linux container for bit-for-bit reproducibility.

**Rationale.** M2's entire premise is reproducible verdicts; Linux containers make that tractable in a way native Windows does not. WSL2 + Docker + Ubuntu are verified present, removing the environment as a blocker before M0.

**Alternatives rejected.** Native-Windows build (reproducibility of the verifier would be materially harder). Note: the MiniNoetica reference repo runs on Windows + Python 3.10; Velith does not inherit that environment.

**Consequences.** M0's setup steps target WSL2/Ubuntu + Docker; a fresh clone must go green in that environment with one documented command.

---

## D14 — Non-goals (explicitly out of scope)

**Status:** Accepted.

**Decision.** The following are out of scope for Velith's identity. Moving any of them in requires a new superseding entry in this record.

| Non-goal | Why |
|---|---|
| Training foundation models | Consume frontier/open-weight models; small task models (embeddings, rerankers, distilled experts) are in scope when justified |
| Building physics engines, CAD kernels, or solvers | Wrap, never rebuild |
| Multi-discipline breadth on day one | Generality is earned by deepening one vertical, via the D5 ladder |
| Chatbot / general-assistant framing | Velith is a reasoning-and-verification system that *uses* LLMs |
| A homunculus / central reasoning engine | Cognition is a control plane over shared state (D9) |
| Premature scale infrastructure (Kubernetes, microservices, multi-tenant, web-scale) | Single-machine discipline for years |
| Verification-as-free-oracle | Any design assuming cheap, perfect ground truth is rejected by D2/D3 |
| Fixed benchmark optimized as the goal | Invites Goodharting; held-out, generalization-tested measurement only (D8) |
| LLM-as-judge as the verifier | The deterministic-verification anti-pattern (D3, D11) |

**Consequences.** These boundaries are load-bearing. They are what keep Velith from collapsing into "another agent framework."

---

## D15 — Decisions intentionally postponed

**Status:** Postponed by design.

**Decision.** The following are deliberately **not** decided now. They are postponed until the experiment (D6) validates the compounding premise, because deciding them earlier would architect for capabilities the program has not yet earned the right to build.

- **Cognitive control plane (C0–C10)** — global workspace, executive, meta-cognition, etc. Named as conceptual map; not built in V0.1.
- **Causal / structural model (L3 causal)** — postponed until after compounding is validated.
- **Self-model and social/theory-of-mind model (C2)** — highest research risk; postponed.
- **Scientific-discovery loop (C5)** — postponed.
- **Self-improvement loops (C9)** — postponed; when built, the fixed-verifier and human-oversight boundary are immutable from day one.
- **Calibration mechanism (I6)** — calibration is a *measured property we will try to force*, with a concrete method to be specified before it is claimed; not asserted as a guaranteed invariant yet.
- **Second vertical (electronics, D5 rung 2)** — postponed until the software loop is proven.
- **Any agent-framework dependency for the core spine** — the V0.1 orchestration loop is plain, testable code; a framework is adopted only if a concrete need appears.
- **Free-energy computation in code** — postponed indefinitely; theory only (D10).
- **Stage 2 / ablation / replication milestone details** — specified only after M10's verdict (D12).

**Rationale.** Postponement is a positive engineering act here: it prevents building cathedrals on an unverified foundation. Each postponed item is gated on a specific validation result, so the program knows exactly what earns the right to decide it.

**Consequences.** This list is the explicit boundary between "decided" and "deferred." An attempt to build any postponed item before its gate is a deviation that must be recorded here with justification.

---

## D16 — M1 ratification clarifications (Q1–Q7)

**Status:** Accepted (clarifications). **Date:** 2026-06-22.
**Scope:** These entries clarify the application of existing decisions (D2, D3, D4, D6, D8, D9, D12, D13) to milestone M1. None supersedes or alters D1–D15; each is a clarification, not a redesign. Where a clarification touches the M0–M10 roadmap acceptance text ratified under D12, it refines wording without changing the ratified substance.

### D16.1 — M1 reproducibility is scoped to the verify→log path
The roadmap's M1 acceptance ("same seed + temperature 0 → same verdict") is clarified: M1's **blocking** reproducibility criterion is that, **given a recorded proposal (fixed patch), the verify→log path produces the same verdict and the same content hash**. Proposal-level model determinism (seed + temperature 0) is attempted and recorded but is **not** a blocking criterion, because local model generation cannot be honestly guaranteed bit-identical across runs/hardware. This *locates determinism in the verifier*, consistent with and strengthening D3. (Clarifies D12; does not alter D3.)

### D16.2 — M1 orchestration runs in-container; Ollama reached via host
The M1 spike orchestrator runs **inside the container** (Python 3.12 target, D13), network-enabled, reaching the host Ollama service via `host.docker.internal` (WSL2 + Docker Desktop). The **verdict is produced in-container** (D3/M0 invariant preserved). The host Python (3.10) is never an execution target. Transient network access during the M1 run is an accepted, documented condition; isolating the test-execution step from the network is a later hardening step, not an M1 concern. (Clarifies D13.)

### D16.3 — M1 uses a minimal representative fixture task, not real SWE-bench
M1 exercises the loop with a **minimal, self-contained fixture task** of the same shape as a SWE-bench task (small repo + hidden test). Real SWE-bench Verified integration is deferred to M4. The fixture is **not a benchmark** and must never be used as the ratifying measurement (D8 held-out discipline is unaffected). (Clarifies D4/D6; does not alter D8.)

### D16.4 — M1 introduces a thin LLM adapter, not routing
M1 adds a **thin `llm/client.py` adapter** (generate + call metadata) so the proposer depends on a model capability, not on a vendor (D9). Model routing, selection policy, and the cost guard remain out of scope until M5; the adapter must not grow into a routing framework in M1. (Implements D9.)

### D16.5 — D8's non-saturating base-model condition binds from M5, not M1
The non-saturating base-model methodological condition (D8) governs the **compounding experiment (M5+)**. M1 may use any small local code-capable Ollama model that can emit diff-shaped output; the model and version are recorded in every episode for provenance and swappability. (Clarifies the scope of D8.)

### D16.6 — M1 episode persistence
Episodes persist to host `./data/episodes/` via a bind mount, gitignored, as an append-only JSONL store. The indexed/queryable store is M3. (Implementation clarification; consistent with I2/observability.)

### D16.7 — M1 verdict taxonomy and the outcome/error distinction
M1 verdict states are: `PASSED`, `FAILED`, `PATCH_APPLY_FAILED`, `NO_PATCH` (all **logged grounded outcomes**, process exit 0) and `INFRA_ERROR` (the **only** error state, non-zero exit). A test failure is a valid grounded outcome and first-class learning data, never an error. No model judges any verdict (D3). `secondary_passed` is null in M1 (populated at M2) and is not a verdict state. (Operationalizes D2/D3.)

> **Provenance note (2026-06-25):** D16 above is restored **verbatim** from commit `b8d458e` ("docs: ratify M1 engineering clarifications (D16)"), which originally recorded it. It was inadvertently removed by commit `cc4a1b4` ("docs: finalize M1 implementation contracts") and was absent from the record until this restoration. No wording was changed.

---

## D17 — M2: verdict taxonomy unchanged; flakiness is metadata

**Status:** Accepted. **Date:** 2026-06-25. **(Ratifies M2 R1.)**

**Decision.** M2 introduces no new verdict state. The closed taxonomy remains `PASSED`, `FAILED`, `PATCH_APPLY_FAILED`, `NO_PATCH`, `INFRA_ERROR` (D16.7). Test flakiness is *measurement quality*, recorded as a boolean `flaky` on the `Verdict` and persisted as episode provenance — never a verdict state.

**Rationale.** A verdict names the grounded outcome; flakiness names the trustworthiness of the measurement. Conflating them would pollute a closed outcome taxonomy with a quality signal and burden every downstream consumer.

**Alternatives rejected.** A `FLAKY` verdict state (mixes outcome and measurement quality in one field).

**Consequences.** Downstream memory policies (M5+) may consume the `flaky` provenance to down-weight or exclude unstable episodes. See D21 for the hash treatment of `flaky`.

---

## D18 — M2: Determinism Levels; M2 targets Level 4

**Status:** Accepted. **Date:** 2026-06-25. **(Ratifies M2 R2.)**

**Decision.** Verifier reproducibility is graded: **L1** same verdict ⊂ **L2** same content hash ⊂ **L3** same verifier output ⊂ **L4** same execution environment. M2 targets **Level 4** via a pinned interpreter environment (`PYTHONHASHSEED`, `TZ`, `LC_ALL`), network-isolated test execution, and the pinned base image, so L1–L3 hold structurally.

**Rationale.** M1 reached L2 incidentally (via output normalization). Pinning the environment makes reproducibility structural — which the compounding experiment (D6) requires of its grounding signal (D2/D3), strengthening D3 and D16.1.

**Alternatives rejected.** Relying on post-hoc output normalization alone (incidental and fragile).

**Consequences.** The verifier injects a fixed environment and isolates the test step; cross-machine equality follows from the pinned image and is asserted same-machine in CI.

---

## D19 — M2: two-phase hardened sandbox; isolation mechanism

**Status:** Accepted. **Date:** 2026-06-25. **(Ratifies M2 R3.)**

**Decision.** The verifier executes tests in two phases — Phase 1 network **ON** (dependency preparation), Phase 2 network **OFF** (test execution). A feasibility prototype determined that unprivileged `unshare -rn` is blocked by the Docker Desktop/WSL2 default seccomp profile, while `cap_add: SYS_ADMIN` + `unshare -n` succeeds; the latter is the **supported mechanism**. Isolation is mandatory: if the mechanism is unavailable, the verifier raises (`SandboxExecutionError` → `INFRA_ERROR`) rather than running untrusted code unisolated. The spike remains single-container.

**Rationale.** Closes the accepted M1 network-exposure risk (R3 / D16.2): untrusted generated code must not reach the network. Two phases preserve the proposal step's required network while isolating the test step.

**Alternatives rejected.** Unprivileged `unshare -rn` (blocked by seccomp, proven by prototype); a `--network none` sidecar (reintroduces a second container and a Docker-socket dependency, contradicting the single-container model).

**Consequences.** `docker-compose.yml` grants `cap_add: [SYS_ADMIN]` to the disposable verifier container; CI runs the isolation tests where the capability is available and capability-skips them (with an explicit reason) otherwise — never silently passed.

---

## D20 — M2: explicit out-of-scope set

**Status:** Accepted. **Date:** 2026-06-25. **(Ratifies M2 R4.)**

**Decision.** Property-based testing, resource profiling, streaming generation, richer proposer prompts, and git-ref provenance are out of scope for M2.

**Rationale.** M2 is verifier hardening; these are unrelated enhancements that would expand scope and risk.

**Alternatives rejected.** Folding any of these into M2 (scope creep).

**Consequences.** The M2 held-out secondary suite is explicit example-based cases; the proposer and the episode provenance fields are otherwise unchanged.

---

## D21 — M2: `flaky` is provenance, not identity (excluded from the content hash)

**Status:** Accepted. **Date:** 2026-06-25. **(Ratifies M2 R5.)**

**Decision.** The `flaky` flag is persisted in the episode but **excluded from the canonical `content_hash`**. The content hash covers reproducible *identity* only; a field belongs inside it iff it is a reproducible function of `(task, patch, environment)`. `flaky` is the observed output of a non-deterministic sampling process and may differ across re-verifications of a fixed proposal, so it is *provenance*, recorded alongside the timing fields outside the hash. `secondary_passed`, by contrast, is deterministic and therefore *identity* (inside the hash).

**Rationale.** Including `flaky` in the hash would make the Determinism Level 2 / D16.1 "same hash on re-verification" criterion unsatisfiable for the very episodes `flaky` exists to flag. Reproducible identity and full-record integrity are distinct concerns served by distinct digests.

**Alternatives rejected.** `flaky` inside the content hash (breaks D16.1 reproducibility); `flaky` left unpersisted (loses provenance needed by M5+ memory policies). Full-record tamper-evidence, if ever required, is a separate record-level digest (an M3 storage concern), never the content hash.

**Consequences.** `episodes/episode.py` adds `flaky` to `HASH_EXCLUDED_FIELDS`; a test asserts a varying `flaky` leaves the content hash unchanged.

---

## Amendment procedure

A ratified decision is changed only by appending a new dated entry that:
1. names the decision it supersedes,
2. states the implementation evidence or flaw that justifies the change, and
3. records the new decision in the same format.

Decisions are never edited in place or removed. This record is the project's memory of *why* it is shaped as it is, and that memory must remain intact for reviewers who join in year three.