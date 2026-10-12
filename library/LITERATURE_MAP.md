# Field map: temporary syntactic ambiguity as a controlled test of revision

Updated 2026-10-12. Scope: Garden Path (NP/Z, NP/S, MV/RR and well-controlled neighbors), behavior before mechanisms.

## Six research programs — different explananda

| Program | Actual question | Strong precedent | Our restraint |
| --- | --- | --- | --- |
| Garden-path *behavior* | Does the **same task** become harder under temporary ambiguity? | Amouyal ACL 2025/2026, Li 2024 | Another benchmark/accuracy gap alone is not new. |
| Good-enough interpretation | Is the error confined to obsolete role or does later meaning become incomplete? | Slattery 2013; Huang–Ferreira 2021; Ceháková–Chromý 2025 | Human results and some LM QA tasks already cover components. |
| Prediction/update cost | Is disambiguation difficulty lexical surprisal, parse update, misanalysis likelihood, or something else? | Huang 2024; Yoshida ACL 2026; Zhou 2026; Ceháková–Chromý 2026 | Do not use LM QA failure to refute a *reading-time* theory. |
| Residual structural priming | Can a superseded reading modulate a subsequent independent construction? | van Gompel 2006 (humans); Sinclair TACL 2022 / JML 2026 / Pucci 2026 (LM priming) | Generic LM priming is known; a rigorous transfer of the **specific human wrong-parse effect** to modern LLMs can itself be new. Test lexical, structure and punctuation controls without requiring a new mechanism. |
| Noisy-channel inference | Does a late anomaly trigger reinterpretation of syntax or suspected input errors? | Cao–Schuler 2025; Clark EMNLP 2025, CoNLL 2026 | Legitimate punctuation restoration ≠ refusing the original evidence; simple source-label prompting was already tested in SSN E80. |
| Mechanistic decoding | Are alternative readings represented, repaired, used by downstream QA? | Hanna–Mueller NAACL 2025; related state tracking | Probe decodability and causal faithfulness have different meanings; no geometric story before robust behavior. |

## The real cross-paper tensions

**Tension A — meaning versus task success.** In Amouyal's source-grounded tasks, a correct Yes/No decision is not logically equivalent to a coherent global event representation. SSN E70/E82/E87/E98/E107 already separate some local/final bindings and production. The new research must improve the *behavioral decomposition and novel prediction*, not merely repeat that "QA ≠ understanding."

**Tension B — what survives the garden path?** Slattery 2013 offers evidence that the new reading can be used even as an old reading still matters. Ceháková–Chromý 2025 argues disruption may extend outside the initially misanalyzed region. These are not contradictions until probes and timepoints are matched; the interesting question is their *boundary conditions*.

**Tension C — initial probability versus late evidence.** Human cloze-based misanalysis likelihood (Ceháková–Chromý 2026) predicts difficulty; surprisal-based human-RT explanations have new positive counterevidence (Yoshida 2026); syntactic belief update (Zhou 2026) is an adjacent competitor. These studies target different variables/populations; a causal claim about LM internal "commitment" needs more than a residual regression coefficient.

**Tension D — memory trace versus ordinary context priming.** van Gompel's 2006 human study detects priming by an inappropriate initial reading; Sinclair et al. 2022 identify LM structural priming generally. An LLM test of van Gompel's **human** effect is itself potentially useful, but interpreting it as *temporary wrong-parse* priming requires comparison with ordinary structural, lexical/semantic and punctuation effects.

**Tension E — intended text versus printed text.** A model can insert punctuation while preserving sentence truth conditions. This is not evidence of "hallucinated correction". Explicit noise tags are task prompts; source reliability must have validated manipulation and actual error controls if this line is reopened.

## Theory-to-measurement separations (nonnegotiable)

1. Before the disambiguator: continuation probability gives *distributional parse preference*, not certainty that the model held a full parse.
2. At the disambiguator: lexical surprisal measures predictive distribution change, not interpretation success or human reading time.
3. After the disambiguator: source-grounded event/role tests must distinguish entailed vs contradictory vs not asserted; a Yes to an unstated but possible event is not always a literal contradiction.
4. Downstream: independent task success, paraphrase fidelity and future choice distributions are distinct measures.
5. Inside the network: availability of a probe direction does not entail functional use; activation patching has confounds.
6. Across model families: heterogeneous failures can be real; never average away contradictory directions to rescue a universal story.

## Interesting but not yet demonstrated

- **H-GLOBAL:** temporally ambiguous input may disrupt construction or coordinated *use* of relations beyond the wrong early attachment, on natural LM items, after controlling general syntactic complexity, question position and source entailment.
- **H-PRIMING:** temporary wrong attachment may create a *specific additional priming contrast* over and above punctuation, final parse, lexical repetition and generic prime effects.
- These hypotheses are deliberately separable. There is no necessity that they join into one paper. See [research plan](../research/RESEARCH_PLAN.md).

## Canonical primary references

- [Amouyal et al. ACL 2025](https://aclanthology.org/2025.acl-long.403/); [ACL 2026](https://aclanthology.org/2026.acl-long.1040/).
- [Ceháková & Chromý 2025](https://doi.org/10.1080/0163853X.2025.2513210); [data/stimuli](https://zenodo.org/records/16358492); [Cognitive Science 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13129637/).
- [van Gompel et al. JML 2006](https://doi.org/10.1016/j.jml.2006.06.004); [Slattery et al. JML 2013](https://faculty.wcas.northwestern.edu/myo507/Papers/SlatteryEtAL_GoodEnough_Published.pdf).
- [Sinclair et al. TACL 2022](https://aclanthology.org/2022.tacl-1.60/); [JML 2026](https://doi.org/10.1016/j.jml.2025.104713); [Pucci et al. 2026](https://arxiv.org/abs/2609.04484).
- [Hanna & Mueller NAACL 2025](https://aclanthology.org/2025.naacl-long.164/); [Yoshida et al. ACL 2026](https://aclanthology.org/2026.acl-long.1694/); [Zhou et al. 2026](https://arxiv.org/abs/2606.27206).
- [Clark et al. CoNLL 2026](https://aclanthology.org/2026.conll-main.25/).
