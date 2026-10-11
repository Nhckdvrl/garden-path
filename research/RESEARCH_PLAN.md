# Garden Path: from transient misinterpretation to a predictive theory of revision behavior

**Scientific program v0.1 — 2026-10-12. No new model experiments have been run.** Primary working repository: this repository. Historical source: [SSN imported assets](../imports/ssn-incremental-revision/README.md). Literature understanding: [genesis atlas](../library/RESEARCH_GENESIS_ATLAS.md), [ownership table](../library/RELATED_WORK_OWNERSHIP.md).

## 0. Question, not a pre-written paper story

Temporary syntactic ambiguity is an unusually controlled setting for later evidence overturning an earlier plausible interpretation. We ask:

> **When temporary ambiguity ends, which parts of sentence meaning become reliably usable, which errors persist, and under what conditions does the model's earlier path affect *subsequent* behavior?**

We do **not** presuppose that the model held a discrete parse, stores a loser state, exhibits inhibition geometry, or shares a human cognitive architecture. An unexpectedly good model or absence of traces is just as scientifically relevant.

We deliberately start with **behavioral phenomena and rival explanations**, not SAE, latent phase transitions or more benchmark leaderboards.

## 1. Why this matters

1. Human work distinguishes rebuilding correct syntax from lingering wrong interpretation (Slattery 2013), and even asks whether the final interpretation is **globally coherent** (Ceháková & Chromý 2025).
2. LLM work establishes Garden Path comprehension difficulty (Amouyal 2025/2026), feature/circuit differences across token prediction and QA (Hanna & Mueller 2025), and ordinary structural priming (Sinclair 2022/2026).
3. Our own earlier SSN experiments E70/E82/E87/E98/E107 **already** suggest relation omission, answer versus role divergence and query-condition heterogeneity. These are not new findings to recycle.
4. The remaining high-level opportunity is a **predictive boundary law**: which grammatical relations and downstream operations are selectively impaired, not merely “some wrong relations linger”.

## 2. Two independent pilots (not a forced unified hypothesis)

### A. Relation-dependency footprint after disambiguation — primary

**RQ-A:** Does Garden Path cause merely a localized obsolete attachment, or a broader, systematically structured inability to establish/coordinate the correct dependencies of the sentence?

**Novelty bar:** Ceháková & Chromý 2025 already measured both initial and disambiguating-region comprehension; SSN E70 already measured atomic roles. Thus “late question also wrong” or “some roles omitted” is **not** sufficient. The useful addition would be a **dependency-sensitive failure topology and out-of-sample prediction** that a local error model, general hard-syntax baseline, lexical surprisal, plausibility and task prompts cannot explain.

- **H-A1 Local stale attachment:** GP errors concentrate in the old NP→V relation and specific dependent consequences. Once those relations are controlled, independently supported late facts remain intact.
- **H-A2 Global/fragmented composition:** GP increases errors in additional **unaffected** dependencies and in combining valid facts, beyond generic syntax difficulty or QA format.
- **H-A3 Task-induced report artifact:** Differences largely track polar question semantics, antecedent framing or source/entailment instructions; intact native semantic representations cannot be inferred from one probe.
- **H-A4 Mere general complexity:** GP vs cue effects vanish against length/nesting matched non-GP difficult structures, or are fully predictable from the same complexity factors.

A combination of explanations may win. We do not label any one an internal parser mechanism. See [Pilot A](PILOT_A.md).

### B. Misparse-specific structural persistence — parallel, independent

**RQ-B:** Does an *initially supported but ultimately ruled-out* syntactic analysis alter a subsequent **lexically unrelated** production decision more than ordinary exposure to the final sentence's structure does?

**Novelty bar:** Wrong-analysis priming has human precedent (van Gompel 2006), and structural priming in LMs is well established (Sinclair TACL 2022; Pucci 2026). A mere nonzero priming effect or GP vs comma difference is insufficient. Test the **GP × expected wrong-target structure interaction**, subtract punctuation and generic context effects, and verify it on unseen lexical targets.

- **H-B1 Transient wrong-analysis additional effect:** After NP/Z, the extra bias toward a *transitive* target exceeds matched ordinary priming, cue, nonambiguous and punctuation controls.
- **H-B2 Only final-structure priming:** GP and cue primes produce comparable target effects after lexical/punctuation adjustment.
- **H-B3 Surface or general-semantic alignment:** Effects disappear when prime/target lexicons, semantic coherence and exact word order are controlled.
- **H-B4 No reliable effect:** Give interval estimates and sensitivity, stop this path-specific explanation without retrofitting hidden-state work.

A standard causal LM has no hidden persistent “mind state” outside the provided token history; **priming here means a context-dependent output distribution effect**. See [Pilot B](PILOT_B.md).

## 3. Explicitly deprioritized hypotheses

- **H1 surprisal vs H2 verb bias simple logistic regression:** Ceháková & Chromý 2026 already compares these in humans; significant residual coefficients cannot identify “commitment inertia”.
- **H3 source reliability prompted editing:** SSN E80 already attempted trust/noisy source metadata and got heterogeneous, partly harmful effects. Reopen only with **actual controlled channel error rates** and explicit truth-preserving versus truth-changing edits.
- **Automatic CoT/Reasoning Garden Paths:** Thoughtology and Amouyal 2026 already measure thinking behavior; no assumed irreversible attractor. A new reasoning claim requires transfer from a replicated *behavioral* effect with stronger anchoring baselines.
- **SAE/geometry/patching search:** Not stage 1. A future white-box intervention must have a previously observed, independently replicated phenomenon and explicit distinct functional predictions.

## 4. Why the original `garden-path` repository needs a new active lane

The repository's existing G0–G33/Unring-the-Bell archives test prospective evidence exclusion, hindsight, source relevance and related work. They are **not** syntax Garden Path stimuli and must not be relabeled as such. The Oct 9 restart preserved their historical negative results and original files. New work uses `research/`, `library/` and `data/gp_behavior/` without changing historical results, frozen preregistrations or scripts.

## 5. Ordered information-gain gates, NOT a time-based checklist

**Gate 0 — Check the instrument before compute.** Final syntactic analysis, source entailment and role probes are independently auditable; enough grammatical NP/Z and MV/RR pairs exist. If not, repair the measurement or use released stimuli, **not new mechanism work**.

**Gate 1 — Reproduce an interpretable behavioral gap.** With identical source-grounded target semantics, GP/control paired items exhibit a meaningful difference beyond mapping, question polarity and overall model weakness. Use released items first and cross-check SSN E52/E82/E87.

**Gate 2A — Separate failure profiles.** Estimate obsolete relation, correct late relation, independent relation and compositional/bridge task performance on independent runs. Test within-item role/dependency contrasts, not a new average accuracy score.

**Gate 2B — Test misparse-specific priming.** Validate target task first; verify baseline structural priming exists; then estimate interaction over fully matched GP/cue/nonambiguity conditions. Keep target lexically disjoint; don't prefilter by correct QA.

**Gate 3 — Strong falsification.** On a held-out material set, test what the leading profile predicted, including non-GP difficult structures, plausible and implausible words, and independent model family. If only one task wording works, downgrade the claim.

**Gate 4 — Explain or abandon.** If one stable, important, broadly predictive failure pattern survives, choose among additional cognitive/computational tests. If neither pilot yields new explanatory leverage, revise the scientific question; no huge grid to rescue an attractive narrative.

## 6. Minimum publishable contribution, and non-goals

A paper would require at least one important *new* regularity with predeclared opposite predictions for established alternatives, an auditable source-grounded semantic outcome, robustness outside discovery items, and honest ownership relative to 2025–2026 prior works. Mechanistic diagrams, cross-model averaging, unusually high n or a method artifact are **not** substitutes.

Success might be: a concise account predicting *where GP-induced errors propagate* and a replicated functional test that separates competing accounts. A null may constrain some widely used story without itself justifying a full paper. We do not assume a particular venue, title, or mechanism in advance.

## 7. Current evidence and status

- **Imported existing evidence only**; no new GP model runs, annotation calls, GPU use or study results as of this document.
- Existing raw archives from SSN may live only on old external filesystem; inspect hashes/availability before designing any claimed reproduction.
- Current action: validate released datasets and probes, then the two small behavioral pilots, not retrain LMs or build SAEs.
- Read [measurement protocol](MEASUREMENT_PROTOCOL.md), [Pilot A](PILOT_A.md), [Pilot B](PILOT_B.md), [decision gates](DECISIONS.md) and [SSN import boundaries](../imports/ssn-incremental-revision/README.md) in that order.
