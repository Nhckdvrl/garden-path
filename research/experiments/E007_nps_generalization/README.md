# E007 — Does the two-force structure generalize from NP/Z to NP/S?

**Status:** generalization test. Card and frozen prediction rule written 2026-10-12 before any E007 scoring.

## Why NP/S

In NP/S (*The student forgot the solution was in the back of the book*) the abandoned analysis is again a direct object, but the final structure is a sentential complement, not a new main clause, and the disambiguation error comes from a different syntactic configuration. If commitment (+) and error-driven adaptation (−) are general properties of how LMs carry garden-path episodes forward, the same item-level structure should appear. If they are NP/Z-specific (e.g. tied to subordinate-clause boundaries and commas), it need not.

## Materials (64 families; `data/gp_behavior/derived/nps_prime_families_v1.jsonl`)

Amouyal 40 + SAP 24 NP/S families, with author overt-*that* controls. Per family:
- GP: *forgot the solution was*
- CUE: *forgot that the solution was*
- NB/NC: S-complement-only verb (*hoped/thought/insisted/pretended/wished/boasted/reckoned/complained*, round-robin) without/with *that*
- TB: true object plus relative clause (*forgot the solution which was*)

Contrast A = (GP − NB) − (CUE − NC): punctuation-free and *that*-matched within pairs, verb bias cancelled across pairs.

## Measures

- **Within-construction targets:** content-disjoint other NP/S families. S = surprisal of the target's disambiguating word after `The nurse knew the patient` (GP target).
- **Cross-construction targets:** the 93 NP/Z target families (S as in E002). Exploratory: does an abandoned object analysis in NP/S shape NP/Z object expectations?
- Commitment: obj_expect = log P(" the") − log P(" that") after the subject + verb.
- Error: gp_strength = lp(disamb | that-version) − lp(disamb | GP).

## Frozen prediction rule (within-construction targets)

For each model, with NP/Z discovery slopes from `results/gp/E005/predictions.json` (discovery t-values):
- **G1:** if NP/Z discovery t_obj ≥ 2, predict NP/S b_obj > 0.
- **G2:** if NP/Z discovery t_gp ≤ −2, predict NP/S b_gp < 0.

Same OLS `A ~ z(obj_expect) + z(gp_strength)` over the 64 prime families; one-sided t > 1.645. Pooled sign test across models per prediction. Net A sign: no prediction (model-dependent in NP/Z).

## Result (within-construction targets, 6 models): generalization FAILED under the frozen rule

G1 (b_obj > 0): 1/5 confirmed (GPT-2 only). G2 (b_gp < 0): 0/4 confirmed. Net A ≈ 0 in all models (−0.14 to +0.11), while the true-transitive control still primes (Afull 0.3–0.95). The instrument works; the two-force structure is absent.

**Post-hoc diagnostics (do not alter the verdict):** A is reliable in NP/S (split-half r = 0.77–0.94) and the predictors have NP/Z-like spread (SD of gp_strength ≈ 2.0 vs 2.3), so the null is not a reliability or range artefact. NP/S garden paths are weaker on average (2.3–3.0 nats vs ≈ 5 in NP/Z).

**Interpretation to test next (not established):** NP/S reanalysis is classically *monotonic* or "easy" (Gorrell 1995; Sturt, Pickering & Crocker 1999): the NP stays inside the verb's complement and is lowered into a clause, and no committed structure is destroyed. NP/Z is *non-monotonic*: the NP must be detached from the verb. Hypothesis: the commitment residue and error-driven adaptation arise only when committed structure must be destroyed. Decisive test: MV/RR (non-monotonic), see E008.
