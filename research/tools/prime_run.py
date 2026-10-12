"""Generic NP/Z priming scorer.

Input spec JSONL (one line per prime family x condition):
  {"family_id": ..., "cond": ..., "prime": "<text or empty>",
   "probes": [[context, word, name], ...]}          # optional prime-internal surprisal probes
Targets (per target family j): comma-placement pair T/I (L = lpT - lpI), and the
target-internal disambiguating word in the GP target (lpD) and in its comma version (lpDc).
Targets: comma-placement pairs from data/gp_behavior/derived/npz_prime_families_v1.jsonl,
restricted to content-disjoint target families (stems of the prime family's E001 entry
plus any extra stems in the spec line under "extra_stems").

Writes results/gp/<exp>/<tag>.scores.csv.gz and <tag>.probes.csv.
Usage: python prime_run.py --spec SPEC --exp E002 --batch 128 --models tag=path ...
"""
import argparse
import gc
import gzip
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research/tools"))
import lmscore  # noqa: E402

FAMS = ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl"


def build(spec_path, prime_fams_path=None, targets_path=None, target_fams_path=None):
    fams = {json.loads(l)["family_id"]: json.loads(l) for l in open(target_fams_path or FAMS)}  # targets
    if targets_path:
        keep = set(json.load(open(targets_path)))
        tf = {k: v for k, v in fams.items() if k in keep}
    else:
        tf = fams
    pf = dict(fams)
    if prime_fams_path:
        pf.update({json.loads(l)["family_id"]: json.loads(l) for l in open(prime_fams_path)})
    spec = [json.loads(l) for l in open(spec_path)]
    items, keys, probes, pkeys = [], [], [], []
    for s in spec:
        fi = pf[s["family_id"]]
        st = set(fi["content_stems"]) | set(s.get("extra_stems", []))
        ctx = s["prime"] + " " if s["prime"] else ""
        for fj in tf.values():
            if fj["family_id"] == fi["family_id"] or st & set(fj["content_stems"]):
                continue
            if "D_ctx" in fj:  # generic target family (e.g. NP/S): only target-internal disambiguation
                tgt = {"D": (fj["D_ctx"], fj["D_word"]), "Dc": (fj["Dc_ctx"], fj["D_word"])}
            else:
                th = f"{fj['subord']} {fj['subj_v']}"
                w1 = " " + fj["rest"].split()[0]
                tgt = {"T": ("", fj["target_T"]), "I": ("", fj["target_I"]),
                       # target-internal disambiguation: GP target and comma target
                       "D": (f"{th} {fj['np']}", w1), "Dc": (f"{th}, {fj['np']}", w1)}
            for t, (pre, cont) in tgt.items():
                items.append((ctx + pre, cont))
                keys.append((s["family_id"], s["cond"], fj["family_id"], t))
        for c, w, name in s.get("probes", []):
            probes.append((c, w))
            pkeys.append((s["family_id"], s["cond"], name))
    return items, keys, probes, pkeys


def run_one(tag, path, items, keys, probes, pkeys, outdir, batch):
    import torch
    t0 = time.time()
    model, tok = lmscore.load(path)
    res = lmscore.score(model, tok, items, batch_size=batch)
    pres = lmscore.score(model, tok, probes, batch_size=batch) if probes else []
    acc = {}
    for k, r in zip(keys, res):
        acc.setdefault(k[:3], {})[k[3]] = r["lp"]
    with gzip.open(outdir / f"{tag}.scores.csv.gz", "wt") as f:
        f.write("prime_family,cond,target_family,lpT,lpI,L,lpD,lpDc\n")
        for (i, c, j), d in acc.items():
            T, I = d.get("T", float("nan")), d.get("I", float("nan"))
            f.write(f"{i},{c},{j},{T:.5f},{I:.5f},{T-I:.5f},{d['D']:.5f},{d['Dc']:.5f}\n")
    with open(outdir / f"{tag}.probes.csv", "w") as f:
        f.write("family,cond,probe,lp,ntok\n")
        for (i, c, n), r in zip(pkeys, pres):
            f.write(f"{i},{c},{n},{r['lp']:.5f},{r['ntok']}\n")
    meta = {"tag": tag, "model": path, "n_items": len(items), "seconds": time.time() - t0}
    json.dump(meta, open(outdir / f"{tag}.meta.json", "w"))
    print(json.dumps(meta), flush=True)
    del model
    gc.collect()
    torch.cuda.empty_cache()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--exp", required=True)
    ap.add_argument("--batch", type=int, default=128)
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--targets", default=None, help="JSON list of target family ids (subset)")
    ap.add_argument("--target_fams", default=None, help="target-family file (default: NP/Z E001 families)")
    ap.add_argument("--prime_fams", default=None, help="extra prime-family file (held-out primes); targets stay FAMS")
    a = ap.parse_args()
    outdir = ROOT / "results/gp" / a.exp
    outdir.mkdir(parents=True, exist_ok=True)
    items, keys, probes, pkeys = build(a.spec, a.prime_fams, a.targets, a.target_fams)
    print(f"{len(items)} target items, {len(probes)} probes", flush=True)
    for m in a.models:
        tag, path = m.split("=", 1)
        if (outdir / f"{tag}.meta.json").exists():
            print(f"[{tag}] exists, skip", flush=True)
            continue
        try:
            run_one(tag, path, items, keys, probes, pkeys, outdir, a.batch)
        except Exception as e:  # keep the panel going; failure is logged
            print(f"[{tag}] FAILED: {e!r}", flush=True)


if __name__ == "__main__":
    main()
