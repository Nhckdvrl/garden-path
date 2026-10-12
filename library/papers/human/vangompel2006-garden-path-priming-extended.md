# van Gompel, Pickering, Pearson & Jacob 2006 — wrong-analysis priming as a diagnostic

**JML 55(3):335–362**, DOI 10.1016/j.jml.2006.06.004. [Publisher](https://doi.org/10.1016/j.jml.2006.06.004), [author-uploaded article text](https://www.researchgate.net/publication/222659936_The_activation_of_inappropriate_analyses_in_garden-path_sentences_Evidence_from_structural_priming).

**Actual reading scope 2026-10-12:** Study introduction, experiment hypotheses, methods and results for all 3 experiments, and General Discussion read via author's publicly posted full-text HTML mirror. Appendices' 40/36-item inventories were not individually audited; peer-reviewed publisher final PDF not independently compared. Prior SSN summary [here](vangompel2006-garden-path-priming.md).

## The research question came from an *identification problem*

A simple Yes to “Did the man visit the children?” after a garden path could mean (a) old transitive structure still has an effect, (b) metalinguistic questioning reactivates it, or (c) respondents use a general plausibility strategy. **The paper does not need a new garden-path construction**: it changes the evidence type. A later unrelated sentence-production choice is harder to dismiss as the same biased Yes/No answer.

**Parent literature:** Christianson et al. 2001 lingering thematic roles; Kaschak & Glenberg 2004 trace of a newly learned construction; classical structural priming in production. **RECONSTRUCTED genesis:** identify metalinguistic probing as a potential reactivation artifact → use subsequent production as downstream functional readout → success still admits lexical boost, plausibility and incomplete-parsing explanations → target these sequentially in Experiments 2–3.

## Experiment 1 — does past misparse affect independent target syntax?

- Material example: subordinate-clause NP/Z with/without comma, longer vs shorter ambiguous object region; target a prompt for a later transitive or intransitive completion.
- Participants silently read prime, produced aloud a completion, sometimes answered a comprehension question; measurement **does not require an explicit question about prime's initial wrong interpretation**.
- Exclusions: source/target word alterations, implausibly fast/slow prime reading (<500ms or >15s), and “other” syntactic completions not unambiguously direct transitive/intransitive.
- **Observed:** transitive completion rates 33.6% after GP vs 29.1% after comma-disambiguated prime. Long-region primes gave 36.7% vs short-region 25.9% in transitive production, but interaction evidence for ambiguity × length was weak/mixed across participants/items.
- **What this identifies:** behaviorally a prime context boosts an inappropriate transitive structure. It does **not** directly prove that a fully specified incorrect parse remains active in memory or exclude ordinary syntactic-context priming.

## Experiment 2 — can early semantic plausibility change persistence?

- 50 candidate items; selected 36 after independent plausibility norms, crossed GP/cue with locally plausible vs implausible NP direct object.
- Competing predictions: deep semantic commitment to plausible wrong transitive event should strengthen residual bias vs lexical-independent structural persistence might not show this difference.
- **Observed:** more transitive completions after GP than cue, **no clear ambiguity × plausibility interaction**. Whole-prime reading time did not tightly predict later transitive preference; read time did not identify the exact locus of processing difficulty.
- **Interpretation caution:** Null plausibility interaction in 36 items is not universal proof that meaning never matters; later work shows priming can interact with semantic coherence.

## Experiment 3 — the strongest identification move, often overlooked

- Pilot weakness of E1/E2: **repeated prime and target verbs** could create a purely lexical effect.
- Reconstructed decisive prediction:
  - lexical-specific residual: GP−cue priming disappears when target verb differs from prime verb;
  - abstract transitive residual: GP−cue difference remains even with verb change;
  - mixed explanation: effect weakens but does not vanish.
- Design: 40 items; 40 participants; 2×2×2 conditions (GP/cue × same/different verb × counterbalanced verb); long ambiguous regions throughout.
- **Observed:** transitive completions 68.6% GP vs 61.6% cue; no reliable ambiguity × verb-repetition interaction. The *correct final subject analysis*, by contrast, showed a different verb-repetition pattern. This asymmetry challenged a simple fixed-sum competition between two parses.
- **Important:** E3 itself already established **lexical independence for humans**, so the finding 'different verb and still priming' is NOT novel per se.

## Inferential bounds and scale

The study's contribution is an **implicit cross-task behavioral diagnostic** plus an exact, sequential comparison of semantic, lexical and structural alternatives. It supports lingering inappropriate analysis, **not** a unique physical storage/activation mechanism: episodic trace and incomplete reanalysis still compete. Some dependent measures are completions conditioned on exclusion of "other" outputs; production counts and RT location limit generalization.

## What an LLM extension must exceed

1. [Sinclair et al. TACL 2022](../priming/sinclair2022-structural-persistence.md) already owns general **LM** structural persistence after prime exposure; [Pucci et al. 2026](../priming/pucci2026-primed-production.md) owns free LM priming and semantic alignment.
2. An LLM GP-vs-comma effect, even with different verbs, is only a **transfer/replication** of a human-style diagnostic. Need **predictive interaction** not already accounted for by target structure, punctuation, lexical/semantic overlap or generic priming.
3. A deterministic causal Transformer produces identical outputs under identical token history regardless of chunked feeding; a next-sentence effect is still a *contextual probability response*, not direct evidence of a hidden human-like ongoing initial parse.
4. Different target completion styles (prefix log odds vs unconstrained production) are separate metrics; use both, avoid conditioning on previous comprehension success. Ordinary transitive/intransitive positive controls must work.

## Strong possible NEXT experiment

Instead of only GP vs cue, vary a normed *prefix transitive preference* while preserving naturally available alternatives, then test whether an **extra path effect** on a lexically disjoint target depends on prior probability after controlling punctuation and ordinary structural priming. Predictive failure on unseen verbs is a valid negative; a single β term on small stimuli is not enough.

This is a **proposal**, not a result, and still requires a valid targeted NP/Z dataset and source gold.
