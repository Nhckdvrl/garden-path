"""A_L = (GP - NB) - (CUE - NC) on the production-like measure L for every model and item set
(discovery E002, held-out E005, Christianson E003), two-way bootstrap over prime x target families.
Writes paper/tables/residue_sets.csv.
"""
import glob
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research/tools"))
from prime_analysis import bootstrap  # noqa: E402

R = ROOT / "results/gp"
C = {"A_L": {"GP": 1, "NB": -1, "CUE": -1, "NC": 1}, "Afull_L": {"TB": 1, "NB": -1, "CUE": -1, "NC": 1}}
rows = []
for exp, pat in (("E002", "E002/*.scores.csv.gz"), ("E005", "E005/*.scores.csv.gz")):
    for f in sorted(glob.glob(str(R / pat))):
        t = Path(f).name[: -len(".scores.csv.gz")]
        df = pd.read_csv(f, usecols=["prime_family", "cond", "target_family", "L"])
        df = df[df.cond.isin(["GP", "CUE", "NB", "NC", "TB"])]
        r = bootstrap(df, C, B=1000)
        rows += [{"set": exp, "model": t, **x} for x in r.to_dict("records")]
for f in sorted(glob.glob(str(R / "E003/*.prime.csv.gz"))):
    t = Path(f).name[: -len(".prime.csv.gz")]
    df = pd.read_csv(f)
    df = df[df.verb_class == "OT"]
    # one prime "family" per Christianson item x length x plausibility cell
    df["prime_family"] = df.family + "|" + df.length.astype(str) + "|" + df.plaus.astype(str)
    df = df.rename(columns={"form": "cond"})[["prime_family", "cond", "target_family", "L"]]
    if not {"GP", "CUE", "NB", "NC"} <= set(df.cond):
        continue
    r = bootstrap(df[df.cond.isin(["GP", "CUE", "NB", "NC", "TB"])], C, B=1000)
    rows += [{"set": "E003_christianson", "model": t, **x} for x in r.to_dict("records")]
out = pd.DataFrame(rows)
out.to_csv(ROOT / "paper/tables/residue_sets.csv", index=False)
a = out[out.stat == "A_L"]
for s, d in a.groupby("set"):
    print(f"{s}: k={len(d)} A_L>0 {int((d.est > 0).sum())}, CI>0 {int((d.lo > 0).sum())}, CI<0 {int((d.hi < 0).sum())}; "
          f"median {d.est.median():+.2f}")
