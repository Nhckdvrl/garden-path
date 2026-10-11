# Measurement and inference contract (no experiment run yet)

**v0.1, 2026-10-12.** Applies to both pilots. Treat any changes after seeing outcomes as POST-HOC, keep original files and old result maps.

## 1. The object being judged must be explicit

For input `While Anna dressed the baby played in the crib.` the **source** asserts an event of Anna dressing and a separate event of the baby playing. It does **not** entail that Anna dressed the baby; however that extra event is not necessarily logically *contradicted*. Ask **what this text states**, not what is possible in the world.

Represent every test proposition with one of:
- `ENTAILED`: supported by the printed sentence on its globally grammatical interpretation.
- `CONTRADICTED`: explicitly incompatible with the sentence in its stated scope, not merely absent.
- `NOT_ENTAILED`: possible but not asserted (important for optional-transitive initial-role questions).
- `UNRESOLVED`: source or probe meaning unclear; quarantined, not silently converted into a wrong answer.

Also classify model outputs as `ASSERTED_SOURCE`, `DENIED_SOURCE`, `UNSPECIFIED`, `AMBIGUOUS_RESPONSE`, `INSTRUMENT_FAILURE`. Distinguish rejecting an unsupported old dependency, explicitly establishing the correct new dependency, and simply omitting both. A paraphrase that says "someone acted" is not automatically a full correct binding.

## 2. Stimulus constraints and controls

- Start with original published data: [Amouyal 2025/26](https://aclanthology.org/2025.acl-long.403/) and [Ceháková & Chromý 2025 stimuli](https://zenodo.org/records/16358492). Original forms/answer labels remain immutable in source manifest.
- NP/Z and MV/RR as primary constructs. NP/S can be an out-of-sample construction after measurement passes. Keep structure-specific results separate before pooling.
- Each `family_id` has matched `GP` and `CUE` forms; for Pilot B also `NONAMB_BARE` and `NONAMB_CUE`. Controls with a missing comma after introductory adverbial clauses are potentially orthographically odd — grammar/naturalness audit required.
- Do not call "barked" a weak-transitive equivalent to "chased": it removes the competing analysis instead of only decreasing strength. Where verb preference is studied, include naturally optional verbs, independent cloze/probability measurements and controls for selection/semantic plausibility.
- Record verb argument structure, parser analysis, word/token length, crucial word position, referent identities, event structure, ambiguity span, punctuation, acceptability, semantic plausibility, target task.
- Avoid non-natural hand-generated stimuli with malformed relative clauses or invalid source-question pairs. Hold out new lexical families; no cherry-picked selected successes.
- The test material is not inferred from model answers. Require independent material acceptance before running inferential statistics.

## 3. Independent behavioral measurements

**Readout A:** literal event/role graph assertions, without asking a leading Yes/No question about the initial misparse. Output schema preserves unsupported-but-possible versus contradicted.

**Readout B:** balanced direct questions including old attachment, newly supported role, unrelated relation, and a counterfactual bridge dependency. Each independent prompt must be run **from a fresh identical input prefix**, not after seeing the answer to another question.

**Readout C:** free faithful paraphrase / two-sentence segmentation. Blind to condition and model; score exact roles and content links, distinguish implied/unspecified.

**Readout D:** in a separately sampled context, lexically disjoint syntactic production probabilities for Pilot B. No comprehension filter in the same context as production, no prefilled correct answer or demonstration leaking the parse.

**Surprisal:** model-specific optional covariate only, computed with correct token boundaries/multi-token crucial region and fixed context. It is **not** the same estimand as understanding, nor a standalone evidence of early misparse.

## 4. Why naive measurements fail

- `No` to “did Anna dress the baby?” is a standard source-grounded answer if meaning is “does the sentence report X?”, but ordinary world truth is `NOT_ENTAILED` rather than contradiction; report the rubric.
- Correct initial-relation rejection is not equal to correct final binding; SSN E82/E107 already showed why.
- Forced 2-option log-probability is not the same as real model generation: SSN E87 reported differences, so measure actual output and invalid/cap rate.
- One big prompt containing multiple questions can introduce target-order priming; independent prompts are primary, joint prompts secondary.
- Gold labels must not be decided by the tested model; blind review with disagreement adjudication, plus clearly recorded post-hoc label corrections.
- Do not use “model passes comprehension” as an inclusion filter when testing subsequent priming; that selection can induce bias and, in a single conversation, the comprehension question itself changes context.
- Avoid equating a source-label prompt or a zero-effect patch with a complete Bayesian/noisy-channel or neural-parsing mechanism.

## 5. Statistical unit and contrasts

- **Primary resampling unit:** original lexical `family_id`, not every paraphrase, question, token or model score as an independent replicate. If multiple targets share a prime family, resample whole families.
- Model-family estimates separately; any pooled estimate should preserve nested pairing and not be interpreted as 10,000 independent tasks. Prefer mixed effects / hierarchical uncertainty when data volume allows.
- Predeclare one primary contrast per pilot; bootstrap paired families and show 95% intervals, plus observed per-family scatter and direction counts.
- Model heterogeneity and controls for output format, cue behavior, construction, question order and invalid generation must be visible (not excluded from plots).
- Pilot sample sizes are for **instrument validation/effect discovery only**, not three-factor coefficient significance or theoretical confirmation. Expand based on independent effect-size/power analysis and hold-out groups, not after choosing a lucky subset.
- When comparing multiple alternative predictors, use nested or held-out evaluation and uncertainty in their incremental value; a significant coefficient is not causal evidence.

## 6. Proposed schema

New files should use unique `item_id`, `family_id`, `source`, `construction`, `condition`, `sentence`, `disambiguator`, `gold_claims` and `review` fields. `gold_claims` entries each contain `relation_id`, `predicate`, `arguments`, `truth_status`, `probe_type` and `confidence/source_span` when applicable. Production targets have distinct `target_id`, `candidate_transitive`, `candidate_intransitive` and independent lexical/semantic audit flags.

**Required provenance:** upstream URL, revision/hash, original row ID, tokenization/model revision, config, prompt SHA, freeze timestamp, train/discovery/confirmatory split, blind labels and original provenance. Don't replace original source labels with newly inferred labels in place.

## 7. Test criteria for instrumentation

- Published cues / controls are comprehensible by an adequately capable model under valid prompts. A floor or uniform "No" model is descriptive only.
- Answers reproduce under two option orderings and a genuine generation protocol; if they diverge, report scope, not average away.
- Source-grounded truth labels have stable high agreement; ambiguity and "NOT_ENTAILED" are reported, not coerced.
- Priming targets have reliable transitive/intransitive preferences with positive and negative control primes.
- Any claimed nontrivial residual survives independent lexical families and at least two model families, with third as scope/replication where practical.
- No GPU authorization or model assets are inferred from the fact that legacy code is in the repo.
