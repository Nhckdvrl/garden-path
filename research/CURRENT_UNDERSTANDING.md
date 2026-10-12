# Current understanding — NP/Z misparse priming in causal LMs

Living document. Each entry says what we believed, what changed it, and what is still open. Newest first. Experiments: `research/experiments/E00x_*` (cards are written before runs; post-hoc steps are labelled).

## 2026-10-12 (night) — error force is causal within family; two-force structure is near-universal; net effect is not

**New evidence:**
- **E006 (within-family manipulation, prefix fixed so commitment is fixed):** more surprising disambiguations produce more negative A. Llama-3.2-3B t = −6.3, Qwen2.5-0.5B −6.4, Pythia-1.4b −4.1; GPT-2 −1.4 and Pythia-410m −1.3, which are exactly the models whose discovery error slope was ≈ 0. Robust to generated-only variants, a naturalness covariate, and auxiliary-vs-lexical first word. The relevant error is surprisal **at the disambiguation point**; surprisal summed over the whole continuation predicts little. So the error-driven component is a causal effect of the disambiguation event, not a between-family correlate.
- **E005 (held-out, frozen rule):** 14/18 predictions confirmed in 8 models. Failures reported, notably Llama-3.2-3B's *between-family* error slope (null on held-out). Lesson: between-family regressions at n ≈ 24 per source are fragile; within-family manipulations carry the weight.
- **E002 panel (17 models):** commitment slope > 0 in 17/17; error slope < 0 in 15/17 (exceptions: GPT-2, Pythia-160m, the weakest garden-pathers). Net A ranges from −0.33 to +0.37 and is not ordered by size.

**Revised understanding:** "Does an LLM show van Gompel's lingering-parse priming?" has a model-dependent answer because it reads out the **net** of two opposing, separately measurable forces. Those forces are stable across 17 LMs. The commitment force is supported between families (17/17 discovery, 5/7 held-out) and by the E004 history test, but it has **no within-family causal manipulation yet**.

**Update (E007, NP/S):** the two-force structure did **not** generalize to NP/S under a frozen rule (G1 1/5, G2 0/4; net A ≈ 0), although A is reliable there and the predictors vary as much as in NP/Z. So the structure is not a property of every garden path. Candidate explanation from classic reanalysis theory: NP/S reanalysis is monotonic (no committed structure destroyed), NP/Z is non-monotonic. Test: MV/RR (E008).

**Open (priority order):**
1. Does MV/RR (non-monotonic) show the two-force structure (E008)? If yes, the boundary is plausibly reanalysis type; if no, NP/Z-specific factors (clause boundary, comma-less style) are the better explanation.
2. A within-family commitment manipulation (peer session E003 crosses plausibility × length on Christianson items, which gives a partial handle).
3. Human prediction: the error component implies that, in humans, garden paths with more surprising disambiguation should show *less* transitive priming. Testable with van Gompel-style designs plus cloze-normed items.

## 2026-10-12 (evening) — "Does the abandoned parse prime?" is the wrong unit of question

**Before:** following van Gompel et al. (2006) and Pilot B, we asked whether a ruled-out NP/Z object analysis primes later transitive structure: yes/no, and how much relative to a real transitive.

**What changed it (E002, discovery; 93 Amouyal+SAP families; 6 base LMs so far):**
- With punctuation- and verb-bias-matched contrast A = (GP−NB) − (CUE−NC) on a comma-free target measure (surprisal of the target's disambiguating word), the **net** residue ranges from **+0.22** (GPT-2; ≈47% of a true transitive prime) to **−0.29** (Llama-3.2-3B). Several Pythia models sit near 0.
- At the item level, A is the sum of two components with **opposite signs**, predicted by nearly uncorrelated variables:
  - **commitment** (model's object expectation at the ambiguous verb) → more transitive priming. Positive in all 6 models (t = 2.0–4.7).
  - **prediction error** (prime's own garden-path surprisal at disambiguation) → less transitive priming. Negative in the larger models (Llama-3.2-3B t = −5.5, Pythia-2.8b −3.1, Pythia-1.4b −2.5), ≈0 in the smallest.
- These match the two classic human theory families: **residual activation** (van Gompel 2006) vs **error-driven implicit learning** (Chang et al. 2006; Jaeger & Snider 2013). In a garden-path prime they push in opposite directions.
- E004 (exact repetition): a second, non-garden-pathed GP copy adds little transitive priming compared with a second TB copy (GPT-2, Pythia-410m, Pythia-1.4b). The residue depends on the garden-path processing episode, not on the string.

**Now:** the scientific object is the **balance** of two forces and what controls it (item properties, model scale/training), not a binary lingering effect. Human net data (van Gompel: GP > comma) suggest activation dominates in humans at the net level. Whether an error-driven component is hidden in human data is an open question this framing raises.

**Status:** exploratory. Held-out confirmation (E005: 48 SyntaxGym + Ceháková families, frozen prediction rule) is running.

**Open:**
1. Does the two-component structure replicate on held-out items (E005)?
2. Is the error component causal? Plan: E006, varying disambiguation surprisal within family with a fixed prefix.
3. How does the balance change with model scale, family and instruction tuning (full panel)?
4. Link to comprehension (peer session's E003): do items the model misunderstands carry more residue?

## 2026-10-12 (afternoon) — measurement corrections that shaped the above

- **E001:** the comma-placement target is dominated by **comma-position copying**. The planned DiD control was itself confounded (recorded before panel results). Only punctuation-matched contrasts are interpretable, which led to the comma-free target measure.
- **E002 order test:** a comma-dropped copy of a sentence just read with a comma is still garden-pathed (it is a *deviant* copy), so the planned processing-history manipulation failed its precondition and is not interpreted. Exact repetition (E004) replaced it.
- The verb-bias-matched contrast A was introduced after inspecting 2 models (labelled post-hoc); every later model and the held-out set are evaluated with it unchanged.
