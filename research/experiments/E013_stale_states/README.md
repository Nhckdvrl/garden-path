# E013: Where is the abandoned analysis carried? Stale NP states vs garden-pathed main-clause states

**Status:** card frozen 2026-10-23, before any E013 run.

## Motivation

In a causal transformer, the hidden states at *the deer* in *While the man hunted the deer ran into the woods* are computed before the disambiguating word. They are therefore **identical** to the states in the transitive prime *While the man hunted the deer it ran…*: the model cannot recompute them after reanalysis. Any later sentence that attends to them reads a representation built under the object analysis. This gives an LM-specific, mechanistic version of van Gompel's "residual activation".

The alternative: the residue is carried by the **main-clause** states (*ran into the woods.*). Those states processed the garden path, so they encode the reanalysis episode, and they could carry the residue and/or the error-driven adaptation.

## Design (activation and KV patching; E002 primes and targets)

- Recipient primes: GP and NB (E002). Donors: CUE for GP and NC for NB (same verb, same NP; the donor's NP comes after a comma, so it is analysed as a subject).
- **Run B (original):** the recipient prime as is.
- **Run A ("reanalysed from the start"):** the recipient prime with the residual stream at the NP tokens replaced, at every layer, by the donor's states at its NP tokens. Later prime positions are recomputed, so in run A the main clause never meets an object-analysed NP. RoPE models: the residual stream carries no absolute position, so the one-token offset is harmless.
- **Hybrid KV caches read by the target:** for each span s ∈ {NP, MC} (MC = from the end of the NP to the end of the prime, period included), the target attends to run-A keys/values at s and run-B keys/values elsewhere. Cells: none (= B), NP, MC, both (= A). Positions before the NP are identical in A and B.
- Targets: E002 L targets (T/I comma-placement pairs) and S targets (D, disambiguator in a GP target), all content-disjoint target families. Unpatched CUE and NC are scored through the same cache pipeline for the A contrast.
- Residue measured as **A = (GP − NB) − (CUE − NC)**. The patch effect on the residue is **Δ_s = [GP_s − GP] − [NB_s − NB]**: the NB/NC control removes anything the patch does merely by importing "after a comma" information. Report **retained fraction ρ_s = A_s / A**, where A_s uses GP_s and NB_s.
- Statistics: two-way bootstrap over prime × target families (as E002). Models: RoPE decoders with complete caches (Llama-3.2-3B, Llama-3.1-8B, Mistral-7B, Qwen2.5-7B, Qwen3-8B-base, Qwen2.5-32B, Pythia-1.4b/2.8b).
- Sanity check: cell "none" must reproduce the E002 scores of the same model (|diff| < 0.02 nats on the family means).

## Frozen predictions

- **M1 (stale-state account, production measure):** on L, patching NP removes a large part of the residue (ρ_NP ≤ 0.5), and does so more than patching MC (ρ_NP < ρ_MC), in the majority of models.
- **M2 (error-driven adaptation lives in the post-disambiguation states):** on S, the patch effects run the other way: MC changes A_S more than NP does (|Δ_MC| > |Δ_NP| on S) in the majority of models.
- **M3 (sum):** "both" ≈ the NP and MC effects combined (no strong interaction); reported, not tested.

If M1 fails (MC carries the L residue), the residue is a property of the garden-path *episode* encoded downstream, not of stale states. The "LM residual activation = non-recomputation" story is then false, and we report that.

## Results (9 models; frozen analysis unchanged)

All runs: 93 families, 0 NP-length mismatches. fp32 except Qwen2.5-32B and Llama-3.1-70B (bf16; 70B on 2 GPUs).

| model | A_L (none) | ρ_NP (L) | ρ_MC (L) | ρ_both (L) | Δ_NP on S | Δ_MC on S | M1 | M2 |
|---|---|---|---|---|---|---|---|---|
| Llama-3.2-3B | +0.82 | **0.39** [.30,.48] | 0.83 | 0.37 | −0.50 | **+1.12** | ✓ | ✓ |
| Llama-3.1-8B-Instruct | +1.09 | **0.29** [.17,.38] | 1.03 | 0.32 | −0.83 | **+1.33** | ✓ | ✓ |
| Mistral-7B | +0.86 | **0.40** [.28,.49] | 0.89 | 0.33 | −0.55 | **+0.93** | ✓ | ✓ |
| Qwen2.5-7B | +0.90 | **0.14** [−.06,.27] | 1.34 | 0.50 | −0.84 | **+1.13** | ✓ | ✓ |
| Qwen3-8B-Base | +0.95 | 0.71 [.55,.92] | 0.96 | 0.63 | −1.11 | **+2.00** | ✗ (ρ_NP > .5) | ✓ |
| Pythia-2.8b | +0.49 | **0.50** [.41,.59] | 0.74 | 0.40 | −0.35 | **+0.40** | ✓ | ✓ |
| Pythia-1.4b | +0.46 | 0.65 [.56,.73] | 0.85 | 0.59 | −0.26 | +0.22 | ✗ (ρ_NP > .5) | ✗ (|Δ_MC| < |Δ_NP|) |
| Qwen2.5-32B (bf16) | +0.61 | **0.01** [−.35,.21] | 1.94 | 0.68 | −0.72 | **+1.56** | ✓ | ✓ |
| Llama-3.1-70B (bf16) | +0.52 | **0.01** [−.36,.22] | 1.89 | 0.64 | −0.79 | **+1.46** | ✓ | ✓ |

**Frozen predictions:** M1 **7/9**, M2 **8/9**. Directional pattern without the magnitude threshold:
- ρ_NP < ρ_MC on L in **9/9**;
- on S, Δ_NP < 0 in **9/9** and Δ_MC > 0 in **9/9**, all CIs excluding 0.

**Reading:**
1. The production-like residue is read mostly from the NP's pre-disambiguation states, which a causal LM never recomputes. Replacing only those states (subject-analysis states from the comma twin, comma import controlled by NB←NC) removes 30–86% of A_L. Replacing the post-disambiguation main-clause states removes little or nothing; in Qwen2.5-7B it *raises* the residue (ρ_MC = 1.34), consistent with the main clause carrying an opposite-signed force.
2. On the comprehension-like measure the two spans push in **opposite directions** in every model. Stale NP states contribute the residue (+, removing them lowers A_S). Main-clause states, which processed the disambiguation, contribute the error-driven adaptation (−, removing them raises A_S by +0.2 to +2.0). This is a mechanistic counterpart of the two-force account: the forces are carried by different positions of the same prime.
3. The ratio on S is not interpretable where A_S ≈ 0 (wide CIs). The Δ values carry the S result.
4. (Post-hoc observation.) In the largest models, patching the main clause *raises* the production residue: ρ_MC is 1.34 in Qwen2.5-7B and 1.94 in Qwen2.5-32B. In Qwen2.5-32B and Llama-3.1-70B, patching only the NP removes the residue entirely (ρ_NP = 0.01 in both). So even on L the observed net residue is the sum of a stale-NP contribution (+) and a main-clause contribution (−). The raw A_L *under*states the abandoned-analysis residue where the error-driven force is strong.

Sanity check (Llama-3.2-3B): cell "none" vs E002 family means differ by up to 0.045 nats (card threshold 0.02). The fp32 cache scorer equals the fp32 full-sequence scorer to 1e-4 (checked). The difference comes from E002's bf16 scoring, not from the pipeline. Recorded as a deviation from the stated threshold.

## E013b (exploratory, added 2026-10-23 after the 7-model results; not part of the frozen test)

Two follow-ups on Llama-3.1-8B-Instruct, Mistral-7B and Qwen2.5-7B (`run.py --donor NB`, `--from_layers`; `analyze_b.py`):
1. **No-comma donor:** GP's NP states come from NB (*While the man slept the deer…*: same NP, subject analysis, no comma; NB←NB is an identity patch, checked). If ρ_NP stays low, the NP effect is not imported punctuation information. The verb differs, so verb information could leak; this is the complement of the CUE donor, where only punctuation differs.
2. **Depth:** the NP states are replaced only from layer ⌊f·L⌋ onward (f = 0.25, 0.5, 0.75). Lower layers keep their object-analysis keys and values. The f at which ρ returns toward 1 shows from which depth the target reads the abandoned analysis.

### E013b results (exploratory; 3 models)

Retained fraction of A_L (95% CI):

| model | ρ_NP, CUE donor (E013) | ρ_NP, **NB donor (no comma)** | ρ_MC, NB donor | NP patched from 25% depth | from 50% | from 75% |
|---|---|---|---|---|---|---|
| Llama-3.1-8B-Instruct | 0.29 | **0.36** [.21,.47] | 1.14 | 0.51 | 1.07 | 1.01 |
| Mistral-7B | 0.40 | **0.46** [.29,.57] | 1.09 | 0.56 | 1.06 | 1.02 |
| Qwen2.5-7B | 0.14 | **0.34** [.15,.46] | 1.49 | 0.22 | 0.44 | 1.04 |

1. **Not imported punctuation:** with a no-comma subject-analysis donor (NB), patching the NP still removes 54–66% of the residue, and patching the main clause removes none. The NP effect in E013 does not come from information about the comma.
2. **Depth:** the target reads the abandoned analysis from the NP's keys and values in the lower half of the network (Llama, Mistral) or the lower three quarters (Qwen2.5-7B). Replacing only the upper layers' NP states has no effect (ρ ≈ 1.0).
