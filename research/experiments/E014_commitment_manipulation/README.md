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

## Results (10 models, 87 families; 6 families dropped for a missing context, as frozen)

### Frozen test

| | result |
|---|---|
| **K0 manipulation check** (verb-level commitment OBJ > INT on average and in > 70% of families) | **0/10**. On average OBJ > INT in every model (+0.16 to +0.58), but only in 48–64% of families |
| K1 commitment coefficient on A_L > 0 | 10/10 (CI > 0 in 4); A_L(OBJ) − A_L(INT) > 0 in 4/10 (3 significant +, 2 significant −, both Pythia) |
| K2 error coefficient on A_S < 0 | 4/10; commitment coefficient on A_S > 0 in 8/10 |
| K3 error coefficient S < L | 6/10 |

**Frozen verdict:** K0 fails, so by the card's own rule the confirmatory test is **uninformative**. The contexts did not move the verb-level transitivity expectation reliably. K1–K3 are reported but not interpreted as confirmation.

### Post-hoc (labelled PH_ in `analyze.py`; added after two models)

The contexts were written to make the *NP* a likely object, and they did that: NP-specific garden-path strength (gp_eff = surprisal of the disambiguating word without vs with the comma) rose by +0.9 to +1.7 nats in **10/10** models (60–77% of families). Effect of OBJ vs INT contexts on the residue:

| model | Δgp_eff | ΔA_L (± se) | ΔA_S (± se) |
|---|---|---|---|
| Gemma-2-2B | +1.29 | −0.06 ± .04 | +0.06 ± .05 |
| Gemma-2-9B | +1.72 | −0.01 ± .05 | **+0.16 ± .07** |
| Llama-3.2-3B | +1.06 | −0.06 ± .05 | **+0.12 ± .04** |
| Llama-3.1-8B-Instruct | +1.05 | −0.02 ± .05 | **+0.36 ± .06** |
| Mistral-7B | +1.35 | **+0.13 ± .06** | **+0.28 ± .05** |
| Qwen2.5-7B | +1.10 | **+0.29 ± .07** | **+0.27 ± .06** |
| Qwen2.5-7B-Instruct | +1.41 | **+0.46 ± .11** | **+0.51 ± .10** |
| Qwen3-8B-Base | +1.73 | +0.13 ± .10 | +0.08 ± .08 |
| Pythia-1.4B | +0.88 | **−0.21 ± .03** | −0.03 ± .04 |
| Pythia-2.8B | +1.14 | **−0.10 ± .02** | **+0.06 ± .03** |

- On **S**, a stronger to-be-abandoned object analysis *raises* the residue in 9/10 models (7 significant, none significantly negative). S is the measure on which error-driven adaptation usually dominates (E010), and a stronger garden path also means a larger disambiguation error. An error-only account predicts the opposite sign. So the commitment (residue) force grows with the strength of the abandoned analysis, and here it outgrows the accompanying increase in error.
- On **L** the effect is model-dependent: positive in Mistral and the Qwen2.5 models, negative in the two Pythia models, null elsewhere. Within-family slopes on gp_eff: L > 0 in 9/10 (CI > 0 in 5), S > 0 in 8/10 (CI > 0 in 4).

**Reading:** E014 does not provide the clean causal confirmation it was designed for (failed manipulation check). Its post-hoc pattern is consistent with a causal commitment force, mainly on S, and inconsistent with an error-only account. The direct causal evidence for the residue force is E013: removing the object-analysis NP states removes the residue.
