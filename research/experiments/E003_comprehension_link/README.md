# E003 — Lingering misinterpretation vs misparse priming on the *same* human items

**Status:** v2 design, 2026-10-12. Not yet run (GPU: per the user, waits for freed cards; no extra cards). Owner: this session. E001/E002/E004 belong to the parallel session; E003 reads nothing from them except, optionally, per-family A for the Amouyal subset.

## Why the design changed (v1 → v2, before any E003 data existed)

v1 used Amouyal's 69 NP/Z families with one Yes/No question. A literature check before running changed this:
- **Christianson et al. 2001** (full text read) published the canonical items *with* the manipulations that carry diagnostic information: ambiguous-region **length** (*the deer that was brown and graceful*), **plausibility** of the misinterpretation (*ran into the woods* vs *paced in the zoo*), a natural no-comma **control** (*hunted the pheasant the deer…*), and a **verb class** contrast (optionally transitive OT vs reflexive absolute transitive RAT, where pragmatic inference to the object is blocked). Human rates for each condition are reported (Tables 2, 3, 7).
- **van Gompel et al. 2006**, Exp. 2: plausibility did **not** modulate misparse *priming*. Christianson: plausibility **does** modulate lingering *comprehension*. In humans, the two residues respond differently to the same manipulation.
- **Fujita & Cunnings 2020** (Applied Psycholinguistics): structural priming and lingering comprehension errors in the same design; priming changed reading times but not comprehension accuracy. Another human dissociation.

So the right high-information experiment uses the 54 Christianson families and measures **both residues, plus garden-path strength, on every cell**. The question is no longer just "do they correlate?" but **"do they respond to the same manipulations, the way humans' do or don't?"**

## Materials (data/gp_behavior/derived/christianson2001_families_v1.jsonl; 42 OT + 12 RAT)

Sentence forms per family × length (S/L) × plausibility (P/I; OT only):

| Form | Example (OT1, short, plausible) | Role |
|---|---|---|
| GP | While the man hunted the deer ran into the woods. | target condition |
| CUE | While the man hunted, the deer ran into the woods. | comma control (van Gompel) |
| CTL | While the man hunted the pheasant the deer ran into the woods. | Christianson's control: no comma, V has its own object |
| TB / TC | …hunted the deer (,) it ran into the woods. | genuinely transitive reference |
| NB / NC | While the man slept (,) the deer ran into the woods. | strictly intransitive verb (priming A only) |
| REORD | The deer ran into the woods while the man hunted. | Christianson Exp. 3 control |

## Readouts (all per family × cell, saved unaggregated)

1. **Comprehension:** logodds(Yes) − logodds(No) for OBS (*Did the man hunt the deer?*) and FINAL (*Did the deer run into the woods?*). Two question sets (author wording; uniform template *Is it true that …?*), two prompt formats (plain; chat template), and both answer orders in the instruction.
2. **Priming:** prime → E001 target families (content-disjoint). Target comma-placement `L` and target GP surprisal `S`. Per-family A = (GP−NB) − (CUE−NC), plus GP−CTL and GP−TB.
3. **Garden-path strength in the sentence itself:** disambiguating-word surprisal GP vs CUE per cell; object expectation at the verb.

## Key comparisons and what each would tell us

| Comparison | Human result | If an LM matches | If it differs |
|---|---|---|---|
| comp: GP − CTL, GP − CUE (OBS) | GP > CTL | human-like lingering on canonical items | — |
| comp: long > short; plausible > implausible | both main effects (Exp. 1a/1b) | residue sensitive to commitment duration and to semantics | — |
| priming A: long > short | weak, mixed (van Gompel Exp. 1) | — | — |
| priming A: plausible vs implausible | **no difference** (van Gompel Exp. 2) | priming is structural, comprehension is semantic: two residues | if LM priming *is* plausibility-sensitive, its residue is semantic, not human-like |
| RAT vs OT, CUE/REORD baseline | OT control 49% vs RAT 12.5%; GP high for both | LM separates pragmatic inference from syntactic lingering | — |
| comp fraction (GP−CUE)/(TC−CUE) vs priming fraction rA | unknown in humans | — | a quantitative LM-internal comparison of the two residues |
| item level: corr(A, comp residue) within cell | unknown | one shared residue | dissociation |

Positive controls: FINAL logodds in CUE > 0; OBS logodds in TC > OBS logodds in CUE. Models failing these are reported but not interpreted. Unit = family (42 OT; RAT analysed separately, n = 12, descriptive). Inference by family bootstrap; for priming, two-way bootstrap over prime × target families.

## Known limitations recorded up front

- Christianson's implausible items are human-authored; some remain fairly plausible (e.g. *played on the phonograph*). We use them as published.
- TB/TC use a resumptive pronoun (*it/they*), so they are a structural reference, not a natural sentence class.
- Base models answering Yes/No are a weak instrument. The positive controls decide which models count.

## Addition before any E003 data (2026-10-12): within-family cell-level slopes

The parallel session reports a two-force pattern in E005 (held-out): priming rises with commitment (object expectation at V) and falls with the disambiguation error (garden-path surprisal). E003's length and plausibility manipulations change the garden-path surprisal *within a family* (same verb, same NP), so they give a within-family test of the error force. Added to `analyze_v2.py`:
- per (family, cell): A on S, comprehension lingering (GP − CUE on OBS_author), gp_eff = lp(CUE_dis) − lp(GP_dis);
- family-demeaned slopes of A on gp_eff and of lingering on gp_eff (family bootstrap).

Prediction under the two-force account: slope(A) < 0. Human-like comprehension predicts slope(lingering) > 0, since in humans harder or longer garden paths leave *more* lingering. Opposite signs would be a clean dissociation of the two residues. A pipeline smoke test (GPT-2, CPU, 4 OT + 3 RAT families, 6 targets) ran end to end. Its numbers are not results.

## Second addition before data (2026-10-12): commitment confound and the prefix-matched test

Raised by the parallel session: length and plausibility can move commitment *over the NP* (digging-in) together with gp_eff. The two forces predict opposite signs on A, so the family-demeaned slope is a **net** effect. A slope < 0 supports error dominance; a slope ≥ 0 does not refute the error force. Two fixes, both specified before data:
1. **Prefix-matched slope (primary within-family test).** Christianson's plausibility manipulation changes only the main-clause *continuation*, so within (family, length) the GP prefix, and hence commitment over the NP, is identical. Demeaning by family × length leaves only the P/I variation in gp_eff. This is the same logic as E006, on human-normed items.
2. **Commitment covariate.** `commit_end = log(P(",") + P("."))` at the end of the ambiguous region (probes NPend_comma / NPend_period). It enters a two-covariate family-demeaned regression with gp_eff. Interpretive caveat: P/I differ in semantic plausibility as well as surprisal, so the prefix-matched slope is "error + plausibility of the misreading". It cannot separate those two.

## Running log (exploratory; models analysed as they finish)

- 2026-10-12, after 4 models: an interim statement to the user, "LM lingering is insensitive to plausibility, unlike humans", was **wrong** and has been corrected. The original `plaus_eff` was the difference-in-differences `(GP−CUE)_P − (GP−CUE)_I`, which is ≈ 0. The simple GP plausibility effect is positive and human-like in direction (Mistral-7B +0.42 [0.22, 0.61], Llama-3.1-8B-Instruct +1.76 [1.10, 2.44] logodds). It is about equally large in CUE, REORD and even TC, where the hunting is *asserted*. So in these models plausibility acts as an additive world-knowledge prior on the answer, not as a GP-specific correction. Christianson varied plausibility only in GP items (controls were plausible only), so the human interaction is unknown. Stats renamed: `plaus_x_GPCUE` (DiD), `plaus_GP/CUE/TC/REORD` (simple effects); `plaus_check.py` prints all forms.

## E003b — does rereading / processing history change lingering? (designed 2026-10-12, before data)

Motivation from E003 so far: in instruction-following models lingering is far larger than in humans (Llama-3.1-8B-Instruct P(yes) ≈ 0.87–1.00 vs human 0.29–0.44), and the final relation is also weakened. E004 (parallel session) showed that an exact second copy of a GP sentence is not garden-pathed. That gives a clean processing-history manipulation for *comprehension*. Runner: `run_reread.py`; output `results/gp/E003b/`. Same 192 cells, OBS/FINAL × author/template questions × 2 formats × 2 answer orders.

Presentations: GP1, GP2 (read again), CUE1, CUE2, GP_CUE (GP then the punctuated version), CUE_GP, QFIRST_GP / QFIRST_CUE (question before the sentence; cf. Christianson 2024 Exp. 2), TC1.

| Account of LM lingering | GP2 − GP1 (vs CUE2 − CUE1) | GP_CUE vs CUE1 | QFIRST_GP vs GP1 |
|---|---|---|---|
| Processing-episode residue (states built under the object analysis) | lingering drops | ≈ CUE1 | lingering drops if the question changes how the NP is encoded |
| Surface / lexical match to the adjacent string *hunted the deer* | no drop (or rise: two matches) | stays above CUE1 | no change |
| Final parse never built (incomplete reanalysis; string-level repetition adds no information) | no drop | ≈ CUE1 (punctuation supplies the parse) | no change |

Primary statistic: `reread = (GP2 − GP1) − (CUE2 − CUE1)` on OBS (author), family bootstrap, per model. Secondary: the same on FINAL (sign flipped: does rereading restore the final relation?), and GP_CUE − CUE1.
