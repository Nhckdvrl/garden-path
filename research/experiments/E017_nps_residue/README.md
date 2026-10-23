# E017: Does an NP/S garden path also leave a residue of the abandoned object analysis?

**Status:** card frozen 2026-10-24, before the new runs. Existing data for 11 models (E007_cross) had been inspected when this card was written: A_L > 0 in 9/11, CI > 0 in 6/11, ratio to the true-object prime about 0.3–0.5. This card fixes the prediction for the 11 models added now.

## Motivation

A reviewer argued that the stale-state account predicts a residue for NP/S garden paths too (*The student forgot the solution was in the back of the book*): the NP's states are computed under the object analysis before *was* arrives. E007 tested only the S-type item-level relations for NP/S and found none.

## Design

- E007 materials: 64 NP/S families with GP, CUE (*forgot that the solution*), NB/NC (S-complement-only verb *hoped*, without/with *that*), and TB (*forgot the solution which was ...*, a real object).
- NP/S primes are followed by the E002 NP/Z targets (cross-construction, `E007_cross`), so the L measure is identical to the main experiments.
- Residue: A_L = (GP − NB) − (CUE − NC); real-object effect: A_L^TB. Two-way bootstrap.
- New models: the 11 E002-panel models not yet run (see `run_queue`).

## Frozen predictions (new models)
- **N1:** A_L > 0 in the majority of the new models (sign test).
- **N2:** the residue is smaller relative to the real-object prime than for NP/Z primes (ratio below the NP/Z ratio of the same model) in the majority of models, because cross-construction priming dilutes the effect.
