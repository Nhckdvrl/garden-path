# What can behavioral Garden Path experiments actually identify?

**2026-10-12.** A hostile-reviewer checklist against mechanistic overclaiming. Refer to [Pilot A](PILOT_A.md), [Pilot B](PILOT_B.md), [2023 Ceháková/Chromý](../library/papers/human/cehakova-chromy2023-misrepresentation-diversity.md), [2026 predictor study](../library/papers/psychometrics/cehakova-chromy2026-cloze-vs-surprisal.md).

## 1. The deterministic-prefix identification ceiling

For a deterministic, evaluation-mode *causal* Transformer, with identical model weights, token sequence, positional IDs, masks, decoding and numerical computation, the hidden states/output distribution are the same regardless of whether a human researcher fed the tokens as one block or in consecutive chunks. For ordinary GP vs comma controls the actual input strings differ, so a later output difference **does not uniquely reveal that the model privately formed, stored and then failed to purge a wrong parse**.

A GP-specific priming interaction is still legitimate as a **context-distribution effect**; attributing it to a private persistent parsing state requires a special intervention or stronger operational definition. The phrase “memory trace” is only a behavioral analogy until proven.

## 2. Correct answer vs source-grounded relation graph

Answering `Who played?` correctly, rejecting `Anna dressed the baby` as not asserted, and producing an explicit coherent pair of events are three separate demands. Failure of one may result from generation preferences and prompt format, not internal inability to represent the relation. Conversely, a probe that decodes a relation does not show native free generation can use it. Report each outcome and condition-specific role dependencies rather than silently naming all wrong outputs “belief”.

## 3. Local dependency propagation can masquerade as global fragmentation

Suppose the model gets an early subject wrong and later cannot answer a question which logically **depends on that subject**. This second failure is fully predicted by a one-error/one-propagation account; it is *not* independent evidence that global sentence meaning broke apart.

To support a distinct “coordination failure”, contrast *independent supported facts* with *dependent facts* matched for word distance/complexity and ask for a new test outcome that a local-error propagation model predicts differently. If valid material cannot vary graph distance and token distance somewhat independently, we should stop claiming a causal separation—do not manufacture ugly sentences to force a factorial grid.

## 4. Candidate probability ≠ cloze probability ≠ processing cost

Human cloze analyses are manually categorized retrospective completions; next-token surprisal measures a different event distribution. A 2026 Czech human study sampled ~295 participants and 66 item families, but its results cannot be relabeled as model's inner belief strength. Its causal object is not simply `P(disambiguating token)`. Matching surprisal and finding another regression term significant is insufficient to prove a "commitment inertia" mechanism.

## 5. Negative controls can be harder than target phenomena

- GP conditions may lack a standard comma after an initial adjunct, making `GP` vs `CUE` a punctuation/naturalness comparison. Explicit comma absence must be audited.
- A verb with obligatorily intransitive use (`bark`) vs obligatory transitive use (`chase`) may delete the ambiguity rather than continuously change its strength.
- Structural prime/target pairs can share syntactic surface pattern, lexical semantic fit or word order. "Lexically disjoint" alone is necessary but not sufficient.
- A target that changes its *main verb* as well as argument structure measures broad lexical probability, not a clean syntactic choice.
- A parse that has never been directly supported by prefix probabilities should not be post-selected as “strong commitment” because final answer is wrong.
- An explicit comprehension check preceding priming changes the input; a success-only filter selects on an outcome after treatment.

## 6. What would justify mechanism work?

A replicated item-level phenomenon with distinct, precommitted predictions that survive task validity, matched no-GP difficulty, target controls and out-of-sample families. Only then choose a causal manipulation *specifically testing* whether early partial information is **necessary or sufficient** for the later behavioral phenomenon. It should predict not just one forced output label but the affected role/target family and an unaffected control. Probe angles and broad residual patching are not an explanation in themselves.

## Decision discipline

Do not assume the two pilots form one narrative. Missing effects with wide CIs are inconclusive, not a hidden falsehood; a precise null with valid positive controls is a real boundary. A well-controlled **new LLM application of a classic HUMAN phenomenon** can be a scientifically worthwhile, potentially publishable contribution even without a new mechanistic law, provided the same LLM task was not already settled. Cite the human owner, differentiate generic LM priming, and make the data/model boundaries explicit. See [novelty calibration](SCIENTIFIC_NOVELTY_STANDARD.md).
