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
