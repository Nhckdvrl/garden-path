# Pilot A — what survives: local wrong attachment vs disrupted sentence-wide interpretation?

> **Status note (2026-10-13):** this plan was the starting design. Pilot B (misparse priming) was executed as E001–E012, and Pilot A's comprehension question was partly pursued in E003. The project is now **PAUSED**. Current results: [experiment index](experiments/README.md), [current understanding](CURRENT_UNDERSTANDING.md), [pause handoff](PAUSE_HANDOFF_2026-10-13.md). The text below is kept as the original design record.


**Pre-experiment DESIGN DRAFT v0.2 (2026-10-12).** Human→LLM translation may be a contribution; detailed explanatory topology is a *stretch question*, not a mandatory prerequisite. [Data/sample-size strategy](DATA_STRATEGY.md). Not preregistered/frozen. No data have been newly collected, evaluated or run. [Rationale](RESEARCH_PLAN.md), [semantic measurement contract](MEASUREMENT_PROTOCOL.md), [closest existing result](../imports/ssn-incremental-revision/README.md).

## A1. Core estimand (cannot be reduced to “final question also wrong”)

Ceháková–Chromý 2025 already demonstrates **noninitial-region GP comprehension damage** in humans, and SSN E70/E82/E107 already reports incomplete LM role revision. We specifically test whether the *shape* of damage follows **relational dependency structure** (and can predict out-of-sample items), rather than merely local erroneous attachment, generalized sentence difficulty, lexical plausibility or prompting.

The sought explanatory claim is a **predictive boundary**, not “LLMs have lingering errors” and not “models cannot form global semantics”.

## A2. Source items and cells

- Start with published Ceháková–Chromý 2025: 24 NP/Z + 24 MV/RR lexical families (metadata audited in imported `D0-Cehakova2025-source-audit.json`: 48 families, 8 source conditions per family). Read the exact original source and clarify condition/gold mapping before extracting; do not assume all eight forms are minimal pairs.
- Check candidate natural English with blinded native-level audit; source preserved byte-exact; repaired entries get new `derived_item_id` with full provenance rather than overwriting originals.
- Use a balanced GP/cue pairing as primary; ambiguous source and its cue version describe the *same asserted core relations*. For MV/RR, ensure passive/reduced-relative paraphrase is actually grammatical and semantically comparable.
- Add a small **matched difficult non-GP control** with similar clause count, lexical frequency, question complexity and length. It serves as falsification control, not an opportunity to optimize a benchmark.
- First do a *technical smoke* on ~20–40 mixed families (small for debugging, not a science result). For discovery prefer **all qualified original published families** in relevant construction(s); use the released 24+24 Ceháková and 69/40/40/40 Amouyal materials where their exact semantic task and control condition fit. If precision or needed controls are insufficient, expand with **natural independently sourced lexical families** guided by observed family variance and minimum worthwhile effects; do not require an arbitrary fixed expansion, and do not prematurely conclude from ~12 items.

## A3. Four source-grounded probe roles

For each sentence, prepare independently validated questions or a structured content output about:

1. `OBSOLETE` — original plausible but no-longer-source-supported relation (label **NOT_ENTAILED** if logically possible; don't call it contradictory).
2. `FINAL` — positively asserted dependency that exists only under final parse (e.g., late verb subject).
3. `INDEPENDENT` — a separate, explicitly supported fact whose event/participants do not depend on the obsolete link, matched in test difficulty and word position.
4. `BRIDGE` — a downstream use that requires integrating **two positively supported relations** (one may depend on the disambiguated role). Do not mark a guessed causality/real-world event as entailed.

To separate graph dependence from linear token distance, construct at least a 2×2 cross of `relationally dependent/independent` × `near/far in tokens` where grammatical. Source edits must not accidentally change other gold claims. A bridge dependency is tested with a **counterfactual source perturbation** of one relevant supported relation while holding the rest fixed; successful propagation requires the target answer to change accordingly.

A result 'BRIDGE fails more' is NOT by itself evidence of global fragmentation: it may simply inherit an error in the old relation. The key is to ask whether the new behavioral profile remains beyond what a *local error account* predicts, with matched untouched relationships and changed-basis counterfactuals.

## A4. Non-exclusive competing predictions

| Account | Obsolete role | Final role | Independent role | Bridge / changed relation |
| --- | --- | --- | --- | --- |
| Local lingering | Often incorrect | Usually recovers or weakly impaired | Mostly preserved | Impaired chiefly if bridge actually depends on misattached role |
| Broad construction/coordination failure | Incorrect or omitted | Errors can appear | Errors even when no graph dependence (after matching) | Excess impairment beyond local dependency-only projection |
| Question/answer bias | Strongly sensitive to polar framing | Output-format dependent | Similar instability under equivalent prompts | Errors shrink/rearrange across independent-native readouts |
| General difficulty | GP effect tracks syntactic complexity/length | Same | Similar in difficult nonGP controls | Predictable by difficulty matched controls |

These patterns are **hypotheses, not reported findings**. They may coexist or fail.

## A5. Instrument procedure

1. Blind verify source and all role/event questions as `ENTAILED / CONTRADICTED / NOT_ENTAILED / UNRESOLVED`. Independent annotators or a documented adjudication protocol; don't use assessed model as its own gold judge.
2. Validate baseline cues and model actual free answers. Include positive-control simple questions, option-order balanced choices and an independently run paraphrase; report invalid, cap and response-parsing errors.
3. Run separate fresh contexts for each question (same source, no previous QA transcript), and a separate free paraphrase context. Do not answer multiple questions serially for primary effects.
4. Freeze stimulus family IDs, item maps, exact question wording and candidate models/revisions before observing scientific outcomes. Analyze all qualifying families; no outcome-based subset.
5. Compute family-paired condition contrasts for each probe class, plus difference-in-differences on matched dependency proximity and complexity controls. Plot model-specific item profiles and use family-cluster bootstrap; code and seeds frozen before confirmatory hold-out.
6. Once a candidate account emerges, formulate its **out-of-sample prediction** on a distinct construction or unseen lexical families. Confirm without changing scoring after the result.

**Primary planned estimand** (not yet frozen): an extra GP-specific error contrast for independent and bridged relations **relative to local obsolete-binding errors**, after nonGP difficult controls and label-validity checks. The concrete functional form must be selected **before** the discovery test is executed. Predeclared secondary readouts: omission vs wrong binding, candidate-free production, within-family response invariance and source intervention direction.

## A6. Strong falsification / stop

- If a reliable modern-LLM adaptation of the 2025 *human* multi-region effect occurs, that may already be valuable; situate it against the earlier SSN LLM evidence and all directly overlapping LM papers. **Do not claim a new global-fragmentation mechanism without evidence**, but also do not automatically reject the cross-system contribution.
- If GP and cue differ only for polar Yes/No, or source-gold labels are unstable, the result is measurement-limited.
- If the new pattern appears just as strongly for nonGP difficult sentences, downgrade GP-specificity.
- If BRIDGE defects are completely predicted by local wrong dependencies without independent residual, stop the fragmentation story; examine local error account, don't add SAE just to save it.
- If it is one-model/one-verb-family/post-hoc subgroup only, report it as discovery and reserve hold-out evidence before any stronger claim.

## A7. Historical baseline to avoid repeating

[SSN E69](https://github.com/Nhckdvrl/ssn-group-papaer/blob/main/workbench/incremental-interpretation-revision/experiments/E69-plausibility-versus-structural-revision.md): plausibility already probed. [E80](https://github.com/Nhckdvrl/ssn-group-papaer/blob/main/workbench/incremental-interpretation-revision/experiments/E80-grammar-trust-and-noisy-interpretation.md): trust prompt already probed. [E87](https://github.com/Nhckdvrl/ssn-group-papaer/blob/main/workbench/incremental-interpretation-revision/experiments/E87-actual-answer-versus-forced-choice.md): actual-vs-forced output audited. [E107](https://github.com/Nhckdvrl/ssn-group-papaer/blob/main/workbench/incremental-interpretation-revision/experiments/E107-critical-dependency-commitment-audit.md): omission vs explicit final link distinguished. **Our new factor is explanatory dependency topology and out-of-sample prediction, not any one of these readouts alone.**
