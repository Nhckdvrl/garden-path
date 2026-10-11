# Literature ledger and audit rubric

**Updated 2026-10-12.** This entry records which assets *exist*, not that every article has been completely reread. There are 36 imported SSN note files with the original source-provenance header; the number of imported note files is not the number of newly read full articles.

## Read-status vocabulary

- `VERIFIED_FULL_MAIN`: explicitly verified body from introduction to conclusion; appendices may be only partial.
- `VERIFIED_SELECTED_SECTIONS`: precisely named sections only.
- `PRIMARY_ABSTRACT_META`: publisher/arXiv/Anthology abstract and official metadata, perhaps accessible excerpts; cannot support quantitative-method details absent from the excerpt.
- `IMPORTED_SCOPE`: an earlier team note preserves its own explicit scope; import itself is **not** rereading.
- `OPEN_READING_DEBT`: hypothesis or paper needs full body/tables/appendix before operationalization.

The 36 imported paper cards each begin with `IMPORTED_SCOPE` and preserve their own original-specific status. Cross-reference the original SSN reading ledger if verification scope matters: [legacy research theme](https://github.com/Nhckdvrl/ssn-group-papaer/tree/main/library/themes/incremental-language-processing).

## Highest-priority anchor reading debt

| Paper | Present evidence status | Missing / decision it affects |
| --- | --- | --- |
| Ceháková & Chromý 2025 | `IMPORTED_SCOPE`: original card explicitly says primary abstract/introduction/method excerpts | Full results/tables for errors in noninitial region, measurement independence, material variants; essential for PILOT-A |
| Ceháková & Chromý 2026 | `PRIMARY_ABSTRACT_META` + intro/discussion excerpts | Exact cloze collection, predictor construction, human sample and mixed-effects; explanatory model baselines |
| van Gompel et al. 2006 | `IMPORTED_SCOPE` abstract/introduction excerpts | Exact prime/target definitions, target transitivity metric and exclusions; essential for PILOT-B |
| Sinclair et al. TACL 2022 | `IMPORTED_SCOPE` from team + primary public article/README | PE metric definition, control contrasts, model scoring adaptation |
| Sinclair et al. JML 2026 | `IMPORTED_SCOPE` abstract/intro/method snippets | Full 41 pages, item-level priming effects, word-order vs hierarchy control |
| Pucci et al. 2026 | `IMPORTED_SCOPE` selected sections + abstract | Free-production classifier and negative controls; do not rely on its figures alone |
| Amouyal ACL 2025/2026 | `IMPORTED_SCOPE` original main-text notes | Recheck prompt-order averaging, actual gold definition, open data version, distinct constructions |
| Hanna & Mueller NAACL 2025 | `IMPORTED_SCOPE` original main/selected appendix | Feature faithfulness and action task constraints; mechanism only if later justified |
| Zhou et al. 2026 | `PRIMARY_ABSTRACT_META` | Full SBU definition and within-construction generalization claims |
| Bates 2025 blog | `VERIFIED_SELECTED_SECTIONS` article main body as indexed | Code and independent replication; blog result not peer-reviewed |
| Clark et al. CoNLL 2026 | `IMPORTED_SCOPE` original main and selected appendices | Full other appendices and machine-readable data |
| Yoshida ACL 2026 | `IMPORTED_SCOPE` original main and limitations | Fine-tuning intervention/RT prediction distinctions |

## Every future paper card must include

1. Exact title/authors/venue/year/revision/source URL, *and verified read scope*.
2. Scientific object, actual dependent variable and target population/model.
3. Parent claim and why it did not explain an observed fact.
4. Explicit author-stated motivation versus our **RECONSTRUCTED** idea path.
5. At least two competing hypotheses, their differential predictions and the paper's decisive experimental manipulation.
6. Dataset selection, sample size **unit**, exclusions, model families, model versions, output format and controls.
7. What its result licenses versus what it demonstrably does *not* license.
8. Nearest 3–5 studies: concrete shared claims and nontrivial distance.
9. The single most information-gaining experiment that could have come next, with possible refuting outcome.
10. Reuse conditions, data/code/hash/rights where available.

## Literature update rule

Do not concatenate endless short annotations into a false 'deep reading' count. To add a new full card, give a primary excerpt or verified paper artifact and complete fields above; if only abstract is available, put it in [new readings](NEW_READINGS_2026-10-12.md) and mark the debt. Re-evaluate the research plan when an accepted or high-quality neighboring paper changes the ownership boundary.
