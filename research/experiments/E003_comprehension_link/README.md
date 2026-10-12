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
- 2026-10-12: E003b gets a manipulation check before running (prompted by the parallel session's E002 finding that a sentence differing from the previous one only by a dropped comma is a *deviant copy* and is still garden-pathed). `<tag>.probes.csv` stores the disambiguator surprisal in GP1, CUE1, the second copy of GP2, CUE_GP and GP_CUE, in the same prompt frame. CUE_GP is interpreted only if its second-copy GP effect is near zero; GP_CUE and GP2 are the primary conditions.
- Mistral-Small-24B-Instruct is excluded from all panels: the local HF cache holds only 4/10 weight shards (the E002 run failed for the same reason). Re-downloading (~48 GB) needs user authorization.
- 2026-10-12, 16/21 models done (exploratory). **Second correction:** the interim claim "comprehension lingering is huge but the priming residue is small" holds only for the S measure (target GP surprisal, adaptation-like). On L (comma placement, production-like, the van Gompel analogue), the residue is large: rA_L = 0.89 (Llama-3.1-8B-Instruct), 0.96 (Mistral-7B), 0.70 (Gemma-3-12B-it), and A_L > 0 in 16/16 models (`report_for_E010.csv`). This matches the parallel session's frozen E010 card (scored there: D1 16/16, D3 14/16, D2 partially failed).
- **Family-level link** (`itemlink.py`; reliabilities ≥ .90, ceiling ≈ .96): corr(lingering, A_L) = −.31 (Mistral, CI excludes 0), −.25 (Qwen3-8B), −.16 (Llama-Instruct), +.14 (Gemma); corr(lingering, A_S) ≈ 0 in all four. Both residues are large on average, but the items with the most lingering are not the items with the most priming.
- **What drives each** (`item_predictors.py`): A_L tracks commitment at V (obj_expect, r = +.27 to +.59, 4/4 models). Lingering measured as GP − CUE correlates −.79 to −.95 with the CUE baseline, but this is largely a **shared-term + ceiling artefact**: P(yes | GP) = .74–.93 with about half the between-family SD of CUE. Using GP alone, the yes-rate correlates with the CUE baseline (+.45 to +.78; a pragmatic prior that V acted on NP) and not with obj_expect, gp_eff or A_L. Working interpretation (to be tested, not established): in LMs, yes/no lingering is a near-ceiling GP effect whose item variance is pragmatic, while production priming tracks syntactic commitment.

### E003b first results (2 instruction models; exploratory)

Manipulation check passes in both: GP1 disambiguator effect +9.8 (Gemma-3-12B-it) / +7.5 (Llama-3.1-8B-Instruct) nats. The second copy in GP2 **and in CUE_GP** is not garden-pathed (effect −4.7 to −6.3: the word is copied). So CUE_GP is valid for these models, unlike GPT-2/Pythia in E002.

OT, OBS_author (logodds, family bootstrap): GP1−CUE1 = +10.05 / +3.79. reread = **+3.56 / +1.15** (rereading *increases* lingering). GP_CUE−CUE1 = +6.90 / +2.62 (the punctuated version only partly corrects). CUE_GP−CUE1 = **+3.85 / −0.46** (the same two sentences in the other order: little or no lingering). qfirst = −3.29 / −2.59. FINAL is impaired in every condition that contains the GP string, including CUE_GP (−2.7 / −1.3).

Reading: with identical content, lingering depends on whether the GP string was processed with a garden path (GP first) or without one (after its disambiguated twin). Recency predicts the opposite order effect, and surface string match predicts none. **Open alternative: primacy / label role** ("Sentence:" holds GP in GP_CUE but CUE in CUE_GP), which predicts the same order effect. E003c separates them.

## E003c — processing history vs primacy (designed before data)

The GP sentence is always the labelled primary sentence, preceded by a context line that either removes the garden path without answering the question, or is neutral:
- `CTX_DIS`: "Context: The deer ran into the woods." → Sentence: GP (or CUE)
- `CTX_NEU`: "Context: The weather was mild that day." → Sentence: GP (or CUE)
- `CTX_REORD`: "Context: {REORD}" (full disambiguated paraphrase; still does not assert the obsolete relation)
- Neutral-label order test: "Version 1: X / Version 2: Y" for (GP, CUE) and (CUE, GP).
Statistic: `hist = [(GP−CUE) | CTX_DIS] − [(GP−CUE) | CTX_NEU]`. Processing history predicts hist < 0, tracking the per-family reduction in the disambiguator surprisal. Primacy predicts hist ≈ 0. Manipulation check: disambiguator surprisal in GP after each context.
- 2026-10-12 (16/22 models; `overview.py`, point estimates; Mistral-Small-24B failed to load because its cache is incomplete on fvcrc11, same as in E002). Six models pass both positive controls *and* give a clearly positive TC − CUE: gemma3-12b-it, llama3.1-8b-instruct, mistral-7b, qwen2.5-3b, qwen2.5-7b, qwen3-8b. In these six:
  1. **Comprehension lingering is strong and human-like.** GP is answered "Yes, he hunted the deer" at 39–86% of the level of a sentence that asserts it (frac 0.39–0.86). It grows with ambiguous-region length in all six (digging-in; e.g. Gemma-3-12B +4.8 logodds, Qwen3-8B +5.6), as in Christianson Exp. 1.
  2. **Priming residue is small**: A = 0.00–0.50 on S, and GP primes *less* than Christianson's control in 5/6 (GP − CTL < 0).
  3. **The two residues are unrelated at the item level.** Across the 42 OT families, Spearman r(lingering, A) = −0.08 … +0.15 in all six, although both are highly reliable (lingering author~template r = .89–.98; A split-half Spearman–Brown .90–.97). With n = 42, this rules out a moderate shared-residue correlation (|r| ≳ .35) in each model.
  4. **Error-driven priming on human-normed, prefix-matched items:** the within-(family, length) slope of A on gp_eff is negative in 6/6 (−0.06 … −0.13; CI excludes 0 in Mistral-7B and Qwen2.5-3B, upper bound ≈ 0 in Gemma and Llama). Lingering shows no consistent slope (−0.73 … +0.06, all CIs include 0).
  Reading: in these LMs, the residue that comprehension questions detect is not the source of structural priming. Priming tracks the *prediction error* of the garden path (adaptation toward the resolved parse, as in E005–E008), while comprehension tracks *commitment duration* (length). Exploratory; to be re-checked on the remaining models and with bootstrap CIs from analyze_v2.
