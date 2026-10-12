"""E003 item-level link between comprehension lingering and priming residue A (OT families).

For each model passing both comprehension positive controls (overview.csv: pass_fin, pass_tc,
and TC-CUE > 0 with linger > 0.5 logodds so the instrument is not at floor):
  r(lingering, A)   across 42 families (family means over cells), Spearman, family bootstrap CI
  reliability       lingering author~template (Spearman); A split-half over targets (Spearman-Brown)
  prefix-matched    within-(family, length) slopes of lingering and A on gp_eff
Writes results/gp/E003/item_link.csv.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_v2 import RES, comp_table  # noqa: E402

ov = pd.read_csv(RES / "overview.csv")
valid = ov[ov.pass_fin & ov.pass_tc & (ov.linger > 0.5)].model.tolist()
rng = np.random.default_rng(0)
rows = []
for t in valid:
    g, _, _ = comp_table(pd.read_csv(RES / f"{t}.comp.csv"))
    o = g[g.verb_class == "OT"]
    lin = {}
    for qs in ("author", "template"):
        x = o[o.qkey == f"OBS_{qs}"].pivot_table(index=["family", "length", "plaus"], columns="form", values="logodds")
        lin[qs] = (x["GP"] - x["CUE"])
    p = pd.read_csv(RES / f"{t}.prime.csv.gz")
    p = p[p.verb_class == "OT"]
    p["S"] = -p.lpD
    m = p.groupby(["family", "length", "plaus", "form"]).S.mean().unstack("form")
    A = (m["GP"] - m["NB"]) - (m["CUE"] - m["NC"])
    tg = sorted(p.target_family.unique())
    h = set(np.random.default_rng(0).permutation(tg)[: len(tg) // 2])
    halves = []
    for part in (p[p.target_family.isin(h)], p[~p.target_family.isin(h)]):
        mm = part.groupby(["family", "form"]).S.mean().unstack("form")
        halves.append((mm["GP"] - mm["NB"]) - (mm["CUE"] - mm["NC"]))
    rA = spearmanr(halves[0], halves[1])[0]
    q = pd.read_csv(RES / f"{t}.probes.csv")
    q = q[q.verb_class == "OT"].pivot_table(index=["family", "length", "plaus"], columns="probe", values="lp")
    d = pd.concat([lin["author"].rename("lin"), A.rename("pA"), (q["CUE_dis"] - q["GP_dis"]).rename("ge")], axis=1).dropna().reset_index()
    fm = d.groupby("family")[["lin", "pA"]].mean()
    fam = fm.index.to_numpy()
    r = spearmanr(fm["lin"], fm["pA"])[0]
    rb = [spearmanr(*fm.loc[rng.choice(fam, len(fam))][["lin", "pA"]].T.to_numpy())[0] for _ in range(1000)]
    for k in ("lin", "pA", "ge"):
        d[k + "w"] = d[k] - d.groupby(["family", "length"])[k].transform("mean")
    sl = lambda dd, y: (dd[y + "w"] * dd["gew"]).sum() / (dd["gew"] ** 2).sum()
    fams = d.family.unique()
    bs = np.array([(lambda dd: (sl(dd, "lin"), sl(dd, "pA")))(pd.concat([d[d.family == f] for f in rng.choice(fams, len(fams))])) for _ in range(300)])
    li = lin["author"].groupby("family").mean(), lin["template"].groupby("family").mean()
    rows.append({"model": t, "r_lin_A": r, "r_lo": np.nanpercentile(rb, 2.5), "r_hi": np.nanpercentile(rb, 97.5),
                 "rel_lin": spearmanr(*li)[0], "rel_A_SB": 2 * rA / (1 + rA),
                 "slope_lin": sl(d, "lin"), "slope_lin_lo": np.percentile(bs[:, 0], 2.5), "slope_lin_hi": np.percentile(bs[:, 0], 97.5),
                 "slope_A": sl(d, "pA"), "slope_A_lo": np.percentile(bs[:, 1], 2.5), "slope_A_hi": np.percentile(bs[:, 1], 97.5)})
df = pd.DataFrame(rows)
df.to_csv(RES / "item_link.csv", index=False)
print(df.round(2).to_string(index=False))
