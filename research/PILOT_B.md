# Pilot B — does an inappropriate parse prime later production beyond ordinary context?

**DESIGN DRAFT; no current run.** Nearest direct human ancestor: [van Gompel et al. 2006](https://doi.org/10.1016/j.jml.2006.06.004). Nearest LM instrument: [Prime-LM / Sinclair et al. 2022](https://aclanthology.org/2022.tacl-1.60/).

## B1. A precise direction (Gemini's earlier proposal inverted it)

In NP/Z: `While Anna dressed the baby played ...`, an early temporary analysis treats `the baby` as object of `dressed` (**transitive**). Under the complete correct parse, `dressed` is used **intransitively** and `the baby` is subject of `played`.

A path-specific **old-analysis** priming account therefore predicts an **extra transitive target preference** after the GP version, not a special preference for the *final correct* intransitive analysis.

The effect is a conditional distribution shift, not a private residual hidden state. Any proposal mentioning a persistent "parse ghost" must keep that limited operational meaning.

## B2. Balanced prime conditions

- `GP`: locally tempting transitive parse, ultimately disambiguated.
- `CUE`: same lexical events with correctly placed explicit clause boundary (comma or independently audited overt delimiter) before temporary transitive attachment.
- `NONAMB_BARE`: prefix where early verb does not license the competing object reading; no comma.
- `NONAMB_CUE`: same nonambiguous prefix with comma.
- All four use the *same later main event* when possible, no item scored unless sentences are grammatical/natural and comparable. An omitted comma after an introductory subordinate clause can itself be an oddity; test naturalness and keep this confound explicit. Do not use 'barked' versus 'chased' as if only a scalar verb bias changed.
- Additionally compare matched ordinary `TRANSITIVE_PRIME` and `INTRANSITIVE_PRIME` sentences to establish that this model/target really responds to syntactic priming at all.

First stage: 20–30 independently checked NP/Z lexical families, no MV/RR mixture until the NP/Z protocol is demonstrably valid. Include multiple independently created target families, lexically disjoint from all prime content words.

## B3. Target and metric

Target should permit **both** grammatical transitive and intransitive completions in a new, unrelated domain. Keep target prefix and candidate alternatives literally identical across all prime conditions; independent linguistic review checks naturalness and role interpretation. Match target candidate length where feasible; always compute **within-target** differences before comparing prime contexts so fixed candidate-length effects cancel.

For model m, prime family f, and target t, define:

  L(m,f,t,c) = log P(T_transitive | prime(c), target prefix) - log P(T_intransitive | prime(c), target prefix)

Each probability scores the **same fully specified candidate string with correct tokenization**, not one arbitrary first token. Use exactly the same instruction format, separator and context length policy across prime conditions, and report tokenizer effects/greedy production separately.

Primary contrast:

  Δ_path(m) = mean_family,target [ (L_GP - L_CUE) - (L_NONAMB_BARE - L_NONAMB_CUE) ]

This difference-in-differences is **not magic causal identification**: the four sources differ in verb and surface structure. A positive Δ is interesting only together with accepted sentence quality, multiple lexical families, matched ordinary prime controls, and robustness to punctuation/semantic coherence. Report absolute prime effects in addition to Δ.

## B4. Must-have controls

- **No comprehension question** between prime and target in the same forward context. Separate independent QA runs can describe whether the source is usually answered correctly; never filter primary priming samples on QA success.
- No overlap of content verbs/nouns/entities across prime and target. Remove easy cross-item semantic connections, but report priming degradation if coherence disappears (Sinclair/Pucci already established semantic dependence).
- Randomize assignment of target to prime family, balanced target candidates and order. Do not change target distribution after inspecting model effects.
- Include neutral unrelated prime, ordinary transitive/intransitive primes, CUE and punctuation-controls; no pseudo-benefit from only comparing GP vs an extra-token comma.
- Check output distribution and limited actual free completions. Classification of produced syntax must be blind to prime condition and must distinguish actual verbs' argument structures.
- Run item-level family bootstrap/hierarchical model, avoid treating many targets per family as independent evidence. Compare **within each model** before pooling.
- If pre-disambiguator continuation probability shows no plausible competing transitive analysis for many items, that's a limitation; report full and language-qualified sets, do not post-select on model success.

## B5. Interpretive decision table

| Observation | Licensed inference | Not licensed |
| --- | --- | --- |
| Positive robust Δ_path on independent targets, valid controls | Additional GP-specific structural-context effect in this model/materials | An internal stored wrong parse, human-like incomplete reanalysis |
| GP and CUE same, normal structural priming positive | Target sensitive, but no detected extra path-dependent effect | No possible memory of initial reading anywhere |
| Δ only with overlapping words or semantic themes | Surface/semantic alignment account remains plausible | Abstract syntactic memory |
| Δ disappears on new lexical families / target format | Discovery-only, unstable | General model mechanism |
| No priming even for positive normal primes | Instrument failed or model/target not responsive | A falsification of path-specific priming |

## B6. Potential research contribution *if* replication survives

Find a **boundary law** (e.g. initial plausibility × disambiguator strength × downstream target structure) with controlled opposite predictions for (1) initial-error persistence, (2) ordinary priming by the final parse, (3) semantic alignment and (4) punctuation/length effects, and independent validation. Simply observing a difference from a comma condition is not enough; the human literature already knew that.

## B7. Data handling

Prepare a separate `data/gp_behavior/prime_manifest.jsonl`; keep upstream source line and revised cue form as distinct versions. A validated manifest identifies `family_id, condition, prime_sentence, target_id, target_prefix, transitive_candidate, intransitive_candidate, lexical_disjoint_review, acceptability_review, source_revision`. See [measurement contract](MEASUREMENT_PROTOCOL.md). Existing model engines in `src/` serve old Unring-the-Bell tasks; do not silently reuse old generation settings as if priming logprob scoring were calibrated.
