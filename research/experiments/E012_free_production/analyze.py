"""E012 analysis (statistics frozen in README before generation).

p(c) = proportion TRANS among non-AMBIG continuations in condition c (per prime family x target,
averaged over samples), aggregated as family means. Two-way bootstrap over prime x target families.
  vG    = p(GP) - p(CUE)
  A_gen = (p(GP) - p(NB)) - (p(CUE) - p(NC))
  r_gen = (p(GP) - p(NB)) / (p(TB) - p(NB))
  style = gp_style rate GP - CUE ; NB - NC
Also reports AMBIG rate and gp_style rate per condition, and P1-P3 tallies across models.
"""
import glob
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
from prime_analysis import bootstrap, fmt  # noqa: E402

RES = ROOT / "results/gp/E012"
C = {"vG": {"GP": 1, "CUE": -1}, "A_gen": {"GP": 1, "NB": -1, "CUE": -1, "NC": 1},
     "GP-NB": {"GP": 1, "NB": -1}, "TB-NB": {"TB": 1, "NB": -1}, "TC-CUE": {"TC": 1, "CUE": -1},
     "GP-NONE": {"GP": 1, "NONE": -1}, "CUE-NONE": {"CUE": 1, "NONE": -1}}
R = {"r_gen": ("GP-NB", "TB-NB")}
CS = {"style_GP-CUE": {"GP": 1, "CUE": -1}, "style_NB-NC": {"NB": 1, "NC": -1}}


def main(B=1000, version=1):
    rows = []
    for f in sorted(glob.glob(str(RES / "*.coded.csv.gz"))):
        t = Path(f).name[: -len(".coded.csv.gz")]
        g = pd.read_csv(f, sep="\t", quoting=3, keep_default_na=False)
        g["cls"], g["gp_style"] = g[f"cls_v{version}"], g[f"gp_v{version}"]
        g["trans"] = (g.cls == "TRANS").astype(float)
        amb = g.groupby("cond").cls.apply(lambda s: (s == "AMBIG").mean())
        v = g[g.cls != "AMBIG"].groupby(["prime_family", "cond", "target_family"]).trans.mean().rename("L").reset_index()
        s = g.groupby(["prime_family", "cond", "target_family"]).gp_style.mean().rename("L").reset_index()
        r = bootstrap(v, C, R, B=B)
        rs = bootstrap(s, CS, B=B)
        r.insert(0, "model", t)
        rs.insert(0, "model", t)
        rows += [r, rs]
        pt = g[g.cls != "AMBIG"].groupby("cond").trans.mean()
        st = g.groupby("cond").gp_style.mean()
        print(f"== {t} [coding v{version}]: p(TRANS) " + " ".join(f"{c}={pt[c]:.3f}" for c in ["NONE", "GP", "CUE", "TB", "TC", "NB", "NC"]))
        print(f"   vG={fmt(r,'vG')} A_gen={fmt(r,'A_gen')} r_gen={fmt(r,'r_gen')} TB-NB={fmt(r,'TB-NB')} | "
              f"gp_style GP={st['GP']:.3f} CUE={st['CUE']:.3f} NB={st['NB']:.3f} NC={st['NC']:.3f} "
              f"style_GP-CUE={fmt(rs,'style_GP-CUE')} | AMBIG max={amb.max():.3f}", flush=True)
    out = pd.concat(rows)
    out.to_csv(RES / f"summary_v{version}.csv", index=False)
    w = out.set_index(["model", "stat"])
    models = out.model.unique()
    p1 = sum(w.loc[(m, "A_gen")].lo > 0 for m in models)
    p2 = sum(w.loc[(m, "vG")].lo > 0 for m in models)
    p3 = sum(w.loc[(m, "style_GP-CUE")].lo > 0 for m in models)
    print(f"P1 A_gen>0: {p1}/{len(models)}  P2 vG>0: {p2}/{len(models)}  P3 style GP>CUE: {p3}/{len(models)}")


if __name__ == "__main__":
    main(version=int(sys.argv[1]) if len(sys.argv) > 1 else 1)
