# E012 — Free production: does the abandoned-object residue appear in what models actually write?

**Status:** card frozen 2026-10-13 before any E012 generation. Motivation: every priming result so far (E001–E011) scores fixed strings. The human paradigm (van Gompel et al. 2006) measures *free completions*. A reviewer will rightly ask whether the production-like residue (A on L > 0 in 17/17 models) shows up in generation. This is also the most direct human comparison available: humans produced 33.6% vs 29.1% transitive completions after GP vs comma primes (Exp. 1) and 68.6% vs 61.6% (Exp. 3).

## Design

- Primes: the 93 NP/Z families × {NONE, GP, CUE, TB, TC, NB, NC} (E001/E002 materials).
- Target: a van Gompel-style fragment from every content-disjoint other family, e.g. `… While the nurse washed`. The model continues freely: pure sampling (temperature 1, top-p 1, so samples follow the model's distribution), 2 samples per prime × target × condition, max 24 tokens, no chat template.
- Coding: `research/tools/transitivity.py`, rule-based on POS tags (spaCy's dependency parser is itself garden-pathed, its POS tags are not). It outputs TRANS / INTR / AMBIG plus two extra readouts:
  - `comma`: the continuation starts with a comma;
  - `gp_style`: the model writes an intransitive clause without a comma, i.e. it produces a garden-path sentence itself.
  Gold validation on 1,066 material sentences with known structure: 1,063 correct (99.7%), `test_transitivity_gold.py`. The error rate on real generations is estimated after the run: an LLM-judge cross-check on a random sample of 300 and a manual read of 60. Those numbers are reported whatever they are. AMBIG (relative clause or coordination after the NP) is excluded and its rate reported per condition.

## Statistics (unit = prime family; two-way bootstrap over prime × target families)

p(c) = proportion TRANS among non-AMBIG continuations in condition c.
- `vG = p(GP) − p(CUE)`: the van Gompel contrast (human: +4.5 and +7.0 points).
- `A_gen = (p(GP) − p(NB)) − (p(CUE) − p(NC))`: comma pattern and verb bias matched, as A on L.
- `r_gen = (p(GP) − p(NB)) / (p(TB) − p(NB))`.
- Style: gp_style rate in GP vs CUE, and NB vs NC.

## Frozen predictions (from the current understanding: production-like residue positive in every model)

- **P1:** A_gen > 0 (CI excludes 0) in the majority of models.
- **P2:** vG > 0 in the majority of models.
- **P3:** gp_style rate higher after GP than after CUE in the majority of models (production-level stylistic adaptation).
- **P4:** across models, A_gen correlates positively with A on L from E002 (Spearman, same model set).

Failure of P1/P2 would mean the log-prob residue does not reach actual production, which would be a major correction to the current understanding.
