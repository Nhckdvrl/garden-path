# Experiment index (garden-path, NP/Z misparse priming and lingering)

State on 2026-10-13: **project paused** (see [PAUSE_HANDOFF](../PAUSE_HANDOFF_2026-10-13.md)). Each card states its question, its design, the predictions written before data, and its results. Post-hoc steps are labelled. Living synthesis: [CURRENT_UNDERSTANDING](../CURRENT_UNDERSTANDING.md).

Measures used throughout:
- **L**: comma-placement attachment choice on a target fragment (production-like).
- **S**: surprisal of the disambiguating word in a garden-path target (comprehension-like).
- **A** = (GP − NB) − (CUE − NC): comma pattern and verb bias matched.

Unit of inference = prime family. Two-way bootstrap over prime × target families.

| ID | Question | Design (materials; models) | Verdict / key numbers | Status |
|---|---|---|---|---|
| [E001](E001_npz_misparse_priming/) | Does a ruled-out NP/Z object analysis prime later attachment? | 93 NP/Z families (Amouyal 69 + SAP 24); GP/CUE/TB/TC; 9 models | GP ≈ TB on L in most models. The comma-placement target is dominated by comma copying, and the planned DiD is confounded (recorded before results). | superseded by E002 |
| [E002](E002_surface_vs_analysis/) | String vs processing history; intransitive-verb controls | + NB/NC, order test; L and S; 19 models | A > 0 (defined post-hoc after 2 models). The order test failed its manipulation check and was not interpreted. Discovery set for E005. | done |
| [E003](E003_comprehension_link/) | Comprehension lingering vs priming residue on the same human items | Christianson 2001 (42 OT + 12 RAT families × length × plausibility); 21 models | Lingering is large and length-sensitive. **r(lingering, A) ≈ 0 in 10/10 valid models** (reliabilities .77–.98). Prefix-matched error slope on A < 0 in 10/10. | complete |
| E003b | Does re-reading change lingering? | same items; 10 models | Order effect with identical content; label confound; superseded by E003c | complete |
| E003c | Processing history vs primacy | context lines DIS / NEU / REORD; 7 models | DIS reduces lingering 7/7, **but REORD removes the garden path more and reduces lingering less**. Not processing history. | complete |
| [E004](E004_repetition_history/) | Does the residue need a garden-path episode? (exact repetition) | 93 families; 10–17 models | S: the repeated GP copy adds no residue. L: post-hoc configuration hypothesis, **later rejected by E011** | done |
| [E005](E005_heldout_confirmation/) | Held-out confirmation of the two forces | 48 new families (Ceháková + SyntaxGym); frozen per-model predictions | 14/18 predictions confirmed (8 models); failures reported | interim (8 models) |
| [E006](E006_error_manipulation/) | Is the error force causal? | within-family manipulation of disambiguation surprisal; 5 models | within-family slope t = −4 to −6 in the predicted models; ≈ 0 where discovery predicted ≈ 0 | done |
| [E007](E007_nps_generalization/) | Do the two forces generalize to NP/S? | NP/S families; frozen rule | **Failed** (G1 1/5, G2 0/4): monotonic reanalysis shows neither force | done |
| [E008](E008_mvrr_monotonicity/) | MV/RR (non-monotonic) | 64 families; frozen rule; 9 models | error force 6/9; commitment 0/8 | done |
| [E009](E009_case_disambiguation/) | Punctuation-free test (case disambiguation) | *hunted they ran* vs *hunted the deer ran*; 17 models | commitment slope > 0 in 17/17, error slope < 0 in 15/17 | done |
| [E010](E010_measure_dissociation/) | Production-like vs comprehension-like dissociation (prospective) | Christianson items; frozen; 16 models | net A_L > 0 in 16/16; error slope stronger on S than L 14/16; dissociation is quantitative | done |
| [E011](E011_local_coherence/) | Residue: local coherence or licensed analysis? (passive) | *While the man was hunted the deer…*; frozen; 17 models | **Analysis account**: median A_pass/A_GP = 0.10 (positive only in 5 larger/instruct models) | done |
| [E012](E012_free_production/) | Does the residue reach free production? | vLLM sampling, 57k prompts × 2 per model; POS-rule coding (99.7% gold, audited); 8 models | A_gen > 0 in **8/8**; across models ρ = .81 with A_L; the raw van Gompel contrast is driven by punctuation-style alignment (models write garden-path sentences, up to 25%) | done |

## Proposed next experiments (not started)

- **E013 (mechanism):** where is the production residue carried? Block the target's attention to, or patch, the prime's pre-disambiguation NP states vs its main-clause states.
- **E014 (commitment, causal):** an identical GP prime preceded by a context that raises or lowers V's object expectation.
- **E003d:** decompose comprehension lingering. Context "The man hunted." alone vs main clause alone vs both as separate sentences.

## Reproduction

- Code per experiment: `build_materials.py` / `make_spec.py` → `run*.py` → `analyze*.py`. Shared tools: `research/tools/{lmscore,prime_run,prime_analysis,transitivity}.py`.
- Raw per-pair scores (`*.scores.csv.gz`) and E012 raw generations (`*.gen.csv.gz`) are gitignored. Their SHA-256 values are in `results/gp/<exp>/MANIFEST.sha256`, and they are regenerable from the committed code and materials. E012 coded generations (`*.coded.csv.gz`) are committed.
