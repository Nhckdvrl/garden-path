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

## Results (9 models)

| model | R | ρ, answer ↛ claim | ρ, answer ↛ value | ρ, all later ↛ claim | ρ, answer ↛ correction | class |
|---|---|---|---|---|---|---|
| Llama-3.2-3B | +1.65 | 1.10 | 0.94 | 0.12 | 1.18 | H-later |
| Llama-3.1-8B-Instruct | +1.79 | 1.64 | 1.53 | 0.21 | 1.02 | H-later |
| Mistral-7B | +2.17 | 1.34 | 1.10 | −0.06 | 0.99 | H-later |
| Qwen2.5-7B | +1.35 | 0.16 | −0.04 | 1.13 | 2.01 | H-direct |
| Qwen2.5-7B-Instruct | −2.23 | (R < 0) | | | | H-later (ratio not interpretable) |
| Qwen3-8B-Base | +2.26 | 2.08 | 1.70 | −0.03 | 1.84 | H-later |
| Gemma-2-9B | +1.57 | 1.12 | 1.11 | 0.16 | 1.47 | H-later |
| Qwen2.5-32B | +0.56 | −3.02 | −3.39 | 2.90 | 8.44 | H-direct |
| Llama-3.1-70B | +1.86 | 0.48 | 0.66 | −0.20 | 1.45 | H-direct |

**Control:** blocking the answer's access to the correction raises the pull toward A in 9/9 models (M rises by 5–17 nats).

**Classification:**
- H-later in 6/9: 5 of the 8 models with R > 0, plus Qwen2.5-7B-Instruct, whose R < 0 makes the ratio uninterpretable.
- H-direct in 3/9: Qwen2.5-7B, Qwen2.5-32B and Llama-3.1-70B.

**Reading:**
- In most models the overridden value reaches the answer through positions after the statement. Blocking the answer's own access to the statement changes nothing, while blocking all later access removes the pull.
- In Qwen2.5-7B, Qwen2.5-32B and Llama-3.1-70B the answer reads the overridden statement directly, as later text reads the abandoned NP in the garden path.
- The E015 conclusion "carried by later positions" holds for the majority, and the route depends on the model.
