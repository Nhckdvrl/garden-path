# E004 — Does the residue depend on the sentence being *processed as a garden path*? (exact-repetition test)

**Status:** exploratory. Card written 2026-10-12 before any E004 output. Known at the time: E002 results for GPT-2, Pythia-160m and Pythia-410m (A > 0; rA ≈ 0.47 in GPT-2; the E002 order test failed its manipulation check because a comma-dropped copy is a *deviant* copy that is still garden-pathed).

## Question

E002's A = (GP − NB) − (CUE − NC) isolates the object-licensing-verb × adjacency effect. Is that effect produced by **processing** the NP as a temporary object (history-dependent), or by the **configuration** `V_trans the N` regardless of how it was processed?

## Manipulation

Exact repetition: `X>X` = the same sentence twice, for X ∈ {GP, CUE, TB, NB, NC}. In the second copy the continuation is predictable by copying, so (manipulation check) the GP copy should no longer be garden-pathed: disambiguator surprisal(GP copy 2) − surprisal(CUE copy 2) ≈ 0.

Statistic (S = −lpD, comma-free target measure; L also reported):
- `A2 = (GP>GP − NB>NB) − (CUE>CUE − NC>NC)`, `A2full = (TB>TB − NB>NB) − (CUE>CUE − NC>NC)`, `rA2 = A2/A2full`.
- Increment from the second copy: `ΔA = A2 − A1` vs `ΔAfull = A2full − A1full` (A1 from the E002 singles).

| Account | Prediction |
|---|---|
| History / processing (the garden-path *episode* creates the residue) | second GP copy adds little: ΔA ≪ rA1·ΔAfull, i.e. rA2 < rA1 |
| Configuration / string (a `V_trans the N` sequence is encoded as V–object whatever its predictability) | ΔA ≈ rA1·ΔAfull, rA2 ≈ rA1 |
| Manipulation failure | the GP copy-2 garden-path effect stays well above 0. Then no inference. |

Unit = prime family (93), two-way bootstrap. Same targets as E002.

> **Superseded in part (2026-10-13):** the configuration-level hypothesis below was tested in E011 (frozen passive test) and **rejected** (median A_pass/A_GP = 0.10 on L). The production-like residue needs a licensed object analysis.

## Post-hoc reading of the L measure (recorded 2026-10-13; L was reported, not the primary measure)

- **S (primary, 10 models):** the exact second GP copy (manipulation check passes: garden-path effect ≈ 0) never adds transitive residue (dA −0.23 to +0.07), while TB copies add where repetition adds at all. The adaptation/residue on S depends on the garden-path episode.
- **L (comma-placement, production-like; 17 models):** single-copy GP residue is large (rA1 ≈ 0.4–1.5). Where repetition adds anything on L, the non-garden-pathed GP copy adds about as much as a TB copy, or more: Gemma-2-2B 0.19 vs 0.21; Qwen2.5-3B 0.63 vs 0.70; Qwen3-1.7B 0.14 vs 0.27; Pythia-1.4B 0.11 vs 0.04; Qwen2.5-0.5B 0.14 vs 0.04. Many models saturate (dAfull ≈ 0) and are uninformative.
- **Hypothesis (not established):** the production-like residue is **configuration-level** priming. The locally coherent substring `V the N` primes object attachment regardless of its global parse or processing history (cf. local-coherence effects, Tabor, Galantucci & Richardson 2004). It is not a lingering misanalysis *episode*. The comprehension-like adaptation is episode-dependent. Test planned: E011.
