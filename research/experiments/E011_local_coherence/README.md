# E011 — Is the production-like residue configuration-level (local coherence) or analysis-based? Passive test

**Status:** discriminating test, frozen 2026-10-13 before any E011 scoring. Motivation: E004 on L (post-hoc) suggested that a non-garden-pathed GP copy still adds object-attachment residue.

## Manipulation (93 NP/Z families; same verb as GP)

| Cell | Example | locally coherent `V the N`? | object analysis ever licensed? |
|---|---|---|---|
| GP | While the man hunted the deer ran into the woods. | yes | yes (transient) |
| PASS_B | While the man was hunted the deer ran into the woods. | yes (`hunted the deer`) | **no** (passive participle, monotransitive) |
| PASS_C | While the man was hunted, the deer ran into the woods. | no | no |
| NB / NC | (E002 intransitive-verb controls) | | |

- A_GP = (GP − NB) − (CUE − NC) (from E002 data, identical items)
- **A_pass = (PASS_B − PASS_C) − (NB − NC)**: comma pattern matched within each pair; *was* cancels within the passive pair.

## Frozen predictions (L = production-like comma-placement measure; S also reported)

| Account | A_pass on L | ratio A_pass / A_GP on L |
|---|---|---|
| Configuration / local coherence | > 0, comparable to A_GP | ≈ 1 (≥ 0.5) |
| Analysis (needs a licensed object reading) | ≈ 0 | ≈ 0 (< 0.25) |

Decision per model from the bootstrap CI of A_pass on L. Pooled: median ratio across models. **P-CONF:** median ratio ≥ 0.5 and A_pass > 0 (CI) in the majority of models. **P-ANAL:** median ratio < 0.25 and A_pass CI includes 0 in the majority. Anything else is intermediate.

Manipulation check: the disambiguator surprisal effect for PASS_B vs PASS_C should be small relative to GP vs CUE (no garden path).
Plausibility: passive sentences are rated by Llama-3.1-8B-Instruct (same protocol as E006). Results are reported for all families and for the plausible half (rating ≥ median).

**Exclusion rule (fixed before scoring):** families whose ambiguous verb has a past form different from its participle (rode, drew, drank, ate, wrote, woke, grew, shrank, broke, hid, began) are excluded, because the passive would be ungrammatical or would change the GP substring.

## Results (2026-10-13; 17 models; frozen rule applied as written)

**Verdict: P-ANAL = YES, P-CONF = no** (all families: median ratio A_pass / A_GP on L = 0.10; A_pass CI > 0 in 5/17. Plausible half: median −0.08; 2/17).
- Manipulation check passes: the passive barely garden-paths (disambiguator effect PASS_B vs PASS_C 0.5–2.8 nats vs GP vs CUE 3.4–8.1).
- A_pass on L is significantly **negative** in 7/17 (GPT-2, Pythia ×4, Qwen2.5-3B, Qwen3-8B-Base).
- **Heterogeneity (exploratory, not part of the rule):** the 5 models with A_pass > 0 are the larger or instruction-tuned ones (Gemma-3-12B-it 0.27, Llama-3.1-8B-Instruct 0.28, Mistral-7B 0.22, Qwen2.5-7B 0.53, Qwen2.5-7B-Instruct 0.55; ratios). A configuration-level component may exist in stronger models. Unconfirmed.
- On S, A_pass is positive in most models, but A_GP on S is near zero, so the S ratio is uninterpretable. S is the adaptation measure and shares the comma-omission component; not used for the verdict.

**Reading:** the production-like residue (net A_L > 0 in every model in E002/E005/E009/E010) needs a *licensed* object analysis of the NP. The local adjacency `V the N` without a possible object reading does not reproduce it. This refutes the post-hoc configuration hypothesis from E004 (L). The van Gompel-type abandoned-analysis account stands for most models.
