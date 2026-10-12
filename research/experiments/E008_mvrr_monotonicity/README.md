# E008 — MV/RR: is the two-force structure tied to non-monotonic reanalysis?

**Status:** discriminating test. Card and frozen rule written 2026-10-12 after E007 (NP/S) failed and before any E008 scoring.

## Question

The two-force structure (commitment residue +, error-driven adaptation −) is robust in NP/Z (17 discovery models; held-out; within-family causal E006) but absent in NP/S (E007). Two explanations make opposite predictions for MV/RR:

| Account | NP/Z | NP/S | **MV/RR prediction** |
|---|---|---|---|
| Non-monotonic reanalysis (committed structure must be destroyed; Gorrell 1995; Sturt et al. 1999) | hard ✓ | easy ✗ | **structure present** (MV→RR is the canonical non-monotonic, hard reanalysis) |
| NP/Z-specific surface factors (subordinate-clause boundary, comma-less style) | ✓ | ✗ | **structure absent** (no clause-boundary comma issue) |

## Materials (64 families; `data/gp_behavior/derived/mvrr_prime_families_v1.jsonl`)

Amouyal 40 (author unreduced controls with the authors' relativizer, often *which*) + SAP 24 (ditransitive RRs, control *who was*).
- GP: reduced relative
- CUE: unreduced relative (author's string)
- NB/NC: same frames with an irregular participle that cannot be a main verb. Assignment rule fixed in advance: ditransitives → *given*; selection verbs → *chosen*; others → *seen*. These sometimes yield odd meanings; they are structural controls.

Two documented overrides: upstream metadata typos are bypassed by deriving the verb from GP/control alignment; s37's disambiguator is *was*, not *pleased*. A = (GP − NB) − (CUE − NC) on S = surprisal of the target's disambiguating main verb in a reduced-relative target.

## Measures

- Commitment: mv_expect = log[P(" the") + P(" a")] − log P(" by") after `NP verb` (main-verb-with-object vs passive-participle continuation). Noisy for SAP ditransitives, where both readings continue with an NP.
- Error: gp_strength = lp(disamb | unreduced) − lp(disamb | reduced).

## Frozen rule (same as E007)

- **M1:** NP/Z discovery t_obj ≥ 2 → predict b_obj > 0.
- **M2:** NP/Z discovery t_gp ≤ −2 → predict b_gp < 0.

OLS `A ~ z(commit) + z(gp_strength)` over the 64 families, one-sided t > 1.645, sign test across models. The verdict on the two accounts uses M1 and M2 jointly, with E007 as the contrast.

## Interim result (6 models; frozen rule)

M1 (commitment b_obj > 0): **0/5**. M2 (error b_gp < 0): **3/4** (Llama-3.2-3B t = −3.5, Pythia-2.8b −3.2, Pythia-1.4b −1.9; Qwen2.5-0.5B −1.6 not confirmed). MV/RR garden paths are weak in these models (mean 0.9–2.4 nats), yet the error slope appears. NP/S (E007) had larger errors (2.3–3.0) and no error slope. So, for the **error** component, the monotonic/non-monotonic split fits. The commitment residue has appeared only in NP/Z. Caveat: the MV/RR commitment proxy (log[P(the)+P(a)] − log P(by) at the verb) is crude and especially poor for the SAP ditransitive items, so "commitment is NP/Z-specific" vs "proxy invalid outside NP/Z" is unresolved.

(A counting bug in the printed summary, which showed M2 as 1/4, was fixed; the per-model table was correct.)

## Result (9 models)

M1 (commitment): **0/8**. M2 (error): **6/9** confirmed (sign test p = .25). The error force generalizes to MV/RR; the commitment force does not with this proxy.
