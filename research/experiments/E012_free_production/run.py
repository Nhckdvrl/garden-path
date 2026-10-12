"""E012 free-production run (vLLM). See README for design and frozen predictions.

Usage: python run.py --models tag=path [...] [--n 2]
Writes results/gp/E012/<tag>.gen.csv.gz (one row per sample, with coding) and <tag>.meta.json.
"""
import os

os.environ.setdefault("VLLM_WORKER_MULTIPROC_METHOD", "spawn")  # CUDA must not be initialised before fork

import argparse
import gc
import gzip
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))

SPEC = ROOT / "research/experiments/E002_surface_vs_analysis/spec.jsonl"
FAMS = ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl"
OUT = ROOT / "results/gp/E012"
CONDS = ["NONE", "GP", "CUE", "TB", "TC", "NB", "NC"]


def build():
    fams = {json.loads(l)["family_id"]: json.loads(l) for l in open(FAMS)}
    spec = [json.loads(l) for l in open(SPEC)]
    prompts, keys = [], []
    for s in spec:
        if s["cond"] not in CONDS:
            continue
        st = set(fams[s["family_id"]]["content_stems"]) | set(s.get("extra_stems", []))
        ctx = s["prime"] + " " if s["prime"] else ""
        for fj in fams.values():
            if fj["family_id"] == s["family_id"] or st & set(fj["content_stems"]):
                continue
            frag = f"{fj['subord']} {fj['subj_v']}"
            prompts.append(ctx + frag)
            keys.append((s["family_id"], s["cond"], fj["family_id"], frag))
    return prompts, keys


def first_sentence(text):
    for i, ch in enumerate(text):
        if ch in ".!?\n":
            return text[: i + 1].rstrip("\n")
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--n", type=int, default=2)
    ap.add_argument("--gpu_mem", type=float, default=0.85)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    prompts, keys = build()
    print(f"{len(prompts)} prompts x {a.n} samples", flush=True)
    from vllm import LLM, SamplingParams
    for spec in a.models:
        tag, path = spec.split("=", 1)
        if (OUT / f"{tag}.meta.json").exists():
            print(f"[{tag}] exists, skip", flush=True)
            continue
        try:
            t0 = time.time()
            # vLLM 0.11.0 sizes its sampled-token pinned buffer by max_model_len, not max_num_seqs:
            # keep max_model_len >= max_num_seqs or the engine crashes in _to_list.
            llm = LLM(model=path, dtype="bfloat16", max_model_len=1024, max_num_seqs=512,
                      gpu_memory_utilization=a.gpu_mem, seed=0)
            sp = SamplingParams(n=a.n, temperature=1.0, top_p=1.0, max_tokens=24, seed=0, stop=["\n"])
            outs = llm.generate(prompts, sp)
            tg = time.time() - t0
            with gzip.open(OUT / f"{tag}.gen.csv.gz", "wt") as f:
                f.write("prime_family\tcond\ttarget_family\tsample\tcls\tcomma\tgp_style\tcontinuation\n")
                for (pf, c, tf, frag), o in zip(keys, outs):
                    for k, comp in enumerate(o.outputs):
                        cont = first_sentence(comp.text)
                        cont_s = cont.replace("\t", " ").replace("\n", " ")
                        # coding is done offline by reclassify.py (keeps the GPU free)
                        f.write(f"{pf}\t{c}\t{tf}\t{k}\tNA\t-1\t-1\t{cont_s}\n")
            meta = {"tag": tag, "model": path, "n_prompts": len(prompts), "n": a.n,
                    "gen_seconds": tg, "total_seconds": time.time() - t0}
            json.dump(meta, open(OUT / f"{tag}.meta.json", "w"))
            print(json.dumps(meta), flush=True)
            del llm
            gc.collect()
            import torch
            torch.cuda.empty_cache()
        except Exception as e:
            print(f"[{tag}] FAILED: {e!r}", flush=True)


if __name__ == "__main__":
    main()
