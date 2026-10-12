"""Numbers requested by the parallel session's E010 (frozen predictions, commit 57fa532).

Per model, OT families (42), from results/gp/E003/<tag>.prime.csv.gz and probes.csv:
  (a) net A on L and on S: A = (GP-NB) - (CUE-NC), averaged over targets, then cells, then families;
      family-bootstrap 95% CI.
  (b) prefix-matched slope of A on gp_eff within (family x length), separately for L and S;
      t = estimate / family-bootstrap SD.
Same A and gp_eff definitions as analyze_v2.cell_level; no analysis choices changed.
"""
import glob
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RES = Path(__file__).resolve().parents[3] / "results/gp/E003"
B = 1000


def per_cell(tag):
    p = pd.read_csv(RES / f"{tag}.prime.csv.gz")
    p = p[p.verb_class == "OT"].copy()
    p["S"] = -p.lpD
    out = {}
    for v in ("L", "S"):
        m = p.groupby(["family", "length", "plaus", "form"])[v].mean().unstack("form")
        out[v] = ((m.GP - m.NB) - (m.CUE - m.NC)).rename(f"A_{v}")
    q = pd.read_csv(RES / f"{tag}.probes.csv")
    w = q[q.verb_class == "OT"].pivot_table(index=["family", "length", "plaus"], columns="probe", values="lp")
    ge = (w.CUE_dis - w.GP_dis).rename("gp_eff")
    return pd.concat([out["L"], out["S"], ge], axis=1).dropna().reset_index()


def slope(d, y):
    g = d.groupby(["family", "length"])
    x = d.gp_eff - g.gp_eff.transform("mean")
    yy = d[y] - g[y].transform("mean")
    return float((x * yy).sum() / (x ** 2).sum())


def main(tags):
    rng = np.random.default_rng(0)
    rows = []
    for t in tags:
        d = per_cell(t)
        fams = d.family.unique()
        fam_means = d.groupby("family")[["A_L", "A_S"]].mean()
        res = {"model": t, "n_fam": len(fams)}
        for v in ("A_L", "A_S"):
            bs = [fam_means[v].loc[rng.choice(fams, len(fams))].mean() for _ in range(B)]
            res[v] = fam_means[v].mean()
            res[v + "_lo"], res[v + "_hi"] = np.percentile(bs, [2.5, 97.5])
        groups = {f: d[d.family == f] for f in fams}
        for v in ("A_L", "A_S"):
            est = slope(d, v)
            bs = [slope(pd.concat([groups[f] for f in rng.choice(fams, len(fams))]), v) for _ in range(B)]
            res[f"slope_{v}"] = est
            res[f"t_slope_{v}"] = est / np.std(bs, ddof=1)
        rows.append(res)
    df = pd.DataFrame(rows)
    df.to_csv(RES / "report_for_E010.csv", index=False)
    pd.set_option("display.width", 200)
    print(df.round(3).to_string(index=False))


if __name__ == "__main__":
    tags = sys.argv[1:] or sorted(Path(p).name[: -len(".meta.json")] for p in glob.glob(str(RES / "*.meta.json")))
    main(tags)
