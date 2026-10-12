# E009 — A punctuation-free test of the lingering-object residue (case disambiguation)

**Status:** discriminating test. Card written 2026-10-12 before any E009 scoring, after the post-hoc finding that the NP/Z "commitment" slope is entangled with **comma-omission salience**: in unambiguous NB/NC pairs, omitting a comma that the verb made likely lowers target S in 17/17 models, and the obj_expect slope splits into a weak "the" part (+, 17/17) and a stronger comma part (−, 17/17).

## Design (93 E001/E002 NP/Z families)

| Cell | Example | Object analysis possible? | Comma after V |
|---|---|---|---|
| GP | While the man hunted the deer ran into the woods. | yes (transient) | omitted |
| NOM | While the man hunted they ran into the woods. | **no** (nominative) | omitted |
| NB | While the man slept the deer ran into the woods. | no | omitted |
| NBNOM | While the man slept they ran into the woods. | no | omitted |

`they` is nominative-only (object form *them*), so it rules out the object reading without punctuation. *it* is avoided because its case is ambiguous.

**A_case = (GP − NOM) − (NB − NBNOM)** on S. Within each pair the verb and the omitted comma are identical, so comma salience and verb bias cancel. Across pairs, the full-NP vs pronoun lexical difference cancels. What remains is the effect of the NP being *analysable as an object* (transiently). That combines the residue (+) and the error-driven adaptation from the GP's disambiguation (−).

## Predictions (frozen)

- **C1 (residue exists beyond punctuation):** item-level slope of A_case on object expectation at the verb (log P(" the") − log P(",")) is > 0. Pooled sign test across all models; each model's one-sided t reported.
- **C2 (error component):** slope on gp_strength < 0 (same pooled test).
- **C3 (comma part gone):** with lp(" the") and lp(",") entered separately, the comma coefficient should no longer be consistently negative. Under comma salience it cancels within pairs. Sign test.
- Net A_case: no directional prediction; reported with CIs.

If C1 fails while C3 holds, the NP/Z "commitment" residue was punctuation-driven. In that case, the evidence for a van Gompel-type lingering residue in these LMs reduces to the E004 history result (which comma salience also explains) and E002's weak "the" part.

## Result (17 models)

- **C1 confirmed:** commitment slope > 0 in **17/17** models (sign test p < 1e-4; one-sided significant in 12). The object-expectation residue survives a disambiguation that uses case (*they*) instead of punctuation, with the verb and the omitted comma identical within the pair.
- **C2 confirmed:** error slope < 0 in **15/17** (p = .001; significant in 11).
- **C3 refuted:** the comma part of the proxy remains negative in 15/17 even though punctuation salience cancels within pairs. So the comma coefficient was **not** comma-omission salience. It indexes the other side of object commitment: a verb that predicts a clause boundary is a verb whose following NP is less committed as an object.
- Net A_case: −0.41 (Qwen2.5-0.5B) to +0.24 (Gemma-3-12B-it, Qwen2.5-7B-Instruct); model-dependent, as in E002.
