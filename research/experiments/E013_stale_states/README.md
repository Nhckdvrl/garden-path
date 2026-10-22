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
