# SSN incremental-interpretation-revision asset import

Imported 2026-10-12 from [ssn-group-papaer](https://github.com/Nhckdvrl/ssn-group-papaer/tree/main/workbench/incremental-interpretation-revision). **This is a provenance-preserving historical import, not a resumption of that workbench and not a new experiment.** The primary working repo is now [garden-path](https://github.com/Nhckdvrl/garden-path).

## What is actually in this repository

- `results/D0-Amouyal-released-item-type-audit.json` — task semantics, original answer polarity and non-entailment audit.
- `results/D0-Cehakova2025-source-audit.json` — 2025 Zenodo stimulus metadata/hash and source task encoding (0=Yes, 1=No); **not** the stimulus archive itself.
- `results/E52-reading-map-summary.json` — historical multi-model behavioral map (originally 1,732 QA / 309 pairs / 14 models / 5 families); check embedded scope/completeness and experiment card before quoting statistics.
- `results/E82-current-open-model-summary.json` and `E87-actual-answer-summary.json` — **POINTER JSON FILES**, not numeric results. The original large summaries live at the paths/SHAs specified inside them.
- `results/E107-critical-dependency-summary.json` — limited candidate-pool/role-audit summaries with original map path and SHA. A comparison conditional on eligible candidate pairs is not a population-level successful-revision rate.
- `scripts/data_v2.py`, `step_gp_audit.py`, `role_reference.py`, `analyze_reading_map.py`, `analyze_critical_dependency_commitment.py` — historical research code, retained **unchanged**, not a stand-alone executable pipeline. They may import other modules, require external result files, or depend on local model configs.

The scientifically important prior experiments, **not duplicated wholesale**, remain in [old experiment registry](https://github.com/Nhckdvrl/ssn-group-papaer/tree/main/workbench/incremental-interpretation-revision/experiments). Read the [old exploration summary](https://github.com/Nhckdvrl/ssn-group-papaer/blob/main/workbench/incremental-interpretation-revision/EXPLORATION_SUMMARY.md) first.

## What is NOT transferred

- Raw inference logs, Step Plan responses, all model checkpoints, third-party stimulus zip archives and large completed maps whose source repo has only externalized pointers.
- Absence from the new GitHub tree must NOT be reinterpreted as a missing historical experiment or a zero result.
- The old machine path (`/data1/xiangding/work/incremental-interpretation-revision/`) is **historical**, not verified accessible from `/home/xiang/garden-path`.
- Old workbench E00–E108 cards, scripts and historical revisions are left in place and remain the authoritative provenance for earlier work.

## Findings and constraints inherited as *previous* evidence

| Experiment | Historical takeaway | What it does NOT warrant |
| --- | --- | --- |
| [E52](https://github.com/Nhckdvrl/ssn-group-papaer/blob/main/workbench/incremental-interpretation-revision/experiments/E52-genuine-revision-reading-map.md) | Broad model panel and question-semantic confounds | A uniform latent parsing mechanism |
| [E59](https://github.com/Nhckdvrl/ssn-group-papaer/blob/main/workbench/incremental-interpretation-revision/experiments/E59-source-grounding-versus-world-question.md) | Some real source-grounded deficits survive clarification | That every original 'No' is a logical contradiction |
| [E69](https://github.com/Nhckdvrl/ssn-group-papaer/blob/main/workbench/incremental-interpretation-revision/experiments/E69-plausibility-versus-structural-revision.md) | Plausibility affects GP and cues, heterogeneously | A newly discovered good-enough mechanism |
| [E80](https://github.com/Nhckdvrl/ssn-group-papaer/blob/main/workbench/incremental-interpretation-revision/experiments/E80-grammar-trust-and-noisy-interpretation.md) | Trust/noise metadata shifts answers without reliable joint restoration | A calibrated Bayesian noisy-channel or model-wide fix |
| [E82/E87](https://github.com/Nhckdvrl/ssn-group-papaer/blob/main/workbench/incremental-interpretation-revision/experiments/E87-actual-answer-versus-forced-choice.md) | Some errors survive actual generation rather than only forced-choice probes | Every forced-choice number is an actual production failure |
| [E98/E99](https://github.com/Nhckdvrl/ssn-group-papaer/blob/main/workbench/incremental-interpretation-revision/experiments/E98-query-guidance-versus-interpretation-fidelity.md) | Some source-level QA/role dissociations; no stable cross-family QA improvement in the newer panel | That task success generally corrupts meaning |
| [E107](https://github.com/Nhckdvrl/ssn-group-papaer/blob/main/workbench/incremental-interpretation-revision/experiments/E107-critical-dependency-commitment-audit.md) | Deleting an old relation is not the same as explicitly installing a correct new dependency | Broad validated full-semantic repair |

## Migration standard

1. Use exact source links, original protocol, paired structure and SHA; do not quietly relabel old prompts as new ones.
2. Reuse semantic category definitions only after verifying target construction and logical entailment; DO NOT score 'not asserted' as 'contradicted'.
3. A new preregistered pilot must use **new IDs**, read the historical failure ledger, and state why its estimand was not answered before.
4. The imported reading cards in `library/papers/` retain their original reading-scope disclaimers; they have not all been independently re-read in this session.
