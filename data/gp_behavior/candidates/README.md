# Garden Path candidate rows (PENDING — NOT EXPERIMENT GOLD)

Generated from Amouyal et al. public sources, upstream commit `072efefa01cb9716c2d14752eb1d4bf9830b0b81`. See [source registry](../README.md) and [candidate audit manifest](AMOUYAL_PENDING_AUDIT.json).

| File | Construction | Paired families | Source-condition rows |
|---|---|---:|---:|
| `amouyal_extended_v0_pending.jsonl` | NP/Z, reordered control | 69 | 138 |
| `amouyal_nps_v0_pending.jsonl` | NP/S, overt-that control | 40 | 80 |
| `amouyal_rr_v0_pending.jsonl` | MV/RR, unreduced relative | 40 | 80 |
| `amouyal_npvp_v0_pending.jsonl` | NP/VP, morphological control | 40 | 80 |

Records contain the authors' original `question` and `upstream_correct_answer`, **not** our own verified source-entailment labels. Every `gold_claims[].truth_status` is `UNRESOLVED`, `predicate` is `UNREVIEWED`, and all `review_status` are `PENDING`. Independent and bridge claims must be constructed and independently audited. Disambiguators are candidates, not verified positions.

Only structural inspection with `--allow-pending` is permitted. Analysis/inference requires newly versioned, qualified, frozen manifests with audited grammar, controlled targets, source entailment, actual independent claim and relationally dependent target; no output-based exclusions.

Do not overwrite these candidates. Keep all original IDs and source URLs. Pair/bootstrap by independent lexical `family_id`, not the 756 original question rows or the 378 condition records.
