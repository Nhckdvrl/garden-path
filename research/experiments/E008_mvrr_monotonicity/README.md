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
