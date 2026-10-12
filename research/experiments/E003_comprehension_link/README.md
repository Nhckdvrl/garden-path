# E003 — Is the priming residue the same thing as the comprehension residue?

**Status:** designed 2026-10-12. **Not run**: GPU use is held until the user approves going beyond the 4-card budget (the E001/E002 panels already use 4). Owner: this session. E001/E002 belong to the parallel session; E003 only *reads* their outputs (`results/gp/E002/<tag>.family_A.csv`).

## Gap

Humans show both lingering misinterpretation (Christianson 2001: "Did the man hunt the deer?" → Yes) and misparse priming (van Gompel 2006). van Gompel could not tell whether these are one residue or two. Slattery et al. (2013) showed that the correct structure can be built while the wrong interpretation lingers, which suggests the two can dissociate. In LMs we can measure both on the **same items in the same model** with no participant noise, and ask whether item-level priming residue predicts item-level comprehension residue.

## Measures (69 Amouyal NP/Z families; GP vs E001 comma-CUE sentences)

- `OBS` residue: `Δ_obs = logodds(Yes | GP, Q_obs) − logodds(Yes | CUE, Q_obs)`, with Q_obs = *Did the secretary type the memo?*. Q_obs is NOT_ENTAILED in both forms, so only the GP−CUE **shift** is interpreted. No absolute truth label is assumed.
- `FINAL` residue: `Δ_fin = logodds(Yes | GP, Q_final) − logodds(Yes | CUE, Q_final)`, with Q_final = *Did the memo near completion?* (entailed in both). Negative values mean failure to build the final relation. This is distinct from lingering.
- Priming residue: per-family `A = (GP−NB) − (CUE−NC)` on the comma-free target-surprisal measure S (E002, defined post hoc by its owner after two models; exploratory).
- Positive control: logodds(Yes | CUE, Q_final) > 0. Models failing it are reported but not interpreted.
- Two prompt formats (plain `Answer:` and chat template where available). Comprehension reliability = cross-format item correlation. A reliability = split-half over target families (Spearman–Brown). The correlation ceiling is sqrt(rel_A · rel_comp).

## Competing predictions

| Account | Item level (within model) | Model level |
|---|---|---|
| One shared residue (the transient object analysis drives both) | corr(A, Δ_obs) > 0, near the reliability ceiling | models with larger rA show larger Δ_obs |
| Dissociation (Slattery-like: priming residue ≠ interpretation) | corr ≈ 0 despite reliable A and Δ_obs | no relation |
| Priming tracks failure to build the final structure | corr(A, −Δ_fin) > corr(A, Δ_obs) | — |

Item-level correlations need reliable item measures. If either reliability is < .5, the item-level test is declared uninformative and only model-level results are reported. With 69 families, the detectable correlation at 80% power is about |r| ≥ .33. Model level has ~20 models, so it is only descriptive.
