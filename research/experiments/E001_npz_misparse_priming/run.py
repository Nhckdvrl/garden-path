"""E001 scoring run: NP/Z misparse priming in causal LMs.

For each prime family i, prime condition c in {GP,CUE,TB,TC,MAIN,NONE} and each
content-disjoint target family j, score
    L(i,c,j) = log P(T_j | prime) - log P(I_j | prime)
where T_j / I_j are identical word strings differing only in comma placement
(object attachment vs main-clause subject). Context = prime + " ".

Also scores the prime-internal garden-path effect: surprisal of the first word
of the disambiguating region in GP vs CUE (and in TB vs TC for the pronoun).

Usage: python run.py --models tag=PATH [tag=PATH ...] [--batch 64]
"""
import argparse
import gzip
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
import lmscore  # noqa: E402

MAT = ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl"
OUTDIR = ROOT / "results/gp/E001"
CONDS = ["GP", "CUE", "TB", "TC", "MAIN", "NONE"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", required=True, nargs="+", help="tag=path ...")
    ap.add_argument("--batch", type=int, default=64)
    a = ap.parse_args()
    for spec in a.models:
        tag, path = spec.split("=", 1)
        if (OUTDIR / f"{tag}.meta.json").exists():
            print(f"[{tag}] exists, skip", flush=True)
            continue
        try:
            run_one(tag, path, a.batch)
        except Exception as e:  # keep the panel going; failure is logged
            print(f"[{tag}] FAILED: {e!r}", flush=True)


def run_one(tag, model_path, batch):
    import gc, torch
    fams = [json.loads(l) for l in open(MAT)]
    pairs = [(i, j) for i, fi in enumerate(fams) for j, fj in enumerate(fams)
             if i != j and not set(fi["content_stems"]) & set(fj["content_stems"])]
    items, keys = [], []
    for i, j in pairs:
        for c in CONDS:
            ctx = "" if c == "NONE" else fams[i]["primes"][c] + " "
            for t in ("T", "I"):
                items.append((ctx, fams[j][f"target_{t}"]))
                keys.append((i, c, j, t))
    # prime-internal disambiguation surprisal
    pitems, pkeys = [], []
    for i, f in enumerate(fams):
        head = f"{f['subord']} {f['subj_v']}"
        w1 = " " + f["rest"].split()[0]
        pitems += [(f"{head} {f['np']}", w1), (f"{head}, {f['np']}", w1),
                   (f"{head} {f['np']}", " " + f["pronoun"]), (f"{head} {f['np']},", " " + f["pronoun"])]
        pkeys += [(i, "GP_dis"), (i, "CUE_dis"), (i, "TB_pro"), (i, "TC_pro")]

    t0 = time.time()
    model, tok = lmscore.load(model_path)
    print(f"[{tag}] loaded in {time.time()-t0:.0f}s; {len(items)} items", flush=True)
    res = lmscore.score(model, tok, items, batch_size=batch)
    pres = lmscore.score(model, tok, pitems, batch_size=batch)
    print(f"[{tag}] scored in {time.time()-t0:.0f}s", flush=True)

    OUTDIR.mkdir(parents=True, exist_ok=True)
    acc = {}
    nstr = 0
    for (i, c, j, t), r in zip(keys, res):
        acc.setdefault((i, c, j), {})[t] = r
        nstr += r["straddle"]
    with gzip.open(OUTDIR / f"{tag}.scores.csv.gz", "wt") as f:
        f.write("prime_family,cond,target_family,lpT,lpI,L,ntokT,ntokI\n")
        for (i, c, j), d in acc.items():
            f.write(f"{fams[i]['family_id']},{c},{fams[j]['family_id']},{d['T']['lp']:.5f},{d['I']['lp']:.5f},"
                    f"{d['T']['lp']-d['I']['lp']:.5f},{d['T']['ntok']},{d['I']['ntok']}\n")
    with open(OUTDIR / f"{tag}.prime_internal.csv", "w") as f:
        f.write("family,measure,lp,ntok\n")
        for (i, m), r in zip(pkeys, pres):
            f.write(f"{fams[i]['family_id']},{m},{r['lp']:.5f},{r['ntok']}\n")
    meta = {"tag": tag, "model": model_path, "n_items": len(items), "n_pairs": len(pairs),
            "straddle_tokens": nstr, "seconds": time.time() - t0, "materials": str(MAT.relative_to(ROOT))}
    json.dump(meta, open(OUTDIR / f"{tag}.meta.json", "w"), indent=1)
    print(json.dumps(meta), flush=True)
    del model
    gc.collect(); torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
