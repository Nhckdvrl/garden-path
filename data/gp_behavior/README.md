# Syntax Garden Path stimulus provenance (new research)

**Not the old G0–G33 source directory.** This is the materials registry for the 2026-10-12 behavioral design. No freshly validated or frozen Garden Path item manifest has been produced, and no new GP model run has taken place.

## Canonical upstream sources

| Asset | Official source | Available here? | Reuse status |
| --- | --- | --- | --- |
| Ceháková & Chromý (2025) 48-item / 8-condition Czech? **No: this set is English NP/Z/MV-RR source stimuli** | [Zenodo 16358492](https://zenodo.org/records/16358492) | Metadata and hashes only, in [SSN audit](../../imports/ssn-incremental-revision/results/D0-Cehakova2025-source-audit.json) | Need exact original Stimuli.zip and its content/syntax audit before using |
| Amouyal 2025/26 stimuli & human/LLM released outcomes | [authors' GitHub](https://github.com/samsam3232/comparing_humans_llms_processing_difficulties) | SSN question-audit and E52 summary, **not** original complete row-level dataset | Pin upstream commit and verify split, prompt, gold semantics |
| SAP Benchmark Huang et al. 2024 | [source paper](https://www.sciencedirect.com/science/article/pii/S0749596X24000135) | No raw source in this repo | Only if comparing lexical surprisal or RT; different explanandum |
| Prime-LM Sinclair et al. TACL 2022 | [published paper](https://aclanthology.org/2022.tacl-1.60/) | Literature card only | Metric and target construction guidelines; not a pre-built GP prime panel |
| Ceháková & Chromý 2023 diverse representation experiment | [OSF](https://osf.io/98g26/) | Primary paper note only | Possible methodological reference; Czech task not automatically an English LM stimulus |

**Important provenance correction:** The 2025 Ceháková–Chromý dataset examined in our legacy SSN audit contains English-style NP/Z and reduced-relative sentence materials, but the authors' broader oeuvre also contains Czech stimulus corpora. A future ingestion must identify the *actual language* in each file rather than infer it from author affiliation. Material language/status in this manifest remains **unverified from raw files**; no task is eligible until audited.

Zenodo `Stimuli.zip` on 2025-07-23 record: MD5 `f8e5fba84c85bb03da9af928600b420d`; SHA256 inherited from SSN source audit `a6aefcd55945e195c26912bb386b3980272ab2b034fcf152911ce3e1b4fcd25d`; byte count 10891; experimental metadata states 48 item families and 8 experimental rows/family, plus fillers/practice. These are historical **source audit** facts, not current file verification. Direct archive download was rate-limited in the current environment; no copy of raw stimulus files has been committed.

## Before any new model run

1. Verify the source archive exactly (checksum and license), extract only permitted task stimuli and preserve source sentence ID/condition.
2. Semantic/gold check under [measurement contract](../../research/MEASUREMENT_PROTOCOL.md). Crucial: `NOT_ENTAILED` is not `CONTRADICTED`.
3. Build separate pilot A/B JSONL manifests with original/derived IDs, source/target roles, prior-clause dependency and lexical review. Run structural check:
   `python3 research/tools/validate_manifest.py --pilot A FILE.jsonl` or `--pilot B`.
4. Manual linguistic validity and accepted revision must be marked `PASSED` independent of student model results.
5. Freeze prompt/material/code hash, run positive controls first, and retain all failures without sample cherry-picking.

## Why not copy raw SSN files blindly?

The archived SSN workbench points to an external model/data directory `/data1/xiangding/work/incremental-interpretation-revision`, not currently verified as available in the new checkout. Some GitHub JSONs are pointers only. Materialized source rights and original version should be verified before copying; the reference source is identified above.
