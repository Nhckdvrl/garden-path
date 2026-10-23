"""Item-level two-force slopes on both measures (discovery set E002), all models.

For each model and measure (L, S): family-level A = (GP-NB)-(CUE-NC) (mean over targets), regressed on
standardized object expectation at the verb (commit = lp(" the") - lp(",")) and the prime's own garden-path
strength (err = lp(w|CUE prefix) - lp(w|GP prefix)). OLS with HC3 standard errors.
Writes paper/tables/item_slopes.csv.
"""
import glob
from pathlib import Path

import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[2]
R = ROOT / "results/gp/E002"
rows = []
for f in sorted(glob.glob(str(R / "*.scores.csv.gz"))):
    t = Path(f).name[: -len(".scores.csv.gz")]
    df = pd.read_csv(f, usecols=["prime_family", "cond", "target_family", "L", "lpD"])
    df["S"] = -df.lpD
    p = pd.read_csv(R / f"{t}.probes.csv").pivot_table(index="family", columns="probe", values="lp")
    X = pd.DataFrame({"commit": p.V_the - p.V_comma, "err": p.CUE_dis - p.GP_dis})
    X = (X - X.mean()) / X.std()
    for v in ("L", "S"):
        m = df.pivot_table(index="prime_family", columns="cond", values=v)
        A = (m.GP - m.NB) - (m.CUE - m.NC)
        fit = sm.OLS(A, sm.add_constant(X.loc[A.index])).fit(cov_type="HC3")
        for k in ("commit", "err"):
            rows.append({"model": t, "measure": v, "predictor": k, "b": fit.params[k], "se": fit.bse[k], "t": fit.tvalues[k]})
out = pd.DataFrame(rows)
out.to_csv(ROOT / "paper/tables/item_slopes.csv", index=False)
w = out.pivot_table(index="model", columns=["measure", "predictor"], values="t")
print(f"models {len(w)}")
for v in ("L", "S"):
    for k in ("commit", "err"):
        x = w[(v, k)]
        print(f"{v} {k}: >0 {int((x > 0).sum())}, t>1.96 {int((x > 1.96).sum())}, t<-1.96 {int((x < -1.96).sum())}")
b = out.pivot_table(index="model", columns=["measure", "predictor"], values="b")
print("err slope more negative on S than L:", int((b[("S", "err")] < b[("L", "err")]).sum()), "/", len(b))
