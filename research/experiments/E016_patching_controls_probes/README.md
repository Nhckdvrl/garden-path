# E016: Is the residue carried by role information in the noun-phrase states? Patching controls, role probes and a role-direction intervention

**Status:** card frozen 2026-10-24, before any E016 run. Motivated by the simulated ARR review of the paper draft. The reviewers asked:
- (i) whether replacing the NP states could remove the residue merely because any replacement is off-distribution;
- (ii) whether the no-comma donor result holds beyond three models;
- (iii) whether the NP states encode the syntactic role at all, and whether that role information is what later text reads.

## Design (E002 materials and targets; same pipeline as E013)

**(a) Same-analysis donor.**
- GP's NP states are replaced, at every layer, by the states of the same NP tokens in the donor `It was a quiet morning. ` + GP. There the NP is again analysed as an object, but in a different context and at shifted positions.
- NB gets the same treatment with `It was a quiet morning. ` + NB.
- If patching itself destroyed the residue, ρ_NP would drop here as it did with the CUE donor. If the residue is carried by the role encoded in the NP states, ρ_NP stays near 1.

**(b) NB donor** (no comma, subject analysis, as in E013b) on all E016 models.

**(c) Role probe.**
- At every layer, a logistic-regression probe on the NP's last-token residual state separates object NPs (TB, TC primes) from subject NPs (CUE, NC primes).
- Two-fold cross-validation by family.
- Applied to:
  - NB (`slept the deer`: no comma, subject);
  - PASS (`was hunted the deer`, E011 material: subject of the main clause, after a passive verb).
- GP's NP states are identical to TB's (shared prefix), so GP is not probed separately.

**(d) Role-direction intervention.**
- Direction per layer: u_l = normalized difference between the mean object-NP state and the mean subject-NP state (TB/TC vs CUE/NC; fit on training-fold families).
- In the GP prime, at the NP tokens and in the layers from L/4 to 3L/4, each state's projection on u_l is set to the subject mean projection. Later prime tokens are recomputed. The target reads the full intervened cache.
- NB primes receive the same operation, and Eq. 2 subtracts it.
- Control: random unit directions with the same projection shift (norm-matched, 3 seeds).

**Models:** Llama-3.2-3B, Llama-3.1-8B-Instruct, Mistral-7B, Qwen2.5-7B, Qwen3-8B-Base, Qwen2.5-32B (bf16), Llama-3.1-70B (bf16, 2 GPUs).

## Frozen predictions
- **P1 (patching is not destructive):** with the same-analysis donor, ρ_NP ≥ 0.8 in the majority of models, and ρ_NP(same) > ρ_NP(CUE donor) in every model.
- **P2 (no-comma donor):** ρ_NP(NB donor) ≤ 0.6 in the majority of models.
- **P3 (role is decodable at the NP):**
  - cross-validated probe accuracy ≥ 0.9 in some layer of every model;
  - NB NP states are classified as subject (mean P(object) < 0.5) in the majority of models.
- **P4 (role direction carries the residue):** removing the object-role component lowers A_L to ρ ≤ 0.7 in the majority of models, and more than the random-direction control in every model.
- **P5 (exploratory, no prediction):**
  - P(object) of PASS NP states per model;
  - its relation across models to the E011 passive/GP residue ratio.

## Results (7 models)

| model | ρ_NP, same-analysis donor | ρ_NP, NB donor | ρ_NP, CUE donor (E013) | ρ, role direction | ρ, random directions | probe acc | P(object) NB / PASS (mid layers) |
|---|---|---|---|---|---|---|---|
| Llama-3.2-3B | 0.94 | 0.45 | 0.39 | 0.63 | 0.76 | 1.00 | 0.33 / 0.54 |
| Llama-3.1-8B-Instruct | 0.95 | 0.36 | 0.28 | 0.68 | 0.81 | 1.00 | 0.39 / 0.67 |
| Mistral-7B | 0.93 | 0.46 | 0.40 | 0.71 | 0.77 | 1.00 | 0.36 / 0.62 |
| Qwen2.5-7B | 0.85 | 0.34 | 0.14 | 0.74 | 0.76 | 1.00 | 0.23 / 0.41 |
| Qwen3-8B-Base | 1.11 | 0.47 | 0.71 | 0.40 | 0.79 | 1.00 | 0.55 / 0.59 |
| Qwen2.5-32B (bf16) | 0.70 | 0.08 | 0.01 | 0.31 | 0.80 | 1.00 | 0.29 / 0.61 |
| Llama-3.1-70B (bf16) | 0.82 | 0.04 | 0.01 | 0.70 | 0.93 | 1.00 | 0.31 / 0.66 |

**Frozen predictions:**
- P1: ρ_SAME ≥ .8 in 6/7, and above the CUE-donor value in 7/7. **Confirmed.**
- P2: ρ_NBD ≤ .6 in 7/7. **Confirmed.**
- P3: probe accuracy ≥ .9 in 7/7, and NB classified as subject in 6/7. **Confirmed.**
- P4: ρ_ROLE ≤ .7 in 4/7, and below random in 7/7. **Confirmed.**
- P5 (exploratory): PASS P(object) is unrelated to the E011 ratio across models (ρ = 0.14, n = 7).

**Reading:**
1. Patching is not destructive in itself. Replacing the NP states with object-analysis states from another context leaves 70–111% of the residue (82% at 70B), so the residue disappears in E013 because the object analysis is replaced, not because the states are replaced.
2. The NP states encode the role.
   - A linear probe separates object from subject NPs perfectly.
   - It classifies comma-less NB noun phrases as subjects, so it does not just read the comma.
   - Passive noun phrases fall in between (0.41–0.67).
3. Moving only the NP's object-role component to the subject mean, in the middle half of the layers, removes 26–69% of the residue. Random directions with the same displacement remove 7–24%.
   - Role information carries a substantial part of the residue.
   - The rest is carried by other components of the NP states, since the full replacement removes more.
4. Caveat: the probe already separates the classes at the first layer, so the probe alone cannot show *where* the role is computed. The depth result of E013b remains the evidence for that.
