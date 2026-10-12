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

## Run notes (2026-10-13)

- vLLM 0.11.0 bug: the sampled-token pinned buffer is sized by `max_model_len`, so the engine crashes whenever `max_num_seqs` > `max_model_len`. Fixed by max_model_len 1024 and max_num_seqs 512; workers spawn; one process per model. The first launches of all 8 models failed on this before any generation; no data was lost.
- Coding moved offline (`reclassify.py`, batched). **v1** = the frozen coding (primary). **v2** = a post-hoc refinement that resolves coordination after the NP ('the dishes and left' → TRANS; 'the baby and the dog cried' → INTR). It is applied uniformly to all models as a sensitivity analysis. AMBIG on Llama-3.2-3B: v1 9.1%, v2 2.0%.
- **Coding audit on real generations** (Llama-3.2-3B, 30 random per v2 class; audited by the research assistant, Claude, not a human):
  - TRANS correct 27–29/30. One clear error: a comma-less garden-path sentence ("…taught algebra and geometry in the forties … both were essential") coded TRANS. Two arguable cases: *began jamming*, a gerund complement.
  - INTR correct 29/30. One error: a participial modifier read as the main verb ("dressed the bathroom mirror downloaded from…").
  - AMBIG (2%) is mostly resolvable: "V and V" is usually intransitive; NP + VBG/relative clause is usually transitive. Excluded as frozen.
  There is no reason for these errors to differ by prime condition, but this is not tested.

## Results (8 models; v1 frozen coding; v2 gives the same verdicts)

| model | p(TRANS) GP / CUE / NB / NC / TB / NONE | vG | A_gen | r_gen | gp_style GP vs CUE |
|---|---|---|---|---|---|
| gemma2-2b | .54 / .47 / .53 / .49 / .59 / .54 | +.074* | +.036* | .30 | .055 vs .002 |
| llama3.1-8b-instruct | .56 / .63 / .51 / .67 / .73 / .68 | −.075* | +.089* | .23 | .245 vs .017 |
| llama3.2-3b | .58 / .71 / .56 / .72 / .71 / .73 | −.139* | +.033* | .13 | .210 vs .024 |
| mistral-7b | .50 / .37 / .51 / .42 / .59 / .48 | +.120* | +.039* | n/a (TB−NB small) | .098 vs .008 |
| pythia-1.4b | .68 / .50 / .67 / .53 / .65 / .57 | +.177* | +.040* | n/a (TB−NB < 0) | .028 vs .009 |
| qwen2.5-7b-instruct | .62 / .60 / .58 / .67 / .76 / .79 | +.008 | +.097* | .20 | .214 vs .004 |
| qwen2.5-7b | .59 / .68 / .54 / .72 / .71 / .76 | −.098* | +.082* | .30 | .239 vs .012 |
| qwen3-8b-base | .59 / .73 / .55 / .74 / .74 / .79 | −.145* | +.046* | .22 | .244 vs .009 |

(* = two-way bootstrap CI excludes 0.)

**Frozen predictions:** P1 (A_gen > 0) **8/8 confirmed**. P2 (vG > 0) **3/8, not confirmed**. P3 (style GP > CUE) **8/8 confirmed**. P4 (A_gen vs E002 A_L across models) **ρ = 0.81, p = .015, confirmed**; vs A_S ρ = 0.60, p = .12.

**Reading:**
1. The abandoned-object residue **reaches free production in every model**, after punctuation style and verb bias are controlled (A_gen +0.03 to +0.10, about 13–30% of a full transitive prime where that ratio is defined). Its size across models tracks the log-prob production measure L (ρ = .81).
2. The raw van Gompel contrast (GP vs comma), the human paradigm's statistic, is **not** a valid LM statistic. It is dominated by punctuation-style alignment, which differs by model family: Llama and Qwen produce comma-less garden-path sentences after comma-less primes (21–25% vs 0.4–2.4%), so vG < 0. Gemma-2, Mistral and Pythia do so much less, so vG > 0. Humans completed orally, without punctuation.
3. **Models write garden-path sentences after reading one.** Up to a quarter of completions after a GP prime are themselves comma-less NP/Z garden paths. This is production-level alignment to the prime's *resolved* structure plus its punctuation style.
