"""Fast point-estimate overview of E003 (no bootstrap): one row per model.

pass_fin : FINAL question in CUE is answered Yes (logodds > 0)        positive control 1
pass_tc  : OBS logodds higher in TC (asserted) than in CUE            positive control 2
linger   : OBS(GP) - OBS(CUE), OT, author questions, mean over cells
frac     : linger / (TC - CUE)
len      : linger(long) - linger(short)
plausGP  : OBS(GP, plausible) - OBS(GP, implausible)
A        : priming (GP-NB)-(CUE-NC) on S, OT mean over cells
GP-CTL   : priming GP vs Christianson control on S
slopeA   : prefix-matched within-family slope of A on gp_eff
"""
import glob
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_v2 import RES, comp_table  # noqa: E402

rows = []
for f in sorted(glob.glob(str(RES / "*.meta.json"))):
    t = Path(f).name[: -len(".meta.json")]
    g, fmt, oe = comp_table(pd.read_csv(RES / f"{t}.comp.csv"))
    o = g[(g.verb_class == "OT")]
    ob = o[o.qkey == "OBS_author"].groupby(["form", "length", "plaus"]).logodds.mean()
    fin = o[(o.qkey == "FINAL_author") & (o.form == "CUE")].logodds.mean()
    cells = [(L, P) for L in "SL" for P in "PI"]
    lin = {c: ob[("GP",) + c] - ob[("CUE",) + c] for c in cells}
    tc = np.mean([ob[("TC",) + c] - ob[("CUE",) + c] for c in cells])
    p = pd.read_csv(RES / f"{t}.prime.csv.gz")
    p = p[p.verb_class == "OT"]
    p["S"] = -p.lpD
    m = p.groupby(["family", "length", "plaus", "form"]).S.mean().unstack("form")
    A = (m.GP - m.NB) - (m.CUE - m.NC)
    q = pd.read_csv(RES / f"{t}.probes.csv")
    q = q[q.verb_class == "OT"].pivot_table(index=["family", "length", "plaus"], columns="probe", values="lp")
    d = pd.concat([A.rename("A"), (q.CUE_dis - q.GP_dis).rename("ge")], axis=1).dropna().reset_index()
    for k in ("A", "ge"):
        d[k + "w"] = d[k] - d.groupby(["family", "length"])[k].transform("mean")
    rows.append({"model": t, "fmt": fmt, "order": oe, "pass_fin": fin > 0, "pass_tc": tc > 0,
                 "linger": np.mean(list(lin.values())), "frac": np.mean(list(lin.values())) / tc if tc > 0 else np.nan,
                 "len": np.mean([lin[("L", P)] - lin[("S", P)] for P in "PI"]),
                 "plausGP": np.mean([ob[("GP", L, "P")] - ob[("GP", L, "I")] for L in "SL"]),
                 "A": A.mean(), "GP-CTL": (m.GP - m.CTL).mean(),
                 "slopeA": (d.Aw * d.gew).sum() / (d.gew ** 2).sum()})
df = pd.DataFrame(rows)
print(df.round(2).to_string(index=False))
df.to_csv(RES / "overview.csv", index=False)
