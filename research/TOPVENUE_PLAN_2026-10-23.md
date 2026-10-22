# Bringing the garden-path work to ACL/EMNLP/NAACL standard (resumed 2026-10-23)

The user resumed the project on 2026-10-23 and asked to align it with the related work at ACL/EMNLP/NAACL and to fill the gaps. This file is the work plan. Results go into each experiment card and [CURRENT_UNDERSTANDING](CURRENT_UNDERSTANDING.md).

## 1. Related-work check (searches on 2026-10-23; abstract level unless a library card exists)

| Line of work | Closest recent papers | Relation to our claim |
|---|---|---|
| GP comprehension and lingering in LMs | Li et al. 2024 (arXiv 2405.16042); Amouyal et al. ACL 2025; Amouyal et al. ACL 2026; Baitalik & Datta ACL-SRW 2026 | QA lingering and recovery are measured, but nobody looks at what the abandoned parse does to *later* sentences |
| GP surprisal vs humans | Huang et al. JML 2024; Yoshida et al. ACL 2026; Timkey, Dillon & Linzen 2026 (arXiv 2605.15440, parse multiplicity); Zhou et al. 2026 (arXiv 2606.27206, belief update) | about the size of the GP effect at disambiguation, not its after-effects |
| GP mechanisms | Hanna & Mueller NAACL 2025 | features for both readings coexist; QA does not reuse the syntax features. No priming and no "stale representation" test |
| LM structural priming | Sinclair et al. TACL 2022, JML 2026; Michaelov et al. EMNLP 2023; Jumelet et al. ACL Findings 2024; Zhou, Frank & McCoy NAACL 2025 (ICL is error-driven); Pucci, Li & Sinclair EMNLP Findings 2026 (priming in production); Lee et al. CDL 2026 (no cross-domain priming) | all use unambiguous primes. None uses temporarily ambiguous primes, so none can separate residual activation from error-driven learning |
| Human misparse priming | van Gompel et al. JML 2006; Fujita & Cunnings 2020 | the human effect we transfer |

**Novelty check:** still no LM study of abandoned-parse priming. Error-driven ICL is already established (Zhou et al. 2025), so our novelty rests on: (i) the GP prime as a crucial case where the two accounts predict opposite signs; (ii) both forces present at once; (iii) the measure decides which dominates; (iv) the residue in free production, and the punctuation-alignment artefact that reverses the raw human statistic.

## 1b. Benchmark against comparable accepted papers (on the user's dimensions, 2026-10-23)

Comparable papers: Amouyal et al. ACL 2025; Hanna & Mueller NAACL 2025; Jumelet et al. ACL Findings 2024; Zhou, Frank & McCoy NAACL 2025; Sinclair et al. TACL 2022; Pucci et al. EMNLP Findings 2026; Yoshida et al. ACL 2026. Figures come from abstracts and library cards and are approximate.

| Dimension | Typical accepted paper in this niche | Ours now | Gap |
|---|---|---|---|
| Model scale | 2 models (mechanistic: Hanna & Mueller) to ~10–20 models up to 70B or API (behavioural: Amouyal, Zhou). Scale trends are usually reported | 8–21 open models, 124M–32B; 32B only in E002/E003 | **moderate**: the core claims need ≥ 1–2 models of ≥ 27B, plus an explicit scale/instruction-tuning trend |
| Items | 45–100 hand-built families, or corpora of 10^4–10^6 pairs | 93 + 48 held-out NP/Z families, 54 Christianson families, MV/RR 64, NP/S; 10^5–10^6 scored pairs per model | none |
| Experimental workload | 2–4 experiments, each with one manipulation | 12 experiments, several frozen-prediction confirmations | **inverted**: too many findings, not too few. Needs compression |
| Number of claims | 1 headline + 2–3 supporting claims | ~6 loosely linked findings (residue, error force, measure dependence, free production, punctuation artefact, QA dissociation) | **main gap**: needs a 3-claim spine with a single question |
| Narrative | theory-driven contrast (Amouyal: three accounts → three manipulations; Zhou: ICL = gradient descent? → IFE diagnostic) or phenomenon → mechanism (Hanna & Mueller) | chronological lab notebook (E001 → E012 with corrections) | **must rewrite**: question → crucial test → two forces → causal tests of each → mechanism → consequences |
| Causal evidence | at least one intervention per central claim (Zhou: fine-tuning control; Hanna & Mueller: feature interventions) | error force causal (E006); commitment correlational; no mechanism | **E014 + E013** |
| What is proved | "LMs show X like / unlike humans, because Y" | "LMs show both residue and adaptation" (descriptive) | the *because*: stale states (E013) and causal commitment (E014) |
| Field and audience | ACL track "Linguistic theories, cognitive modeling and psycholinguistics", plus interpretability | same, plus an evaluation-methodology point | the broader NLP relevance must be stated (below) |

**Significance, stated as a reader of each audience would care:**
1. *Psycholinguistics / cognitive modeling:* garden-path priming is a **crucial case** where residual-activation and error-driven theories of priming predict opposite signs. In humans only the net is observed. LMs show both forces, separable and each causally manipulable. This gives a testable human prediction: more surprising disambiguation → less abandoned-parse priming.
2. *LM science / interpretability:* "ICL is error-driven learning" (Zhou et al. 2025) is incomplete. A second, non-error-driven persistence exists, and its plausible cause is architectural: a causal LM cannot recompute representations formed before a disambiguation (E013 tests this). The general consequence is that **an interpretation a model has abandoned keeps shaping what it writes next**.
3. *Evaluation methodology:* transferring a human production paradigm naively gives the opposite sign (E012 punctuation-style alignment). And "lingering" measured by QA is a different phenomenon from the residue (E003). Claims of "human-like / unlike" garden-path behaviour must say which measure they use.

**Target paper spine (3 claims + 1 method point):**
- **C1 Phenomenon:** a garden-path prime leaves a residue of the abandoned analysis in later production, in log-probability and in free generation. It survives punctuation, verb-bias, case and local-coherence controls, and holds on held-out items across ~20 models (E002, E005, E009, E011, E012).
- **C2 Two forces:** the same prime also drives error-driven adaptation toward the resolved parse. The forces have opposite signs, each is causally manipulable within family (E006 error; **E014** commitment), and the measure decides which dominates (E010).
- **C3 Mechanism:** the residue is read from stale pre-disambiguation NP states; the adaptation lives downstream (**E013**).
- **M Method:** the raw human statistic is invalid for LMs, and QA lingering dissociates from the residue (E012, E003).
E001/E004/E007/E008/E003b-c become appendix or boundary conditions (E007/E008 bound C2 to non-monotonic reanalysis).

## 2. What a reviewer would attack, and the answer we need

| # | Likely reviewer objection | Planned answer |
|---|---|---|
| R1 | "The commitment force is correlational between items. Only the error force has a causal manipulation." | **E014**: same GP prime, preceding context raises or lowers V's object expectation. Within-family slopes on measured commitment and error |
| R2 | "*Why* does an abandoned parse linger in an LM? 'Residual activation' is a human metaphor." | **E013**: a causal transformer never recomputes the NP's states after disambiguation; they are byte-identical to the transitive prime's. Patch the NP states with states computed under the subject analysis ("simulated reanalysis") and test whether the residue disappears. Control span: the main clause |
| R3 | "Models are ≤ 12B (32B in two experiments). Does this hold at scale?" | add larger models (Qwen2.5-32B, Qwen3-32B, Qwen3.5-27B, gemma-2-9b, Mistral-Small-24B; a 70B model if the cache allows) to the core experiments E002/E005/E009/E011/E012 |
| R4 | "The prime–target concatenation format is arbitrary." | robustness of A_L to the separator (space, newline, numbered list, dialogue turn) on a subset of models |
| R5 | "Bootstrap per model; where is the pooled inference?" | a cross-model random-effects meta-analysis of every headline contrast, plus mixed-effects robustness |
| R6 | "Lingering (E003) is a separate story." | keep it as the dissociation result; E003d decomposes it if time allows |

## 3. Order of work

1. E013 (mechanism; strongest LM-specific novelty) and E014 (closes R1). Cards are frozen before data.
2. Scale extension (R3), then format robustness (R4).
3. Meta-analysis and figures (R5), then the paper draft.

GPU use: the free cards the user named on 2026-10-23 (fvcrc13 ×4, fvcrc21 ×4, fvcrc10 ×2), one model per process.
