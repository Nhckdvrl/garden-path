# Calibration note: error-driven vs residual-activation priming, and where our garden-path results sit

2026-10-12. Search-based calibration (abstract-, snippet- and secondary-level unless marked). Written to judge the novelty and significance of the two-force finding (E002–E010) and the E003 dissociation, before the full E003 analysis.

## Who already owns what

| Claim | Owner | Scope |
|---|---|---|
| Prime surprisal and verb structural preference predict LM priming (inverse frequency effect); read as error-based implicit learning | Jumelet et al., ACL Findings 2024 ([anthology](https://aclanthology.org/2024.findings-acl.877/)) | dative/transitive Prime-LM corpora, GPT-2-large + 7B models |
| In-context learning shows the inverse frequency effect, stronger in larger models: "ICL is error-driven learning" | Zhou, Frank & McCoy, NAACL 2025 ([anthology](https://aclanthology.org/2025.naacl-long.586)) | Prime-LM core adapted; fine-tuning as positive control |
| Gradient-based adaptation of an RNN to reduced relatives and datives improves reading-time fit | van Schijndel & Linzen, EMNLP 2018 (D18-1499) | weight updates, not in-context |
| RNN adaptation (one gradient step on the prime) to NP/S garden paths; ambiguous vs comma primes | Frank, CogSci 2021 ([card](papers/priming/frank2021-crosslanguage-priming-rnn.md)) | primes truncated at the disambiguating verb |
| Humans: GP primes produce more transitive (abandoned-parse) completions than comma primes; residual activation | van Gompel et al., JML 2006 | 3 experiments; no measure of prediction error |
| Humans: syntactic adaptation to garden paths through implicit learning; less expected structures adapt more | Fine et al. 2013; Fine & Jaeger 2013 | replicability contested (Prasad & Linzen 2021; CUNY 2021 abstract; LCN 2025 failure to generalise) |
| Humans: priming changes reading times but not lingering comprehension accuracy | Fujita & Cunnings 2020, Applied Psycholinguistics | L1/L2, same-verb priming only |

## What is not owned (search did not find it)

1. **A garden-path prime as a crucial test between the two classic priming accounts.** In an NP/Z or MV/RR garden path, *residual activation* predicts priming of the **abandoned** analysis, while *error-driven learning* predicts priming of the **resolved** analysis, because the prediction error falls on the resolved structure. The two accounts predict opposite signs. In ordinary priming (datives, actives/passives) they predict the same sign, which is why IFE work cannot separate them. Our E002–E010 data show **both** forces in LMs, separately measurable: commitment → abandoned-object residue; disambiguation error → adaptation toward the resolved parse, causal within family (E006). The measure decides which dominates: production-like choice (L) vs comprehension-like surprisal (S).
2. **In-context garden-path adaptation in LLMs** (exposure to a GP lowers later GP surprisal, scaled by the prime's own disambiguation error). The adaptation literature is human or gradient-based; Zhou et al. study IFE, not garden paths.
3. **Item-level dissociation between comprehension lingering and priming residue in the same model and items** (E003). Fujita & Cunnings show a related human dissociation (priming vs accuracy), but not an item-level one.

## Honest significance assessment (preliminary; revisit after the full E003 analysis)

- **Strongest candidate idea (excitement test):** "Garden paths pit the two theories of structural priming against each other. Modern LMs exhibit both mechanisms simultaneously, with opposite signs, and which one you see depends on whether you measure production-like choice or comprehension-like expectation." This explains a model-dependent, seemingly messy literature-transfer result (van Gompel in LMs: sometimes yes, sometimes no). It makes a falsifiable prediction for humans (more surprising disambiguations should yield *less* abandoned-parse priming). It also connects ICL-as-error-driven-learning (Zhou 2025) to garden-path processing. An ACL reviewer would likely find this more than "LMs also show X".
- **So-what risks:** (a) "error-driven ICL" is already established (Zhou 2025), so the error force alone is an application. The novelty must rest on the **opposite-sign, same-prime** structure and its measure dependence. (b) A two-force decomposition can look like post-hoc curve fitting unless both forces have causal manipulations. The error force has E006; the commitment force has no clean within-family manipulation yet. (c) Effects are in log-prob units on constructed targets; reviewers will ask for generation-based production evidence. (d) Human comparison: the human prediction is untested, so the "humans vs LMs" angle is speculative.
- **E003 dissociation alone** (QA lingering ≠ priming residue) is a supporting result, not a headline. "Different tasks dissociate in LMs" is familiar (Hu & Levy 2023). It gains value only as converging evidence that the abandoned-parse residue is not the comprehension misinterpretation.
