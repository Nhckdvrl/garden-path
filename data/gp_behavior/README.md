# Garden Path source-data registry — raw vs candidate vs approved

**Status 2026-10-12:** We have original published stimulus CSVs and **189 paired families**, but **no new audited runnable behavioral pilot items, no new model run, and no confirmed scientific finding**. Do not confuse these three levels.

1. **Immutable original data:** [Amouyal et al. published sources](upstream/amouyal/), pinned to upstream commit `072efefa01cb9716c2d14752eb1d4bf9830b0b81`. Four exact source CSVs plus source repository MIT license and [manifest](upstream/amouyal/SOURCE_MANIFEST.json).
2. **Unreviewed derived candidates:** [candidate directory](candidates/README.md). 189 lexical family GP/CUE pairs = **378 source-condition records**; every semantic gold is `UNRESOLVED`, every source review is `PENDING`. These are NOT eligible model-test inputs.
3. **Source-grounded study items:** **NONE yet qualified**. Requires independent human/linguistic review of acceptability, exact disambiguation position, entailment/role and new `INDEPENDENT` plus `BRIDGE` claims.
4. **New GP model inference:** **NONE**. SSN E52/E80/E107 are historical and not repeated.

## Upstream source inventory

| Construction | Lexical families | Original QA rows | Distinct GP/CUE source records | Type of author-provided nonGP control |
|---|---:|---:|---:|---|
| NP/Z | 69 | 276 | 138 | `REORDERED`: clause order changes; not merely comma |
| NP/S | 40 | 160 | 80 | `OVERT_THAT`: complementizer appears |
| MV/RR | 40 | 160 | 80 | `UNREDUCED_RC`: overt relative clause, morphology and length altered |
| NP/VP | 40 | 160 | 80 | `MORPHOLOGY`: morphosyntactic disambiguation |
| **Total** | **189** | **756** | **378** | **Four intervention classes; not one pooled comma experiment** |

The study's `upstream_correct_answer="No"` is a **task scoring label**, not proof that an unasserted event was logically contradicted. `NOT_ENTAILED`, `CONTRADICTED` and `ENTAILED` must stay distinct.

## Reproduction and science gates

- Exact upstream Git object hashes and 378 generated pending records are checked by `python3 research/tools/verify_upstream_candidates.py`.
- Candidate generator: `python3 research/tools/build_amouyal_candidates.py --source data/gp_behavior/upstream/amouyal --output /tmp/pending.jsonl`. It creates **one combined file**; checked-in candidate files are partitioned by construction.
- Structural-only inspection: `python3 research/tools/validate_manifest.py --pilot A --allow-pending data/gp_behavior/candidates/amouyal_nps_v0_pending.jsonl`. Without `--allow-pending`, pending inputs are rejected intentionally.
- GitHub Actions runs offline unit tests plus exact source/candidate audit. **CI pass is engineering validity, not linguistic/semantic correctness or a scientific result.**
- Make versioned accepted manifests, preserve raw bytes, provenance and human review; never silently replace upstream Gold or select examples based on model success.

## Other source and provenance boundaries

- Ceháková & Chromý 2025 English NP/Z/MV-RR: [Zenodo source metadata](https://zenodo.org/records/16358492) and [historical audit](../../imports/ssn-incremental-revision/results/D0-Cehakova2025-source-audit.json) only; original Stimuli.zip is **not mounted or committed**.
- Ceháková & Chromý 2026 human Czech cloze/RT study is *different*, not the same materials (see [deep reading](../../library/papers/psychometrics/cehakova-chromy2026-cloze-vs-surprisal.md)).
- [Prime-LM 2022](https://aclanthology.org/2022.tacl-1.60/) describes priming measures; there is no ready-to-use four-cell Garden Path target panel here.
- Large SSN experiment maps and some summaries are externalized pointers, not full numerical output files. [Old asset manifest](../../imports/ssn-incremental-revision/README.md).
- Original `garden-path` G0–G33 research data refer to prospective evidence exclusion, **not syntactic Garden Path**; preserve frozen historical data/results untouched.

**Next gate:** Audit source syntax and original source truth; design and blind-review independent versus graph-dependent probes. **Pilot B cannot use REORDERED NP/Z source controls to estimate a clean comma/punctuation effect.** See [measurement contract](../../research/MEASUREMENT_PROTOCOL.md) and the [two distinct pilot designs](../../research/RESEARCH_PLAN.md).
