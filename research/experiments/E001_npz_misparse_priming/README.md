# E001 — Does a ruled-out NP/Z object analysis prime later attachment in causal LMs?

**Status:** exploratory discovery run (not confirmatory). Card written 2026-10-12 *before* the model panel was run; only the GPT-2 smoke run had been observed (it is reported, not hidden).

## Gap

van Gompel et al. (2006) showed that humans who read *While the man hunted the deer ran into the woods* afterwards produce more transitive completions than after the comma version. Generic LM structural priming exists (Sinclair 2022), but nobody has asked a modern LM the specific question: **after disambiguation, does the context behave like an intransitive (final) or a transitive (initial) prime?** For a causal transformer this question is especially sharp: the hidden states of `hunted the deer` are computed before `ran` arrives and are never recomputed. Later tokens may or may not "overwrite" the influence of those states.

## Design (all 93 NP/Z families: Amouyal 69 + SAP 24; lexically identical across conditions)

| Prime | Example | Final parse of V | Comma |
|---|---|---|---|
| GP | While the man hunted the deer ran into the woods. | intransitive (transiently transitive) | no |
| CUE | While the man hunted, the deer ran into the woods. | intransitive | yes |
| TB | While the man hunted the deer it ran into the woods. | transitive | no |
| TC | While the man hunted the deer, it ran into the woods. | transitive | yes |
| MAIN / NONE | The deer ran into the woods. / no prime | — | — |

Target (every content-disjoint other family j; ~88 per prime): `L = log P("While the nurse washed the baby,") − log P("While the nurse washed, the baby")`. The two strings contain the same words and differ only in where the comma goes, i.e. in whether the NP is attached as an object.

## Contrasts and competing predictions

- `struct = TC − CUE`: ordinary transitive-vs-intransitive priming. Instrument check: it must be > 0.
- `DiD = (GP − CUE) − (TB − TC)`: the effect of removing the comma, beyond the effect that comma removal has when it changes no structure.
- `r = DiD / struct`: GP priming as a fraction of a full transitive prime.

| Account | Prediction |
|---|---|
| Final-structure priming only (complete reanalysis propagates) | DiD ≈ 0, r ≈ 0 |
| Human-like partial residue | 0 < r < 1 |
| No propagation of reanalysis into context use (priming reflects the initial / surface analysis) | r ≈ 1 |
| Punctuation style only | GP − CUE ≈ TB − TC, so DiD ≈ 0 |

Stats: family means; two-way bootstrap (prime family × target family), 1000 resamples. Unit = prime family (93).

## Correction recorded before the panel results were inspected (2026-10-12)

`DiD` is **not** a clean punctuation control. CUE puts its comma where the I-target's comma is; TC puts its comma where the T-target's comma is. A model that copies *comma position* therefore predicts GP−CUE > 0 **and** TB−TC < 0, so DiD > 0 with no misparse effect at all. DiD and `r` stay in the output, labelled confounded. The primary E001 contrast becomes the **punctuation-identical** comparison

- `GP − TB`: same verb, same words except the resumptive pronoun, no commas. Final-structure priming predicts GP < TB (by roughly the transitive-structure effect). Initial-analysis or surface priming predicts GP ≈ TB.

The no-comma intransitive baseline needed to scale this (`NB`, a strictly intransitive verb) is added in E002.

## Known open confound (to be attacked in follow-ups, not by retuning this run)

DiD controls comma style but not the surface adjacency `V the N`. A transient *analysis* account and a *surface-string* account both predict r ≈ 1. Discriminating follow-ups: verbs that cannot take an object (adjacency without an object analysis); item-level relation to the prime-internal garden-path surprisal; and manipulations that let later positions re-process the sentence.

Code: `build_materials.py`, `run.py`, `analyze.py`. Raw: `results/gp/E001/`.

## Run record

- Panel completed for 9 models (gpt2, pythia-160m, pythia-410m-s1, pythia-1.4b, pythia-2.8b, qwen2.5-0.5b, llama3.2-3b, mistral-7b, gemma2-2b), then **stopped deliberately** (2026-10-12). E002 contains every E001 condition plus a comma-free target measure, so the remaining E001 models would add nothing. Not stopped because of results.
- Raw per-pair scores are gitignored (regenerable). SHA-256 values are in `results/gp/E001/MANIFEST.sha256`.
- Finding that carries forward: on the comma-placement target, GP ≈ TB for most models (Mistral-7B: GP < TB), but this target is dominated by comma-position copying, so E001 is superseded by E002/E004.
