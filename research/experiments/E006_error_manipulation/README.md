# E006 — Is the error-driven component causal? Within-family manipulation of disambiguation surprisal

**Status:** exploratory-causal test. Card written 2026-10-12 before any E006 scoring. Known at the time: E002 discovery (11 models) and E005 held-out (first 4 models: 10/10 frozen predictions confirmed), showing that A rises with object commitment at the verb and falls with the prime's disambiguation surprisal (gp_strength).

## Why

The gp_strength effect is so far **between-family** (correlational). Families differ in many ways. If the error-driven account is right, then holding the prefix (and therefore commitment) fixed and changing only *how surprising the disambiguation is* should change A within a family.

## Materials

- Prefix fixed: `While the man hunted the deer` (93 discovery families).
- Continuations (variants): the published original (k = 0) plus model-generated alternatives in which the NP is the subject.
  - Generator: Qwen2.5-14B-Instruct.
  - Rule filter: past-tense or past-modal first word; no repeated first word within a family.
  - Independent naturalness rating of the CUE sentence by Llama-3.1-8B-Instruct (expected score on 1–5).
  - Inclusion: originals always; generated variants with rating ≥ 3.0; families with ≥ 3 variants.
  - Files: `e006_continuation_candidates_v1.jsonl` (raw), `e006_variants_v1.jsonl` (rated).
- Per variant k: GP_k, CUE_k, NB_k, NC_k. NB/NC use the same E002 intransitive verb, so the variant content enters all four cells and cancels in A_k = (GP_k − NB_k) − (CUE_k − NC_k).
- Targets: fixed subset of 45 E001 target families (hash-selected, outcome-blind).

## Measures and predictions

- err_k = disambiguation surprisal effect of variant k in the prime: lp(CUE_k at first continuation word) − lp(GP_k at first continuation word). Secondary: the same over the whole continuation.
- Model: `A_k ~ err_k + family fixed effects` (within-family slope), family-clustered SEs.
- **Error-driven account:** within-family slope < 0 in models whose discovery b_gp < 0.
- **Commitment-only account:** slope ≈ 0, since commitment is fixed by the identical prefix.
- Models: Llama-3.2-3B, Qwen2.5-0.5B, Pythia-1.4b, Pythia-2.8b, Mistral-7B (discovery b_gp < 0), plus GPT-2 and Pythia-410m (discovery b_gp ≈ 0, but held-out b_gp < 0, so they are informative either way).

## Caveats known in advance

- Variants differ in content as well as surprisal. The DiD cancels content main effects but not a content × GP interaction.
- Generated text is model-made. Naturalness ratings come from a different model than the generator, and all tested models differ from both. Results will also be reported for originals vs generated separately.
