# Newly checked primary references — 2026-10-12

**Evidence discipline:** The verified sections here are those returned by the primary publisher/Anthology/author site and excerpts accessed during this session. These are **not all full-text cover-to-cover reads**. The 36 imported SSN notes have their own original reading-scope declarations.

## Ceháková & Chromý (2026), Cognitive Science, doi:10.1111/cogs.70208

- **Primary:** [PMC open-access text](https://pmc.ncbi.nlm.nih.gov/articles/PMC13129637/), [publisher](https://doi.org/10.1111/cogs.70208).
- **Scope verified:** publication metadata; abstract; introduction and discussion/conclusion excerpts. Tables, appendix and stimuli not yet independently reproduced.
- **Parent tension:** verb transitivity bias, structural preference, sentence surprisal and plausibility have been used to explain local GP processing with inconsistent outcomes.
- **Changed premise:** compare predictors on the same human dataset spanning **11 types** with self-paced RT and Yes/No comprehension.
- **Reported result:** cloze-derived likelihood of initial misanalysis is more robust than isolated verb bias/surprisal/plausibility in those conditions. This neither proves a neural latent parse in LLMs nor invalidates surprisal theory universally.
- **Idea genesis:** RECONSTRUCTED: rather than inventing a new processing model first, align rival predictors against a broad common measurement table, then ask which actually generalizes.
- **Our distance:** within-construction model-specific parsing probability + downstream *dependency-structured* errors, with predeclared out-of-sample predictions. We cannot use human cloze as a literal replacement for a model's own prefix distribution.
- **Need to finish:** stimulus list / predictors / model-selection details / random effects / per-construction results and whether cloze obtained independent norms.

## Bates (2025), Unexpecting the expected in language models

- **Primary author blog:** https://jonrbates.ai/2025/07/26/garden-path-sentences.html
- **Scope verified:** article main text, n=33 pilot vs n=157 follow-up, four-architecture summary and ablation caveats. **Technical blog, not a peer-reviewed publication.**
- **Idea pressure:** Is juke-point surprisal directly caused by early dominant parse commitment?
- **Critical negative:** Initial n=33 early MLP ablation appeared to lower GP surprisal; at n=157 the reduction did not reproduce (Llama ΔGPS +0.07 bits; Mistral +1.19). Large contrast stemmed largely from much worse ordinary continuation prediction, with Llama early-layer top-5 baseline overlap 2.5%.
- **What this does NOT prove:** that all GP models have a separate surprise generator or that a low-probability alternative is a fully accessible parse.
- **Transfer:** require positive intact-language controls for any future ablation and do not prioritize neuron/geometry work in stage 1.

## Baitalik & Datta (2026), ACL Student Research Workshop

- **Primary:** https://aclanthology.org/2026.acl-srw.32/
- **Scope:** official abstract and publication metadata; not a fresh complete PDF reading here.
- **Data reported:** 100 GP/control pairs in NP/Z, NP/S, MV/RR; causal models use surprisal, masked models use pseudo-surprisal; compare post-disambiguator disruption/recovery.
- **Owned claim:** probability or hidden-distance recovery trajectories differ with architecture; **no implication** that semantic role interpretation was repaired.
- **Our distance:** behavior on downstream role/dependency/meaning after full input, not claiming 'first recovery dynamics' again.

## Zhou, Stanojević & Hale (2026), Syntactic Belief Update

- **Primary preprint:** https://arxiv.org/abs/2606.27206
- **Scope:** primary abstract and indexed study description; full mathematical derivation and item-wise tests require subsequent text audit.
- **Innovation:** lexical surprisal and divergence of syntactic tree beliefs are separate candidate predictors for human processing cost. Generalized Rényi divergence between parse distributions.
- **Critical distinction:** an improvement in human reading-time fit is not a direct mechanism result for an instruction model's QA error. The preprint itself should be tracked by version and acceptance status.
- **Our distance:** include belief-update measures only if we can compute them without circular use of the comprehension target, and evaluate their held-out predictions.

## Sinclair et al. (2026), Journal of Memory and Language, 149:104713

- **Primary:** https://doi.org/10.1016/j.jml.2025.104713
- **Scope:** publisher abstract/highlights and prior SSN note on intro/method excerpts; not the complete 41-page article.
- **Question:** Does LM priming align with humans on individual items or only aggregate direction?
- **Reported:** dative priming is present in both; LM priming does not robustly predict EEG priming itemwise; sharing linear word order improves fit.
- **Learn:** group-average matching is weak; match stimuli at item level and separate priming from lexical/linear-word-order overlap.
- **Our distance:** temporary **wrong** parse effect over and above normal structural priming, with alternate prime structures and matched target tasks.

## Pucci, Li & Sinclair (2026), production priming

- **Preprint:** https://arxiv.org/abs/2609.04484 ; [code](https://github.com/the-context-lab/primedproduction)
- **Scope:** primary abstract + original SSN selected-section note; appendix/classifier not checked.
- **Changed evidence type:** from forced target log-probability to unconstrained production, controlling structural, semantic and lexical alignment.
- **Reported:** LMs show production priming modulated by semantic coherence, plus lexical/semantic alignment in primed completions.
- **Our distance:** not simply 'LLMs exhibit priming after garden-path'; the path-specific interaction and difference from final-parse priming must be isolated.

## Clark, Levy & Gibson (2026), CoNLL Outstanding Paper

- **Primary:** https://aclanthology.org/2026.conll-main.25/
- **Scope:** existing imported SSN card records full main text ``1–5 and appendix A/B examples (additional appendices not deep-read here).
- **Idea source:** noisily observed words may need to be reinterpreted; ordinary surprisal alone does not say which earlier region to revisit.
- **Experiment move:** matched prefixes and suffix-dependent likely error sites create different regressions in human behavior; corresponding inference model predicts this qualitatively.
- **Our distance:** actual source-noise calibration in LM, not a system tag asking 'maybe OCR'.

## DeepSeek-R1 Thoughtology (2025 preprint, later TMLR publication to verify)

- **Primary:** https://arxiv.org/abs/2504.07128 ; [project](https://github.com/McGill-NLP/thoughtology)
- **Scope:** author abstract, indexed `9 text and historical search; not a fresh end-to-end full text.
- **Owned:** 114 GP/control pairs, model thinking-length differences and repetitive reasoning; chain length is not equivalent to genuine successful reinterpretation.
- **Our distance:** this alone rules out 'GP means longer CoT' as a new finding; a reasoning extension requires controlling prior commitments, quality/quantity of feedback and equal compute, and must exceed ordinary answer anchoring.

## Follow-up full-text reading debt

Priority: Ceháková 2025 *complete analysis and appendix*, van Gompel 2006 *full experiments*, Sinclair 2026 *full design/classifier*, Ceháková 2026 *per-item tables and regressions*, Zhou 2026 *full derivation*, formal context-specific sample-size calculations. Do **not** write 'all papers fully read' until these tasks are actually completed.
