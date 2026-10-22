# Current understanding — NP/Z misparse priming in causal LMs

Living document. Each entry says what we believed, what changed it, and what is still open. Newest first. Experiments: `research/experiments/E00x_*` (cards are written before runs; post-hoc steps are labelled).

## 2026-10-23 — mechanism found: the residue is read from stale NP states, the adaptation from main-clause states (E013); scale to 32B; E014 inconclusive as frozen

**E013 (activation patching, 8 models, frozen M1/M2):** replacing only the NP's pre-disambiguation states with subject-analysis states removes most of the production residue (ρ_NP 0.01–0.71; Qwen2.5-32B 0.01). Replacing the main-clause states removes none (ρ_MC 0.74–1.94). M1 6/8, M2 7/8; direction 8/8. On S the two spans push in opposite directions in 8/8: NP states carry the residue (+), main-clause states carry the error-driven adaptation (−).
- **E013b (exploratory):** the same holds with a no-comma donor (ρ_NP 0.34–0.46), so it is not imported punctuation. The target reads the abandoned analysis from the NP's lower-half (Llama, Mistral) or lower-three-quarter (Qwen) layers.
- **Reading:** "residual activation" in LMs has a concrete architectural form. A causal transformer never recomputes states built before the disambiguation, and later text reads them.

**Scale (+ Gemma-2-9B, Qwen2.5-32B, Qwen3-32B; Qwen3-30B-A3B and Llama-3.1-70B running):**
- A_L > 0 20/20; E009 commitment slope 20/20; E011 analysis account holds (median ratio 0.10).
- E012 A_gen > 0 10/11 (v1) / 11/11 (v2), style alignment 11/11.
- The two 32B Qwen models show net A_S < 0: adaptation dominates S at scale.

**E014 (commitment by context, 10 models):** the frozen verb-level manipulation check failed (0/10), so the confirmatory test is uninformative. Post-hoc: the contexts strengthened the NP-specific garden path (+0.9 to +1.7 nats, 10/10), and that *raised* A_S in 9/10 (7 significant). This contradicts an error-only account. On L the effect is model-dependent.

**E005 final (20-model panel):** the frozen held-out between-family test confirms the error sign (9/15, p = .0005), not commitment on S (6/15). The 8-model interim (14/18) overstated support.

**Paper spine now (see research/TOPVENUE_PLAN_2026-10-23.md):**
- C1: the residue persists (L, free generation, controls, 20 models);
- C2: two opposite forces (error causal E006; residue causal E013; E014 supporting), with measure dependence (E010);
- C3: stale-state mechanism (E013/E013b);
- method point: punctuation alignment (E012) and the QA-lingering dissociation (E003).

## 2026-10-13 (evening) — the residue reaches free production (E012); comprehension lingering is not processing history (E003c)

**E012 (free production, 8 models, frozen predictions):** with punctuation style and verb bias controlled, garden-path primes raise transitive *completions* in 8/8 models (A_gen +0.03 to +0.10). The cross-model size tracks the log-prob production measure L (ρ = .81). The raw human statistic (GP vs comma) is dominated by punctuation-style alignment: models reproduce the prime's comma-less resolved structure, writing garden-path sentences themselves in up to 25% of completions, so vG is negative in Llama/Qwen and positive in Gemma/Mistral/Pythia. Transfer of the van Gompel paradigm to LMs therefore *requires* the style control.

**E003 complete (21 models) + E003c (7):** comprehension lingering (Christianson items) is large and grows with ambiguous-region length. It is uncorrelated with the priming residue at the item level in 10/10 valid models (reliabilities ≈ .9). A context that states only the main clause reduces it (7/7). But a full reordered paraphrase that removes the garden path *more* completely reduces it *less*. So LM comprehension lingering is not simply "having been garden-pathed": inferential support available at answer time is a candidate.

**Overall picture (three separable phenomena, each measurement-specific):**
1. **Production residue** of the abandoned object analysis: needs a licensed object reading (E011), scales with commitment, reaches generation (E012). This is the van Gompel transfer, robust across models and item sets.
2. **Error-driven adaptation** toward the resolved parse: comprehension-like surprisal measure; causal within family (E006); reanalysis-type dependent (NP/Z, MV/RR, not NP/S).
3. **Comprehension lingering** (QA): large, length-sensitive, dissociated from (1) item by item, and not tracking garden-path removal.

## 2026-10-13 (evening) — free production (E012, interim), comprehension lingering (E003 final, E003c), and where the story stands

**E012 (free completions, 3/8 models so far; frozen P1–P4):** after a prime, models complete `While the nurse washed …`, coded by POS rules (gold 99.7%; audit on real generations ~90–97% per class).
- **P1 holds 3/3:** A_gen (comma- and verb-matched) is +0.03 … +0.10, i.e. 13–22% of a full transitive prime. The abandoned-object residue reaches actual production, but it is small.
- **P2 fails 0/3:** the raw van Gompel contrast GP − CUE is −0.14, +0.01, −0.14 (humans +4.5 points). Primes without a comma (GP and NB) make models write comma-less clauses whose NP is a new subject.
- **P3 holds 3/3, large:** after a GP prime, 21–25% of completions are themselves garden-path sentences (intransitive and comma-less), against 0.4–2.4% after CUE. Production is dominated by alignment to the prime's *resolved structure and punctuation style*. Human completions were spoken, so they could not show this.

**E003 final (21 models; 10 pass the comprehension controls):** comprehension lingering (*Did the man hunt the deer?*) and the priming residue are unrelated at the item level in 10/10 models (r = −.30 … +.15; reliabilities .77–.98). Priming falls with disambiguation error on prefix-matched items (10/10 negative).
**E003c (3 instruction models):** a disambiguating context line ("The deer ran into the woods.") removes most lingering (3/3). A full matrix-subordinate paraphrase removes the garden path *more* completely (disambiguator surprisal) yet reduces lingering less. The neutral-label order effect is inconsistent across models (−2.8, −0.3, +2.7), so the E003b order effect is **not** evidence for processing history. Lingering is not a simple function of whether the GP sentence was garden-pathed.

**Where the story stands (significance check):**
1. Robust: van Gompel's abandoned-analysis residue transfers to LMs (17/17 on L; 3/3 in free production). It requires a licensed object analysis (E011) and scales with commitment.
2. Robust: the same garden path drives error-driven adaptation toward the resolved parse (S; causal within family, E006; prefix-matched human items, E003).
3. New and potentially important for anyone transferring the paradigm: in free production the raw human contrast **reverses** because of punctuation and structure alignment. A naive replication would conclude "LMs show the opposite of humans".
4. Comprehension lingering is a separate phenomenon from the priming residue.
**Gaps:** a causal commitment manipulation; a single crisp headline (currently four findings); generality beyond NP/Z for the residue (MV/RR, NP/S showed no commitment slope on S).

## 2026-10-13 (afternoon) — E011: the production-like residue needs a licensed object analysis (configuration account rejected)

**Frozen test (17 models, 81 families):** passive primes (*While the man was hunted the deer ran…*) contain the same adjacency `hunted the deer` but never license an object reading. On L, A_pass / A_GP has median **0.10** (plausible half −0.08). A_pass > 0 in only 5/17 and **< 0 in 7/17**. Pre-registered verdict: **analysis account**. The post-hoc configuration hypothesis from E004 (L) is rejected for the panel as a whole.

**Revised understanding:** the production-like residue is a genuine abandoned-analysis effect (van Gompel 2006 transfers): it scales with commitment (E002/E005/E009/E010) and requires that the object analysis was actually available (E011). It coexists with error-driven adaptation toward the resolved parse on comprehension-like measures (E006 causal; E010 prospective).

**Open:** (i) the 5 models with partial passive residue are the larger or instruction-tuned ones (ratio 0.22–0.55). A configuration-level contribution may grow with model strength; check with the remaining large models. (ii) Generation-based production evidence (free completions, as in the human paradigm) is still missing. (iii) The commitment force still lacks a within-family causal manipulation.

## 2026-10-13 (late morning) — the two forces separate by MEASURE: production-like residue vs comprehension-like adaptation (post-hoc; prospective test E010 pending)

Checking the item-level structure on the second target measure (L = comma-placement attachment choice, comma-matched within A's pairs) against S (target disambiguation surprisal):

| Prime set | net A_L > 0 | error slope on S < 0 | error slope on L < 0 | commitment slope L > 0 / S > 0 |
|---|---|---|---|---|
| E002 discovery | 18/18 | 17/18 | 3/18 | 18/18 / 18/18 |
| E005 held-out | 17/17 | 15/17 | 10/17 | 13/17 / **8/17** |
| E009 case controls | 17/17 | 15/17 | 5/17 | 15/17 / 17/17 |

**Revised understanding:** a garden-path prime (i) **raises production-like choice of the abandoned object attachment**, net positive in every model on every item set, scaling with commitment and showing no error slope: the van Gompel (2006) human pattern transfers robustly. (ii) It also **lowers the surprise of later garden-path resolutions**, scaled by the disambiguation error and causal within family (E006): the human syntactic-adaptation pattern (Fine et al. 2013). In humans these come from different literatures and tasks. In LMs they coexist in one context and the **measure** determines which dominates. The earlier conclusion that the net effect is model-dependent was a property of S alone.

**Prospective test (E010, Christianson items, 16 models):** net A_L > 0 in 16/16 (confirmed); error slope more negative on S than L in 14/16 (confirmed); the error slope on L is not zero but weak (10/16 negative, 2 significant). So the dissociation is quantitative: adaptation dominates comprehension-like measures, residue dominates production-like ones.

**Caveats:** first discovered post-hoc; E010 is the prospective check.

**Peer-session corroboration (E003, Christianson OT items, 42 families, reliabilities ≥ .90; reported by the peer, not re-analysed here):** A_L tracks object expectation at the verb in 4/4 models (r = +.27 to +.59): the commitment force on independent items. Comprehension lingering (Yes rates to *Did the man hunt the deer?*, .74–.93) is near ceiling. Its item variance follows the CUE-condition pragmatic baseline, not obj_expect, gp_eff or A_L, and corr(lingering, A_L) ranges −.31 to +.14. Comprehension lingering and the production-like residue are both large but governed by different item properties: the two "residues" dissociate.

**Further hypothesis (post-hoc, E004 on L):** the two forces may differ in *kind*. On L, an exact non-garden-pathed GP copy adds roughly as much object-attachment residue as a TB copy (in the 5 models where repetition is not saturated), unlike on S. So the production-like residue may be **configuration-level** (local coherence of `V the N`), not a lingering misanalysis episode, while the comprehension-like adaptation needs the garden-path error. Test: E011. The commitment slope on S is weak on held-out items (8/17), so commitment is more robust on L. The constructions beyond NP/Z (E007/E008) have only S.

## 2026-10-13 (morning) — CORRECTION: the commitment residue survives punctuation-free disambiguation (E009)

The previous entry claimed the NP/Z commitment residue was "entangled with comma-omission salience" and that evidence for a lingering residue was weak. **E009 tested that and refuted it.** With case disambiguation (*hunted they ran* vs *hunted the deer ran*: same verb, same omitted comma), the commitment slope is positive in **17/17** models (12 significant) and the error slope negative in 15/17. The comma coefficient persists even where punctuation salience cancels, so it reflects low object commitment, not punctuation. Comma-omission salience (NB/NC, 17/17) is real, but it is a separate stylistic adaptation, not the source of the residue.

**Current picture (NP/Z):** two forces with opposite signs, both robust and both punctuation-independent: (+) residue scaling with how strongly the model committed to the object reading; (−) adaptation scaling with the disambiguation error (causal within family, E006). The net effect is model-dependent.

**Across constructions:** the error force appears in non-monotonic MV/RR (E008: 6/9 predicted models) and not in monotonic NP/S (E007: 0–2/9). The commitment force has been detected only in NP/Z (MV/RR 0/8; NP/S 1/8). Whether that reflects construction or the weaker verb-position commitment proxies used outside NP/Z is unresolved.

**Lesson recorded:** a post-hoc decomposition (the "the" vs "," parts of the proxy) suggested a confound. The right move was a discriminating experiment (E009), not a narrative revision. The narrative revision in the previous entry was premature and is superseded.

## 2026-10-13 (early) — [SUPERSEDED by the morning correction] the "commitment residue" is entangled with comma-omission salience; error-driven adaptation is the robust finding

**What changed:**
- **E008 (MV/RR, interim):** the error slope generalizes (3/4 predicted models), the commitment slope does not (0/5). NP/S (E007) shows neither, despite larger disambiguation errors than MV/RR. So the error component follows **non-monotonic reanalysis** (structure destroyed: NP/Z, MV/RR), not merely surprise size.
- **Post-hoc check prompted by E007/E008:** the NP/Z commitment proxy (log P(the) − log P(,) at the verb) splits into a weak object part (+ in 17/17 models, t > 2 in 5) and a comma part (− in 17/17, t < −2 in 8). Direct test on **unambiguous** NB/NC pairs: omitting a comma that the verb made likely lowers target S in **17/17** models. Comma-omission salience is a real, itself error-driven, *stylistic* adaptation, and it can mimic a "lingering-object residue" in NP/Z. It also explains why the commitment slope appeared only in NP/Z (the only construction with comma omission).

**Revised understanding:**
1. The most robust phenomenon is **prediction-error-driven adaptation toward what the garden-path sentence actually turned out to be**: structurally (the resolved parse; causal in E006; NP/Z and MV/RR, not monotonic NP/S) and stylistically (omitted commas).
2. Evidence for a van Gompel-type **lingering abandoned-parse residue** in these LMs is weaker than the evening entry claimed: a weak object-expectation part, plus E004's history result, which comma salience also explains. E009 (case disambiguation, punctuation-free) tests whether any residue survives.
3. Humans show a net *transitive* (residue) effect (van Gompel 2006). If E009 finds no residue in LMs, the LM–human contrast becomes the headline: **LMs adapt to the resolved structure where humans retain the abandoned one** (in production priming).

## 2026-10-12 (night) — error force is causal within family; two-force structure is near-universal; net effect is not

**New evidence:**
- **E006 (within-family manipulation, prefix fixed so commitment is fixed):** more surprising disambiguations produce more negative A. Llama-3.2-3B t = −6.3, Qwen2.5-0.5B −6.4, Pythia-1.4b −4.1; GPT-2 −1.4 and Pythia-410m −1.3, which are exactly the models whose discovery error slope was ≈ 0. Robust to generated-only variants, a naturalness covariate, and auxiliary-vs-lexical first word. The relevant error is surprisal **at the disambiguation point**; surprisal summed over the whole continuation predicts little. So the error-driven component is a causal effect of the disambiguation event, not a between-family correlate.
- **E005 (held-out, frozen rule):** 14/18 predictions confirmed in 8 models. Failures reported, notably Llama-3.2-3B's *between-family* error slope (null on held-out). Lesson: between-family regressions at n ≈ 24 per source are fragile; within-family manipulations carry the weight.
- **E002 panel (17 models):** commitment slope > 0 in 17/17; error slope < 0 in 15/17 (exceptions: GPT-2, Pythia-160m, the weakest garden-pathers). Net A ranges from −0.33 to +0.37 and is not ordered by size.

**Revised understanding:** "Does an LLM show van Gompel's lingering-parse priming?" has a model-dependent answer because it reads out the **net** of two opposing, separately measurable forces. Those forces are stable across 17 LMs. The commitment force is supported between families (17/17 discovery, 5/7 held-out) and by the E004 history test, but it has **no within-family causal manipulation yet**.

**Update (E007, NP/S):** the two-force structure did **not** generalize to NP/S under a frozen rule (G1 1/5, G2 0/4; net A ≈ 0), although A is reliable there and the predictors vary as much as in NP/Z. So the structure is not a property of every garden path. Candidate explanation from classic reanalysis theory: NP/S reanalysis is monotonic (no committed structure destroyed), NP/Z is non-monotonic. Test: MV/RR (E008).

**Open (priority order):**
1. Does MV/RR (non-monotonic) show the two-force structure (E008)? If yes, the boundary is plausibly reanalysis type; if no, NP/Z-specific factors (clause boundary, comma-less style) are the better explanation.
2. A within-family commitment manipulation (peer session E003 crosses plausibility × length on Christianson items, which gives a partial handle).
3. Human prediction: the error component implies that, in humans, garden paths with more surprising disambiguation should show *less* transitive priming. Testable with van Gompel-style designs plus cloze-normed items.

## 2026-10-12 (evening) — "Does the abandoned parse prime?" is the wrong unit of question

**Before:** following van Gompel et al. (2006) and Pilot B, we asked whether a ruled-out NP/Z object analysis primes later transitive structure: yes/no, and how much relative to a real transitive.

**What changed it (E002, discovery; 93 Amouyal+SAP families; 6 base LMs so far):**
- With punctuation- and verb-bias-matched contrast A = (GP−NB) − (CUE−NC) on a comma-free target measure (surprisal of the target's disambiguating word), the **net** residue ranges from **+0.22** (GPT-2; ≈47% of a true transitive prime) to **−0.29** (Llama-3.2-3B). Several Pythia models sit near 0.
- At the item level, A is the sum of two components with **opposite signs**, predicted by nearly uncorrelated variables:
  - **commitment** (model's object expectation at the ambiguous verb) → more transitive priming. Positive in all 6 models (t = 2.0–4.7).
  - **prediction error** (prime's own garden-path surprisal at disambiguation) → less transitive priming. Negative in the larger models (Llama-3.2-3B t = −5.5, Pythia-2.8b −3.1, Pythia-1.4b −2.5), ≈0 in the smallest.
- These match the two classic human theory families: **residual activation** (van Gompel 2006) vs **error-driven implicit learning** (Chang et al. 2006; Jaeger & Snider 2013). In a garden-path prime they push in opposite directions.
- E004 (exact repetition): a second, non-garden-pathed GP copy adds little transitive priming compared with a second TB copy (GPT-2, Pythia-410m, Pythia-1.4b). The residue depends on the garden-path processing episode, not on the string.

**Now:** the scientific object is the **balance** of two forces and what controls it (item properties, model scale/training), not a binary lingering effect. Human net data (van Gompel: GP > comma) suggest activation dominates in humans at the net level. Whether an error-driven component is hidden in human data is an open question this framing raises.

**Status:** exploratory. Held-out confirmation (E005: 48 SyntaxGym + Ceháková families, frozen prediction rule) is running.

**Open:**
1. Does the two-component structure replicate on held-out items (E005)?
2. Is the error component causal? Plan: E006, varying disambiguation surprisal within family with a fixed prefix.
3. How does the balance change with model scale, family and instruction tuning (full panel)?
4. Link to comprehension (peer session's E003): do items the model misunderstands carry more residue?

## 2026-10-12 (afternoon) — measurement corrections that shaped the above

- **E001:** the comma-placement target is dominated by **comma-position copying**. The planned DiD control was itself confounded (recorded before panel results). Only punctuation-matched contrasts are interpretable, which led to the comma-free target measure.
- **E002 order test:** a comma-dropped copy of a sentence just read with a comma is still garden-pathed (it is a *deviant* copy), so the planned processing-history manipulation failed its precondition and is not interpreted. Exact repetition (E004) replaced it.
- The verb-bias-matched contrast A was introduced after inspecting 2 models (labelled post-hoc); every later model and the held-out set are evaluated with it unchanged.
