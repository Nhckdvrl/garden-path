# Claim ownership and novelty distance (current as of 2026-10-12)

This is **not** an automatic kill list or a mandate to invent a totally untouched problem. **Classic human studies (e.g., 2006) precede modern LLMs.** An independently rigorous modern LLM adaptation, especially one revealing similar/different behavior, may itself be a legitimate scientific contribution. Compare existing work with the **same system and task**; generic LM priming does not automatically subsume garden-path *wrong-analysis* priming. The last column contains possible extensions, **not mandatory novelty gates**. [Methodology update](../research/SCIENTIFIC_NOVELTY_STANDARD.md).

| Area | Existing owner (verified publication / source) | What is already covered | Examples of meaningful follow-up (not mandatory gates) |
| --- | --- | --- | --- |
| GP comprehension in LLMs | [Amouyal et al., ACL 2025](https://aclanthology.org/2025.acl-long.403/) | Human/LM understanding failures, plausibility and structural manipulations, paraphrase/image corroboration | Conditional, task-robust, previously unmeasured relation failure and prediction |
| Seven difficult structures / scaling | [Amouyal et al., ACL 2026](https://aclanthology.org/2026.acl-long.1040/) | Broad cross-construction / model-family comparison; some powerful models poor on GP | An explanatory variable that predicts within-construction item heterogeneity, not another score table |
| Early/late LM comprehension | [Li 2024](https://arxiv.org/abs/2405.16042) | Incremental interpretation, reanalysis correlates | Behavioral dissociation predicting independent usage, not just probe curves |
| Multi-reading mechanistic circuits | [Hanna & Mueller, NAACL 2025](https://aclanthology.org/2025.naacl-long.164/) | SAE feature evidence for competing readings and limited downstream QA reuse | A robust phenomenon requiring new causal explanation, and validated feature coverage |
| Surprisal vs garden-path RT | [Huang et al., JML 2024](https://doi.org/10.1016/j.jml.2024.104510); [Yoshida et al., ACL 2026](https://aclanthology.org/2026.acl-long.1694/) | Off-the-shelf LM underprediction vs trained-LM existence proof | Correctly defined RT prediction with hold-out and strong baselines; LM QA accuracy alone irrelevant |
| Syntactic belief update | [Zhou et al. 2026](https://arxiv.org/abs/2606.27206) | Tree-distribution update predicts RT cross-construction differences | Precise within-construction failure and potential causal validation; do not call 'belief update' ours |
| Human cloze / verb / plausibility | [Ceháková & Chromý, Cognitive Science 2026](https://doi.org/10.1111/cogs.70208) | Human cloze misanalysis likelihood predicts response difficulty more robustly than isolated predictors | A model-conditional, matched-predictor finding that transfers beyond human self-paced RT |
| Partial reanalysis & lingering | [Slattery et al., JML 2013](https://faculty.wcas.northwestern.edu/myo507/Papers/SlatteryEtAL_GoodEnough_Published.pdf); [Huang & Ferreira 2021](https://doi.org/10.1016/j.jml.2021.104288) | Correct function can coexist with lingering wrong analysis; local vs global representation | A new, quantitatively predictive failure topology and generalization boundary |
| Beyond wrong initial relation | [Ceháková & Chromý, Discourse Processes 2025](https://doi.org/10.1080/0163853X.2025.2513210) | GP may harm comprehension of noninitial region too | Beyond a two-region accuracy gap: structural-dependency-sensitive spread and out-of-sample prediction |
| Human wrong-parse priming | [van Gompel et al., JML 2006](https://doi.org/10.1016/j.jml.2006.06.004) | **Humans**: initial wrong parse can influence later sentence production | **Modern LLM translation is a plausible new contribution**; verify direct LM overlap, adequate lexical samples and standard structural/word-order controls; mechanism optional |
| Error-driven vs activation accounts of priming | [Jaeger & Snider, Cognition 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC7313543); Chang, Dell & Bock 2006; [Zhou et al. NAACL 2025](https://aclanthology.org/2025.naacl-long.586/) | **Humans:** priming grows with prime surprisal. **LMs:** inverse-frequency (error-driven) signature of in-context priming | Garden-path primes put the two accounts in opposite directions (abandoned transitive vs surprising final intransitive). Item-level separation in LMs (our E002/E005) |
| Generic LM priming | [Sinclair et al., TACL 2022](https://aclanthology.org/2022.tacl-1.60/), [JML 2026](https://doi.org/10.1016/j.jml.2025.104713); [Pucci et al. 2026](https://arxiv.org/abs/2609.04484) | Structural context persistence, lexico-semantic influences, generative production priming | A temporary-*misparse*-specific effect independent of existing priming factors |
| Post-disambiguation probability recovery | [Baitalik & Datta, ACL SRW 2026](https://aclanthology.org/2026.acl-srw.32/) | 100 GP/control pairs, causal vs masked models; surprisal/recovery summaries | Distinguish recovery of **asserted relations** from return to probable word stream |
| Lexical/structural error as noise | [Cao & Schuler, CMCL 2025](https://aclanthology.org/2025.cmcl-1.20/); [Clark et al., CoNLL 2026](https://aclanthology.org/2026.conll-main.25/) | Models' late text repair tendency; human targeted noisy-channel re-reading | Controlled actual corruption vs clean input and behavior calibrated to source reliability |
| Thinking longer on GP | [DeepSeek-R1 Thoughtology](https://arxiv.org/abs/2504.07128); [Amouyal ACL 2026](https://aclanthology.org/2026.acl-long.1040/) | Longer / rumination-heavy chains, heterogeneous thinking effects | Why and when added reasoning *selectively* revises interpretations beyond general anchoring |
| Model error interventions | [Bates, July 2025 blog](https://jonrbates.ai/2025/07/26/garden-path-sentences.html) | Early-layer ablations, 33→157 failure of original surprisal interpretation | Stable behavioral law before mechanism; isolated patch with preserved capability |
| Task/objective measurement | [Hu & Levy 2023](https://aclanthology.org/2023.emnlp-main.306/); old SSN E59/E87 | Token probability, actual output and metalinguistic QA need not agree | Object-specific predictions beyond 'asking differently changes answers' |

## Legacy experiment ownership inside our own team

**Never repackage these as new results simply because they were done in another repository.**

- **E52**: 14 models/5 families; printed question semantics and data qualification.
- **E69**: plausibility manipulations with mixed GP/cue outcomes.
- **E80**: trust/noise prompt modulation already tested, not stable joint revision.
- **E82/E87**: new model generations do reveal some real source failure; role readouts and task-dependent performance diverge.
- **E98/E99**: goal task can increase wrong free role descriptions on some families but not universal QA benefit.
- **E107**: reducing incorrect old commitments is not equivalent to explicitly committing to correct new dependencies.
- Evidence/source mapping: [SSN import README](../imports/ssn-incremental-revision/README.md). Original cards in old repo remain authoritative.

## Three kinds of compression risk

1. **Measurement-only:** 'LLMs also show this well-established human phenomenon.' Only interesting with a new theoretical prediction/outcome and well-matched human/LM protocols.
2. **Known gap with new label:** 'Correct answer ≠ global interpretation' or 'trace exists but is not used.' Needs a specific why/when with falsifiable transfer.
3. **Method-first:** 'We measured feature angles / patched a head and noticed QA changed.' Without a newly explained behavior and functional specificity, the mechanism claim is underspecified.

**Potential contribution:** a reliable modern-LLM manifestation, absence, or reversal of an established human pattern, or a structured new behavioral law. Mechanism is an optional depth, not a prerequisite. Prior-work ownership should calibrate claims, not mechanically veto transfer studies. If the data refuse a specific prediction, revise the explanation instead of building tools to rescue it.

## Our results (2026-10-13) and their nearest owners

| Our claim (experiments) | Nearest owner | Distance |
|---|---|---|
| Abandoned-object residue in LM production, licensed-analysis dependent (E002/E005/E009–E012) | van Gompel et al. 2006 (humans); Sinclair 2022 / Pucci 2026 (generic LM priming) | first LM transfer of the GP-specific effect, with punctuation, verb-bias and local-coherence controls and free generation |
| Error-driven adaptation toward the resolved parse, causal within family (E006–E008) | Jumelet 2024, Zhou et al. 2025 (error-driven / IFE priming in LMs); Fine et al. 2013 (human adaptation) | GP-specific; opposite sign to the residue on the same prime; tied to non-monotonic reanalysis |
| Measure dependence of which force dominates (E010) | none found | new |
| Comprehension lingering dissociates from priming item by item (E003) | Fujita & Cunnings 2020 (human, by measure) | item-level, LM, 10 models |
| Raw van Gompel statistic invalid for LMs because of punctuation-style alignment (E012) | none found | methodological |
