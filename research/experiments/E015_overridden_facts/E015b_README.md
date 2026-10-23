# E015b: Where is the overridden value read from? Attention knockout

**Status:** card frozen 2026-10-24, before any E015b run. Motivated by the round-2 interpretability review: the E015 re-encoding counterfactual (a `Mistake:` label before the statement) may be too weak to change the statement's states. A direct copy of the value token at the answer position would also explain why re-encoding failed (F3 0/9).

## Design

E015 items and models. Scoring uses full sequences (context + probe + answer) with a 4D attention mask: causal, plus the blocked query→key pairs listed below, applied at every layer and head.

Spans:
- **claim:** the tokens of the overridden statement S(E,A), or of S(E′,A) in CTRL;
- **value:** the token(s) of A inside it;
- **correction:** the tokens of S(E,B);
- **answer:** the probe and answer tokens.

Cells:
- `none`;
- `KO_ANS_CLAIM`: answer tokens cannot attend to the claim;
- `KO_ANS_VALUE`: answer tokens cannot attend to the value token(s) only;
- `KO_ALL_CLAIM`: every token after the claim cannot attend to it;
- `KO_ANS_CORR`: answer tokens cannot attend to the correction. This is a directional control: it should increase the pull toward A.

Measure: R_cell = M(CORR, cell) − M(CTRL, cell), and ρ_cell = R_cell / R_none.

## Frozen predictions (competing)

- **H-direct** (the answer reads the overridden statement directly, as later text reads the abandoned NP): ρ(KO_ANS_CLAIM) ≤ 0.5. If the route is a value copy, ρ(KO_ANS_VALUE) ≤ 0.5 as well.
- **H-later** (the pull is carried by positions after the statement): ρ(KO_ANS_CLAIM) ≥ 0.8 and ρ(KO_ALL_CLAIM) ≤ 0.5.

Each model is classified as H-direct, H-later or neither. The paper's §7 interpretation follows the majority.

**Control:** M(CORR, KO_ANS_CORR) > M(CORR, none) in the majority of models.
