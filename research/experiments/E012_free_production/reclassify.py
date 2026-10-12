"""Offline coding of E012 generations (batched spaCy). Writes <tag>.coded.csv.gz with
cls_v1/gp_v1 (frozen coding, primary) and cls_v2/gp_v2 (post-hoc coordination refinement,
sensitivity analysis), plus comma. Usage: python reclassify.py [tags...]"""
import glob
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
from transitivity import classify_batch  # noqa: E402

RES = ROOT / "results/gp/E012"
FAMS = ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl"


def main(tags):
    import json
    frag = {json.loads(l)["family_id"]: f"{json.loads(l)['subord']} {json.loads(l)['subj_v']}" for l in open(FAMS)}
    tags = tags or sorted(Path(p).name[: -len(".meta.json")] for p in glob.glob(str(RES / "*.meta.json")))
    for t in tags:
        out = RES / f"{t}.coded.csv.gz"
        if out.exists():
            continue
        g = pd.read_csv(RES / f"{t}.gen.csv.gz", sep="\t", quoting=3, keep_default_na=False)
        pairs = [(frag[tf], c) for tf, c in zip(g.target_family, g.continuation)]
        for v in (1, 2):
            r = classify_batch(pairs, version=v)
            g[f"cls_v{v}"] = [x["cls"] for x in r]
            g[f"gp_v{v}"] = [int(x["gp_style"]) for x in r]
        g["comma"] = [int(c.strip().startswith(",")) for c in g.continuation]
        g.drop(columns=["cls", "gp_style"]).to_csv(out, sep="\t", index=False, compression="gzip")
        print(t, len(g), g.cls_v1.value_counts(normalize=True).round(3).to_dict(), g.cls_v2.value_counts(normalize=True).round(3).to_dict(), flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
