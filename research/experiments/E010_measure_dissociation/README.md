# E010 — Measure dissociation: production-like residue vs comprehension-like adaptation

**Status:** prospective prediction, frozen 2026-10-13 before any test on new items. Discovered post-hoc in E009 (L measure) and checked on E002/E005 data that already existed.

## Pattern to confirm

The same NP/Z garden-path prime:
1. **raises production-like object attachment** (L = log P("V the N,") − log P("V, the N"); comma-matched within A's pairs). Net A_L > 0, scaling with commitment, with no error-driven slope. This mirrors van Gompel et al. 2006 (human production priming of the abandoned transitive analysis).
2. **lowers the surprise of a later garden-path resolution** (S = surprisal of the target's disambiguating word), with a negative slope on disambiguation error. Net sign is model-dependent. This mirrors human syntactic adaptation in comprehension (Fine et al. 2013).

Evidence so far (counts of models): net A_L > 0 in 18/18 (E002), 17/17 (E005), 17/17 (E009). Error slope on S < 0 in 17/18, 15/17, 15/17. Error slope on L < 0 in only 3/18, 10/17, 5/17.

## Frozen predictions for new, independent items

Test set: Christianson et al. 2001 NP/Z appendix items as implemented in the peer session's E003 (54 families; analysis owned by that session; we request read-only numbers).
- **D1:** net A_L > 0 in the majority of models (sign test across models, one-sided α = .05).
- **D2:** the prefix-matched within-family error slope is negative on S (sign test) and **not** negative on L (fewer than half of models negative).
- **D3:** within each model, error slope(S) < error slope(L) in the majority of models (sign test).

Failure of D1 or D3 means the dissociation is set-specific and is reported as such.

## Result (Christianson OT items, n = 42 families, 16/21 models; numbers from peer session E003 `report_for_E010.csv`, scored here against the frozen card)

Provenance: the E003 per-model raw files were readable on the shared disk from about 14:15, before this card was frozen (15:55). No L/S numbers were computed or seen by this session before the peer's report. Recorded as requested.

- **D1 confirmed:** net A_L > 0 in **16/16** models, every family-bootstrap CI above 0 (0.14 to 1.84).
- **D2 split:** prefix-matched error slope on S negative in **13/16** (sign p = .011), confirmed. Error slope on L "not negative in most" **failed**: 10/16 negative, but only 2 significant (Llama-3.1-8B-Instruct t = −3.15; Mistral-7B t = −2.08).
- **D3 confirmed:** slope(S) < slope(L) in **14/16** models (sign p = .002), despite A_L's larger scale.

**Verdict:** the measure dissociation is **quantitative, not absolute**. Error-driven adaptation is much stronger on the comprehension-like measure (S), with a weak same-sign tendency on the production-like measure (L). The production-like net residue (the van Gompel pattern) is positive in every model on all three independent item sets (E002, E005, Christianson). The five remaining models will be appended when the peer reports them; the verdict above is not revised unless they change a count's significance.
