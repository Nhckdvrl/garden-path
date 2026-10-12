# Garden Path research knowledge base

**Primary research repository:** [Nhckdvrl/garden-path](https://github.com/Nhckdvrl/garden-path). Revised 2026-10-12.

This library is a *scientific understanding and experiment-design resource*, not merely a bibliography or a list of untested ideas. It records what each paper's scientific question was, the parent claim it challenged, its key discriminatory experiment, nearest neighbors, evidence scope, and what our own study must do differently.

## Start here

1. [LITERATURE_MAP.md](LITERATURE_MAP.md): field structure and open explanatory tensions.
2. [RESEARCH_GENESIS_ATLAS.md](RESEARCH_GENESIS_ATLAS.md): reverse-engineered **idea genesis** / why each experiment was necessary / exact novelty scale.
3. [RELATED_WORK_OWNERSHIP.md](RELATED_WORK_OWNERSHIP.md): claim ownership, non-novelty warnings and promising differentiation.
4. [NEW_READINGS_2026-10-12.md](NEW_READINGS_2026-10-12.md): additional verified primary records; what was and was not actually read.
5. [READING_LEDGER.md](READING_LEDGER.md): evidence-scope ledger and unresolved close-reading debt.
6. [research plan](../research/RESEARCH_PLAN.md), then [measurement contract](../research/MEASUREMENT_PROTOCOL.md).

## Curated original notes from SSN (36 cards)

These are **curated imports**, not newly certified full-text reading. The header of every card preserves a link back to its exact original file, and its original in-card declaration controls evidence status. No numerical result should be cited without checking that status.

### Behavioral experiments and ambiguity comprehension
- [Amouyal ACL 2025](papers/behavior/amouyal2025-garden-path-humans-llms.md), [Amouyal ACL 2026](papers/behavior/amouyal-2026-processing-difficulties.md), [Li 2024](papers/behavior/li-2024-incremental-comprehension.md), [Cao & Schuler 2025](papers/behavior/cao-2025-disambiguation.md).
- [Ceháková & Chromý 2025](papers/behavior/cehakova2025-disrupted-final-interpretations.md), [Lee 2026 paraphrasing](papers/behavior/lee2026-good-enough-paraphrase.md), [Wang 2026 grammaticality](papers/behavior/wang2026-implicit-grammaticality.md).

### Human reanalysis, lingering meaning and revision cost
- [Slattery 2013](papers/human/slattery2013-competing-representations.md), [Huang & Ferreira 2021](papers/human/huang-ferreira2021-memory-versus-parse.md), [van Gompel 2006](papers/human/vangompel2006-garden-path-priming.md), [Christianson 2024](papers/human/christianson2024-rereading-and-question-order.md).
- [Sturt 2007](papers/human/sturt2007-semantic-persistence.md), [Malyutina 2016](papers/human/malyutina2016-blended-interpretations.md), [Maina-Kilaas 2026](papers/human/mainakilaas2026-digging-in.md).

### Structural priming / production
- [Sinclair et al. TACL 2022](papers/priming/sinclair2022-structural-persistence.md) ([actual public corpus audit](papers/priming/sinclair2022-data-asset-audit.md)), [Jumelet 2024](papers/priming/jumelet2024-structural-priming.md), [Sinclair et al. JML 2026](papers/priming/sinclair2026-human-lm-priming.md), [Pucci et al. 2026](papers/priming/pucci2026-primed-production.md), [Zhou 2025](papers/priming/zhou2025-error-driven-priming.md), [Frank CogSci 2021 (RNN GP-target priming via adaptation; full read)](papers/priming/frank2021-crosslanguage-priming-rnn.md), [Jaeger & Snider 2013 (priming scales with prime prediction error; abstract scope)](papers/priming/jaeger-snider2013-prediction-error-priming.md).

### Measurement and noisy-channel reasoning
- [Yoshida ACL 2026](papers/psychometrics/yoshida2026-surprisal-existence.md), [Hu & Levy 2023](papers/psychometrics/hu2023-metalinguistic-measurement.md), [Hu & Frank 2024](papers/psychometrics/hu-frank2024-task-demands.md), [McGee 2026](papers/psychometrics/mcgee2026-syntactic-encapsulation.md).
- [Clark et al. EMNLP 2025](papers/noisy-channel/clark2025-resource-rational-noisy-channel.md), [Clark et al. CoNLL 2026](papers/noisy-channel/clark2026-targeted-noisy-channel.md), [PoCO EMNLP 2025](papers/noisy-channel/park2025-poco-overcorrection.md).

### Mechanisms and neighboring belief-updating work
- [Hanna & Mueller NAACL 2025](papers/mechanisms/hanna-2024-gp-mechanisms.md), [Storer 2026](papers/mechanisms/storer2026-incremental-contextual-trajectories.md), [Causal Quotient 2026](papers/mechanisms/li2026-causal-quotient-belief-state.md), [Tang 2026](papers/mechanisms/tang2026-entity-tracking-state-changes.md).
- [Prakash 2026](papers/mechanisms/prakash2026-lookback-belief-tracking.md), [Yangjia 2025](papers/mechanisms/yangjia2025-spontaneous-retraction.md), [Balcells 2026](papers/mechanisms/balcells2026-belief-state-geometry.md).

### Experiment craft / evidential discipline
- [Mueller 2025 causally valid mediators](papers/craft/mueller2025-right-causal-mediator-survey.md), [Kamoi 2024 self-correction](papers/craft/kamoi2024-self-correction-survey.md), [Hu 2026 reasoning mechanisms survey](papers/craft/hu2026-reasoning-mechanisms-survey.md).

## Rules for local research agents

- **Scope first.** FULL_MAIN / MAIN_SECTIONS / ABSTRACT / SOURCE_METADATA / IMPORTED_SCOPE are distinct; do not inflate.
- **Ownership first.** Before calling something new, compare at least three specific neighbor claims and the *tested estimand*, not the paper's title.
- **Evidence types are not interchangeable.** Surprisal ≠ reading time ≠ source-grounded assertion ≠ role binding ≠ stable cross-task meaning ≠ a causal latent mechanism.
- **Reverse-design every experimental leap.** At each step: unresolved alternative, counterfactual predictions, why this measurement rather than another, observed limitations, strongest adversarial interpretation.
- **Negatives remain visible.** Do not erase no-effects, mixed architectures, cue damage, selection-conditioned comparisons, post-hoc relabeling, or externalized-pointer files.
- **Historical SSN evidence is separate from new results.** [Import manifest](../imports/ssn-incremental-revision/README.md).
- **Never infer that syntactic priming reveals a private persistent state.** It is a distributional context effect in a standard autoregressive LM unless stronger evidence is shown.
