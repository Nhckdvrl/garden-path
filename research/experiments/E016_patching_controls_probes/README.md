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
