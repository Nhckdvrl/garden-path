# Garden Path project: pause and handoff (2026-10-13)

**State: PAUSED by the user (2026-10-13) to work on another project.** Nothing is running: no GPU jobs, relays or monitors. Everything is committed and pushed. Resume by reading this file, then [CURRENT_UNDERSTANDING](CURRENT_UNDERSTANDING.md), then the [experiment index](experiments/README.md).

## 1. What we know (2026-10-12 → 13; 12 experiments, up to 21 models)

A NP/Z garden-path sentence (*While the man hunted the deer ran into the woods*) leaves **three separable traces** in causal LMs:

1. **Production residue of the abandoned object analysis** (the van Gompel et al. 2006 human effect transfers).
   - Net positive on the production-like measure in every model and item set (E002, E005, E009, E010; 16–17/17 models).
   - Punctuation-free (E009). Requires a *licensed* object reading, not just the string `V the N` (E011).
   - Reaches free generation: A_gen > 0 in 8/8, tracking the log-prob measure across models, ρ = .81 (E012). Scales with commitment (object expectation).
2. **Error-driven adaptation toward the resolved parse.**
   - On the comprehension-like measure (target disambiguation surprisal), scaled by the prime's disambiguation error; causal within family (E006).
   - Present in non-monotonic reanalysis (NP/Z, MV/RR), absent in NP/S (E007, E008). Dominates S, weak on L (E010).
3. **Comprehension lingering** (Yes to *Did the man hunt the deer?*).
   - Large, and grows with ambiguous-region length, as in humans.
   - Uncorrelated with (1) item by item in 10/10 valid models with reliabilities ≈ .9 (E003).
   - Does not track garden-path removal: a reordered-paraphrase context removes the garden path more but lingering less (E003c).

Methodological finding: the human paradigm's raw statistic (GP vs comma completions) is invalid for LMs. Models copy the prime's punctuation style and write garden-path sentences themselves (up to 25% of completions), which flips the sign in Llama/Qwen (E012).

Theoretical hook: in garden paths, residual-activation and error-driven accounts of structural priming predict **opposite signs**; in ordinary priming they predict the same sign. LMs show both forces at once, and the measure decides which dominates. See [library/CALIBRATION_error_vs_residue_2026-10-12.md](../library/CALIBRATION_error_vs_residue_2026-10-12.md) for ownership and novelty calibration. Searches on 2026-10-13 found no prior LM study of abandoned-parse priming.

## 2. Honest significance assessment (calibrated to ACL/EMNLP/NAACL)

- **Have:** a carefully controlled first modern-LM transfer of van Gompel (log-prob and free production, frozen predictions, held-out items, discriminating tests E006/E009/E011), a two-force account that explains why naive transfer looks model-dependent, and an item-level dissociation from comprehension lingering.
- **Missing, in order of value:**
  1. A **mechanistic causal test** of where the production residue lives. The original LM-specific hypothesis: a causal transformer never recomputes the NP's pre-disambiguation states. Proposed E013.
  2. A **within-family causal manipulation of commitment**. Only the error force has one (E006). Proposed E014.
  3. The **cause of comprehension lingering** (inferential support at answer time?). Proposed E003d.
  4. Human data for the new prediction (more surprising disambiguation → less abandoned-parse priming on comprehension-like measures). We cannot run humans; it stays a stated prediction.
- **Judgement:** close to a solid ACL/EMNLP paper. Items 1 and 2 would make it strong. Risks: effects are partly post-hoc (A defined after 2 models; E010 is the prospective check); E005 has 8 models; coding audit done by Claude, not humans.

## 3. Proposed next experiments (designed in outline, nothing run)

| ID | Question | Sketch | Discriminating prediction |
|---|---|---|---|
| E013 | Where is the production residue carried? | E002 primes, L target. (a) attention knockout from target positions to the prime's NP span vs main-clause span; (b) patch the NP-span KV from a case-disambiguated twin (E009, same token count) into the GP run | "Stale NP states" account: A_L shrinks only with NP-span intervention. Later-position re-encoding account: the main-clause intervention matters |
| E014 | Is commitment causal? | identical GP prime; preceding context raising or lowering V's object expectation (verified with the obj_expect probe) | A_L rises with induced commitment; S effect is net (commitment also raises error) |
| E003d | What drives comprehension lingering? | contexts: "The man hunted." / main clause only / both as separate sentences / neutral | inferential-support account: "The man hunted." alone *raises* lingering; main clause alone lowers it |

Write each card (frozen predictions) before scoring, as in E005–E012.

## 4. Infrastructure notes (needed to resume quickly)

- **Env:** conda `verl-clean` (torch 2.8 cu128, transformers 4.57, vLLM 0.11.0). Run with `HF_HUB_OFFLINE=1`; models come from the shared HF cache.
- **Incomplete caches** (load fails): Mistral-Small-24B on fvcrc11; Llama-3.2-1B (NousResearch), meta-llama/Llama-3.1-8B; Pythia-410m/1b (use `EleutherAI/pythia-410m-seed1`; `lmscore.load` falls back to the Pythia-160m tokenizer).
- **vLLM 0.11.0 bug:** the sampled-token buffer is sized by `max_model_len`. Keep `max_model_len ≥ max_num_seqs` (we use 1024 / 512). Use `VLLM_WORKER_MULTIPROC_METHOD=spawn` and one process per model (`E012_free_production/lane.sh`).
- **spaCy** `en_core_web_sm` is installed outside the env at `~/.local/share/gp_spacy` (path inserted by `research/tools/transitivity.py`). Its dependency parser is itself garden-pathed, so use POS tags only.
- **GPUs:** the user's budget for this project was 4 cards. Nodes: fvcrc20 (local, RTX PRO 6000 96 GB ×4) and fvcrc11 (A100 80 GB ×4); fvcrc13 is used by another project (e131). Model loading over NFS is slow, about 1–2 min per shard.
- **Scripts that wait on PIDs** (`relay*.sh`): do not use `pgrep -f` with a pattern contained in the waiting command itself. It self-matches and never exits; this happened once.
- **zsh:** globs with no match abort commands. Wrap monitors in `bash -c '... shopt -s nullglob ...'`.

## 5. Process lessons

- **Duplicate sessions (2026-10-12/13):** after "Try again" or reconnects, the desktop app restarted the CLI process for this conversation while the old process kept running its turn. For several hours two or three instances worked in parallel: they messaged each other as "peers", split E001–E012, and wasted quota. Fix: at every resume, check `ps -u xiang -o pid,lstart,args | grep ccd-cli` and walk this shell's parents to identify the live process. Stop stale garden-path CLI processes (done 2026-10-13 for PID 3370971).
- Write the card and predictions before data. Record post-hoc steps as post-hoc. Report failed predictions (E007 failed; E012 P2 failed; a poorly grounded E003 prediction is corrected in its card).
- Prefer a discriminating experiment over narrative revision. A premature narrative change on 10-13 (comma confound) was refuted by E009 the same morning.

## 6. Data provenance

| Source | Path | Use |
|---|---|---|
| Amouyal et al. 2025/2026 (MIT) | `data/gp_behavior/upstream/amouyal/` | 69 NP/Z families (E001–E006, E009, E011, E012) |
| SAP benchmark (Huang et al. 2024; MIT) | `.../upstream/sap/` | 24 NP/Z with comma controls |
| Ceháková & Chromý 2025 | `.../upstream/cehakova2025/` | held-out NP/Z (E005) |
| SyntaxGym NP/Z suites | `.../upstream/syntaxgym/` | held-out NP/Z (E005) |
| Christianson et al. 2001 appendix (transcribed from the published PDF; research use with citation) | `.../upstream/christianson2001/` | E003, E010 |

Derived materials: `data/gp_behavior/derived/*.jsonl`, built by each experiment's `build_materials.py` / `make_items.py`.
