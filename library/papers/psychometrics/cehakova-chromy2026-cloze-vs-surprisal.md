# Ceháková & Chromý (2026) — Cloze, Frequency, Surprisal, or Plausibility?

**Publication:** Cognitive Science 50(4), e70208, first published 2026-04-30. DOI 10.1111/cogs.70208. **Reading scope: main HTML ``1–6, methods, results Tables 1–4 and Discussion checked against the publisher primary page on 2026-10-12; supporting PDF/OSF scripts NOT checked.** [Full publisher article](https://onlinelibrary.wiley.com/doi/full/10.1111/cogs.70208). Evidence category: VERIFIED_FULL_MAIN, APPENDIX_UNREAD.

## 1. Parent scientific problem and why it matters

Not “do people get garden-pathed?”—known. The issue is **why the same broad garden-path class exhibits huge item-level and construction-level variability in processing time and final comprehension**. Lexical surprisal, verb argument preference, plausibility, and syntactic complexity correlate, so earlier claims often tested incompatible materials/populations. The paper asks which measurable property explains both likelihood of misinterpretation and ease of escaping it.

## 2. Idea genesis (RECONSTRUCTED, not author biography)

- Parent account A: minimal attachment/simple structure induces wrong first parse.
- Parent account B: a verb's syntactic frequency preference commits the parser.
- Parent account C: the disambiguating word's surprisal determines difficulty.
- Parent account D: event plausibility helps or hinders alternative analysis.
- **Pressure:** item variability within a syntactic class, and disagreement across studies, defeat any unqualified one-factor claim.
- **New inferential object:** separate THREE analyses of *different portions of the same sentence*, rather than one “garden-path cost”:
  - `AmbMis`: initial **misinterpretation** of the ambiguous region;
  - `AmbCor`: final **correct reinterpretation** of that region;
  - `DisCor`: correct attachment/analysis of the **disambiguating region**.
- The design question before seeing results: which of 12 properties of these three components predicts RT *and* understanding across 11 naturally diverse structures?
- Key move: use **independent human cloze completion ending before disambiguation** to estimate interpretation likelihood, not lexical continuation probability alone.

## 3. Data design and numeric facts from main article

- Czech, 11 GP construction types. Initial 8 lexical item families/type = 88; 164-person naturalness study (88 experimental + 126 fillers); retain 6/type = **66 experimental families**, 8-word stimuli, typically 1–3 ambiguous words. Ambiguous condition mean naturalness 45.18 (SD20.67), unambiguous 68.89 (SD16.63), **meaningful naturalness imbalance**.
- Cloze norming: 115 students, open-ended completion of prefix prior to disambiguator; manually coded AmbMis vs AmbCor interpretations; mean ClozeAmbMis .766 (median .887), ClozeAmbCor .268 (median .139).
- Plausibility: 111 students, 3×2 Latin square on three interpretation types; normalizer/predictor distribution is measured rather than assumed from words.
- Surprisal: **CzeGPT-2 124M**, trained on 5GB Czech, sums token surprisal over each region; not GPT-5 and not a human processing model.
- Reading/answer main task: initial 303 native Czech undergraduates, 8 excluded by predeclared filler/RT quality; **N=295 participants**. Word-by-word moving-window SPR. 66 experimental trials with 78 fillers, Latin square one condition per participant. One initial-misanalysis Yes/No question per item, response keyed 'No' on both GP and controls; question item092 excluded due script error.
- Inferential analysis: 12 separate predictor×ambiguity models per dependent measure because collinearity, participant and item random effects; Bonferroni thresholds 0.004 accuracy and 0.002 across two RT regions; log RT after 100–5000ms trimming (0.38% discarded).
- Outcome: GP vs cue accuracy impairment present. After adjustment, for accuracy AmbMis cloze×ambiguity β≈−.344 (SE .10), PlausAmbCor β≈+.342 (SE .10); no others significant at stated threshold. BIC accuracy ClozeAmbCor=17,704.93 and ClozeAmbMis=17,705.58 outrank alternatives.
- Disambiguator reading time: AmbMis cloze×ambiguity β≈+.018 (SE .006); BIC AmbMis cloze and PlausAmbCor close. Spillover: AmbMis cloze β≈+.051 (SE .012), AmbCor cloze β≈−.053 (SE .012), surprisal DisCor β≈+.044 (SE .012) all interaction terms significant; BIC cloze versions again dominate among the models considered.
- **No causal evidence that a particular latent incorrect parse was “locked in.”** This is an observed regression among human participants; moreover cloze is off-line and can reflect strategic choice.

## 4. Strength and failure conditions

Strength: broad types, independent norming of competing interpretations, multiple dependent measures, actual participant/item random effects, preselected naturalness and Bonferroni adjustment.

Limits: only ~6 lexical items per construction; English-LM transfer untested; GP stimulus naturalness lower; 12 competing correlated regressors fit **in separate** rather than joint identifiable mechanistic models, so BIC comparison is predictive not causally identifying. Human cloze may capture reflective completion strategy, not initial millisecond parse. CzeGPT-2 surprisal and human distributions have mismatched sources; author's paper explicitly says its RT findings are **not directly comparable** to previous studies predicting the magnitude of human slowdown from surprisal.

## 5. Exact nearest-neighbor distance

- **Trueswell et al. 1993:** verb-specific constraints at local ambiguity; new paper uses wider cross-construction predictor comparisons and cloze-derived whole-prefix interpretation.
- **Huang et al. 2024:** lexical surprisal and large-scale human GP cost; this paper investigates *within/among item variation* and distinguishes AmbMis/AmbCor/DisCor, not a new magnitude mismatch result.
- **Ceháková & Chromý 2023/2025:** coherent vs fragmented outcomes; this 2026 paper is a **predictor** comparison, not an additional multi-probe semantic-coherence experiment.
- **Zhou et al. 2026:** syntactic belief update measure for RT; comparator exists, but not equivalent to human cloze.
- **Yoshida et al. ACL 2026:** existence proof of trained-LM surprisal fitting GP slowdown; cannot claim surprisal theory was logically disproved by Ceháková's ordinary CzeGPT-2 data.

## 6. Implication for OUR Garden Path project

Our Pilot A **cannot claim novelty simply from splitting AmbMis/AmbCor/DisCor**; all three are explicitly treated in this paper. It must produce a new *dependency-topology / downstream-use* prediction that goes beyond these three regions and the 2025 two-region accuracy work. If no such prediction can be separated from local-error propagation, reject the “global fracture” idea, even when some scores differ.

Our Pilot B needs human vs model interpretation likelihood as **separate measurements**, and any “stronger initial commitment” theory must be supported by actual prefix behavior rather than a verb label.

**Method to imitate:** begin with a natural variance not explained by coarse group means; identify competing properties of *what must change* and *what must be constructed*; obtain independent norming; compare models on same material with explicit limitations rather than committing to a neural story.
