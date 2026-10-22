# E014: Is commitment causal? Same garden-path prime, context that raises or lowers the object analysis

**Status:** card frozen 2026-10-23, before any context was generated or scored.

## Why

The commitment force (more object expectation at the verb → more abandoned-object residue) is so far supported only *between* items (E002, E005, E009, E010) plus the licensing test (E011). The error force has a within-family causal test (E006). A reviewer will say the commitment slope could reflect any item property correlated with object expectation. E014 manipulates commitment while keeping the prime string, the target and the verb identical.

## Design

- 93 NP/Z families (E002). Five one-sentence contexts per family, placed before the prime:
  - **OBJ1/OBJ2**: make it likely that the subject is about to act on the NP (*The man had been tracking the deer since dawn.*);
  - **INT1/INT2**: make the subject's activity object-less and present the NP as an independent agent (*The man hunted alone that day while the deer grazed by the river.*);
  - **NEU**: mentions both without relating them.
- Constraints, checked automatically: all contexts mention the subject noun and the NP noun; none contains the ambiguous verb's lemma, the intransitive control verb, or any main-clause content word; one sentence, at most 16 words, no comma. Contexts are written by a local instruction model (Qwen3-32B, no thinking, deterministic) from a fixed prompt. No context is selected or edited on the basis of any scored model output.
- Primes after each context: GP, CUE, NB, NC. Residue **A(c) = (GP − NB) − (CUE − NC)** on L and S, computed within context c. The context itself is shared by all four primes, so its direct effect on the target cancels.
- Targets: E002 targets, content-disjoint from the family and from the context words.
- Per (family, context) probes in the scored model:
  - commitment = log P(" the" | c + *While the man hunted*) − log P("," | …);
  - error = −log P(disambiguating word | c + GP prefix up to the NP).
- Models: the E002 panel subset with complete caches (≈ 12 models, incl. ≥ 27B).

## Analysis and frozen predictions

Per model, regress A_L(f, c) and A_S(f, c) on commitment and error with **family fixed effects** (within-family variation only; 93 × 5 cells). Coefficients come from the within-family regression; CIs from a bootstrap over families.

- **K0 (manipulation check):** commitment(OBJ) > commitment(INT) on average in every model, in > 70% of families. If this fails, E014 is uninformative and is reported as such.
- **K1 (commitment is causal on the production measure):** within-family commitment coefficient on A_L > 0 in the majority of models (sign test across models), and A_L(OBJ) − A_L(INT) > 0 in the majority.
- **K2 (two forces within the same manipulation):** on A_S, error coefficient < 0 in the majority of models (replicates E006 with a different manipulation), and commitment coefficient > 0 with error controlled.
- **K3 (measure dependence):** the error coefficient is more negative on S than on L in the majority of models (as in E010).

If K1 fails while K0 holds, the commitment slope in E002–E010 is an item confound, not a causal force. The "two forces" claim would then reduce to a residue of unknown origin plus error-driven adaptation, and we report that.
