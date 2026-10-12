# E002 — Is LM "misparse priming" carried by the string or by the processing history?

**Status:** exploratory. Card written 2026-10-12 before any E002 output existed. At that point interim E001 results for 4 small models were known: **GP ≈ TB** (a GP prime moves the comma-placement target as much as a genuinely transitive prime with identical punctuation), and the comma-placement target is dominated by comma-position copying.

## What we do not know after E001

GP ≈ TB has at least three explanations:
1. **Surface string:** the bare `V the N` sequence (no comma) primes object attachment whether or not any object analysis was ever entertained.
2. **Transient analysis (processing history):** the representation built while `the N` was read as V's object, which is never recomputed in a causal LM, drives later behaviour.
3. **Final-structure insensitivity:** the target measure does not register final structure at all, so GP ≈ TB is uninformative. Instrument failure.

## Manipulations (93 E001 families; all primes lexically disjoint from targets)

- **No-comma triad:** `NB` *While the man slept the deer ran…* (strictly intransitive verb; same adjacency, no object analysis), `GP`, `TB`. Comma-free comparisons only.
  - surface: GP ≈ NB; analysis: GP > NB and GP ≈ TB; instrument failure: TB ≈ NB.
  - Caveat: NB changes the verb, so GP − NB also contains a lexical verb-bias component. GP − TB does not.
- **Processing-history order test:** two-sentence primes with identical content. `GP>CUE` vs `CUE>GP` and `TB>CUE` vs `CUE>TB` (plus `TC`, `CUE>CUE`).
  - Key statistic: `H = [L(CUE>GP) − L(CUE>TB)] − [L(GP>CUE) − L(TB>CUE)]`. GP and TB have identical punctuation, so comma recency cancels.
  - Surface account: H ≈ 0 (GP behaves like TB in both positions).
  - Analysis account: H < 0. A GP copy read *after* its disambiguated twin is not garden-pathed, so it loses its transitive-like priming. TB stays transitive regardless.
  - Manipulation check: the disambiguating word's surprisal in a GP copy after CUE (`GPafterCUE_dis`) should be much lower than for GP alone.

## Two target measures

1. `L`: comma placement (from E001); vulnerable to comma copying, so only comma-matched contrasts are interpreted.
2. **Target garden-path surprisal (comma-free):** `−lpD` = surprisal of the disambiguating word in a GP target (*While the nurse washed the baby **cried***). More transitive expectation → higher surprisal. Normalised version: `GPeff = lpDc − lpD` (target GP effect vs its comma version).

Primary: `GP − TB`, `GP − NB`, `TB − NB`, and `H` on both measures. Unit = prime family (93), two-way bootstrap over prime and target families.
