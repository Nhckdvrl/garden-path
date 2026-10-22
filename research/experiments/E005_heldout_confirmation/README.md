# E005 — Held-out confirmation of the two-force account

**Status:** confirmatory design, frozen 2026-10-12 **before any E005 model output exists**. Materials, spec, prediction rule and analysis code are committed together. Discovery data: E002 + E004 on the 93 Amouyal/SAP families.

## What discovery suggested (exploratory; to be confirmed)

The net effect of a garden-path prime on a later NP/Z target (A = (GP−NB) − (CUE−NC), comma-free measure S) is the balance of two item-level components with opposite signs:

1. **Commitment / residual activation (+):** across prime families, A increases with the model's object expectation at the ambiguous verb (`obj_expect` = log P(" the") − log P(",") after `While the man hunted`). Discovery: b_obj > 0 in all 6 models analysed so far.
2. **Prediction error / adaptation (−):** A decreases with the prime's own garden-path surprisal at the disambiguating word (`gp_strength`). Discovery: negative in the larger models (Llama-3.2-3B t = −5.5, Pythia-2.8b t = −3.1, Pythia-1.4b t = −2.5), ≈ 0 in the smallest.

The two predictors are nearly uncorrelated across families (|r| ≤ 0.16), so they can be estimated jointly. Net A ranges from +0.22 (GPT-2) to −0.29 (Llama-3.2-3B). The E004 exact-repetition result (a non-garden-pathed second GP copy adds little object priming) also needs replication.

## Held-out materials (48 families, never used in discovery)

- SyntaxGym `npz_ambig`, 24 items (Futrell et al. 2019 / Hu et al. 2020; MIT). NB/NC use the **authors'** non-object verbs.
- Ceháková & Chromý 2025, 24 NP/Z items (CC-BY-4.0). Reflexive-absolute verbs and long NPs (`the mother who was afraid`).
- 15/48 share an ambiguous verb with a discovery family (flagged `verb_overlap_with_discovery`; sensitivity analysis excludes them).
- Targets are the same 93 discovery families: same instrument, new primes. Conditions: GP, CUE, TB, TC, NB, NC and exact doubles X>X.

## Frozen prediction rule (applied per model by `analyze.py --predict_only` from discovery outputs; predictions.json entries are written once, before that model's held-out scoring, and never overwritten)

For every model with both discovery (E002) and held-out (E005) data:
- **P1 (commitment):** if discovery b_obj has t ≥ 2, predict held-out b_obj > 0.
- **P2 (prediction error):** if discovery b_gpsurp has t ≤ −2, predict held-out b_gpsurp < 0. If t ≥ 2, predict > 0.
- **P3 (net sign):** if the discovery A 95% CI excludes 0, predict the same sign for held-out A.
- **P4 (history):** if discovery E004 data exist **and** P3 predicts A > 0 (there is a positive residue to lose), predict held-out r_inc (= dA/dAfull) < held-out rA1.

Same regression as discovery: `A ~ z(obj_expect) + z(gp_strength)` (OLS over prime families). One-sided tests at α = .05 for P1/P2 (t > 1.645); P3 conservatively requires the two-sided 95% bootstrap CI to exclude 0 in the predicted direction; P4 is a point-estimate comparison. **Primary summary:** the proportion of confirmed predictions across models, plus a pooled test per prediction type (models as replicates, sign test). No family exclusion based on model behaviour. Additional families or models may be added later only as a separately labelled extension.

## What would change our understanding

- P1 and P2 both replicate → the van Gompel-style residue and error-driven adaptation are dissociable, co-occurring forces. Their balance, not a binary "does the misparse linger?", is the object of study.
- P1 replicates, P2 fails → the negative A in strong models is not error-driven at the item level; look for construction-level adaptation instead.
- P2 replicates, P1 fails → "residual commitment" was a verb-property artefact of the discovery set.
- Neither replicates → the item-level structure is set-specific. Keep only the net-effect descriptions.

## Final frozen-rule results (17 models; analysed 2026-10-23; rule and predictions unchanged)

The held-out scores for all 17 models existed by 2026-10-12, but only the 8-model interim below had been reported. Full panel, `exclude_overlap = False` (primary):

| Prediction (held-out, between-family, S measure) | confirmed / predicted | sign test |
|---|---|---|
| P1 commitment slope > 0 | **5/12** | p = .61 (fails) |
| P2 error slope sign as predicted | **8/13** | p = .002 |
| P3 net A sign as predicted | 4/7 | p = .23 |
| P4 history | 2/2 | p = .25 |

With overlapping lexical material excluded: P1 4/12, P2 4/13, P3 4/7, P4 2/2.

**Scale extension (2026-10-23; 20 models: + Gemma-2-9B, Qwen2.5-32B, Qwen3-32B, each with predictions frozen by `scale_lane.sh` before its held-out scoring):** P1 **6/15** (p = .50), P2 **9/15** (p = .0005), P3 5/9, P4 2/3. With overlap excluded: P1 4/15, P2 5/15, P3 5/9, P4 2/3. The verdict above is unchanged.

**Reading:** with the full panel, the frozen between-family held-out test confirms the error force only weakly and **does not confirm the commitment force on S**. This agrees with the item-level summary in CURRENT_UNDERSTANDING (commitment slope on S > 0 in only 8/17 held-out). The commitment force is reliable on the production-like measure L (13/17 held-out, 15–18/17–18 elsewhere), not on S. The 8-model interim (14/18) overstated the held-out support, and this table supersedes it. A within-family causal test of commitment is E014.

## Interim results (8 models; frozen rule unchanged)

14/18 predictions confirmed: P1 commitment 5/7, P2 error 3/4, P3 net sign 4/5, P4 history 2/2. Failures, reported as-is: Llama-3.2-3B P2 (held-out b_gp t = −0.85); Pythia-2.8b P1 (b_obj ≈ 0); Qwen2.5-0.5B P3 (A = +0.09, predicted negative); Qwen2.5-3B P1 (this model already failed the discovery instrument check, Afull < 0).

**Post-hoc diagnostic (not part of the confirmation):** the two held-out sources differ strongly in object expectation at the verb (Ceháková reflexive-absolute verbs ≈ −0.3; SyntaxGym ≈ +1.5), so pooled between-family slopes partly encode a source contrast, and each source alone has only n = 24. With source fixed effects, the error slope is negative in Pythia-1.4b, Pythia-2.8b, Qwen2.5-0.5B and GPT-2 (t = −2.3 to −3.6). In Llama-3.2-3B it is null within both sources. Between-family item regressions at n ≈ 24 per source are fragile; within-family manipulations (E004, E006) carry more weight.
