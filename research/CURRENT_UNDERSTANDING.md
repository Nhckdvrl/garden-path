# Current understanding — NP/Z misparse priming in causal LMs

Living document. Each entry says what we believed, what changed it, and what is still open. Newest first. Experiments: `research/experiments/E00x_*` (cards are written before runs; post-hoc steps are labelled).

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
