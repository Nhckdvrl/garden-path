"""E007 analysis: NP/S two-force regression, frozen G1/G2 predictions from NP/Z discovery."""
import glob
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import binomtest

ROOT = Path(__file__).resolve().parents[3]
E2 = ROOT / "results/gp/E002"


def reg(d):
    z = lambda x: (x - x.mean()) / x.std()
    f = smf.ols("A ~ zo + zg", d.assign(zo=z(d.obj_expect), zg=z(d.gp_strength))).fit()
    return f.params.zo, f.tvalues.zo, f.params.zg, f.tvalues.zg


def nps_table(exp, tag):
    s = pd.read_csv(ROOT / f"results/gp/{exp}/{tag}.scores.csv.gz")
    m = s.assign(S=-s.lpD).pivot_table(index="prime_family", columns="cond", values="S")
    p = pd.read_csv(ROOT / f"results/gp/{exp}/{tag}.probes.csv").pivot_table(index="family", columns="probe", values="lp")
    d = pd.DataFrame({"A": m.GP - m.NB - m.CUE + m.NC, "Afull": m.TB - m.NB - m.CUE + m.NC})
    d["obj_expect"] = p.V_the - p.V_that
    d["gp_strength"] = p.CUE_dis - p.GP_dis
    return d.dropna()


def main():
    rows = []
    for exp in ("E007_within", "E007_cross"):
        for f in sorted(glob.glob(str(ROOT / f"results/gp/{exp}/*.meta.json"))):
            t = Path(f).name[: -len(".meta.json")]
            d = nps_table(exp, t)
            bo, to, bg, tg = reg(d)
            disc = pd.read_csv(E2 / f"{t}.family_A.csv") if (E2 / f"{t}.family_A.csv").exists() else None
            dto = dtg = np.nan
            if disc is not None:
                _, dto, _, dtg = reg(disc)
            rows.append({"exp": exp, "model": t, "A": d.A.mean(), "Afull": d.Afull.mean(), "b_obj": bo, "t_obj": to,
                         "b_gp": bg, "t_gp": tg, "gp_mean": d.gp_strength.mean(), "npz_t_obj": dto, "npz_t_gp": dtg,
                         "G1": (to > 1.645) if dto >= 2 else None, "G2": (tg < -1.645) if dtg <= -2 else None})
    r = pd.DataFrame(rows)
    r.to_csv(ROOT / "results/gp/E007_within/summary.csv", index=False)
    print(r.round(2).to_string(index=False))
    w = r[r.exp == "E007_within"]
    for g in ("G1", "G2"):
        x = w[g].dropna()
        if len(x):
            print(f"{g}: {int(x.sum())}/{len(x)} confirmed; sign test p={binomtest(int(x.sum()), len(x), 0.5, alternative='greater').pvalue:.4f}")


if __name__ == "__main__":
    main()
