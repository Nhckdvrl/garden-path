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
