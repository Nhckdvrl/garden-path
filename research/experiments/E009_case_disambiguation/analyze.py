"""E009 analysis: punctuation-free residue test (see README). Frozen C1-C3."""
import glob
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import binomtest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
from prime_analysis import bootstrap, fmt  # noqa: E402

RES = ROOT / "results/gp/E009"
z = lambda x: (x - x.mean()) / x.std()
rows = []
for f in sorted(glob.glob(str(RES / "*.meta.json"))):
    t = Path(f).name[: -len(".meta.json")]
    s = pd.read_csv(RES / f"{t}.scores.csv.gz")
    s["S"] = -s.lpD
    b = bootstrap(s, {"A_case": {"GP": 1, "NOM": -1, "NB": -1, "NBNOM": 1}, "GP-NOM": {"GP": 1, "NOM": -1}},
                  B=500, value="S")
    m = s.pivot_table(index="prime_family", columns="cond", values="S")
    p = pd.read_csv(RES / f"{t}.probes.csv").pivot_table(index="family", columns="probe", values="lp")
    d = pd.DataFrame({"A": m.GP - m.NOM - m.NB + m.NBNOM, "obj": p.V_the - p.V_comma, "lthe": p.V_the,
                      "lcomma": p.V_comma, "gp": p.CUE_dis - p.GP_dis}).dropna()
    m1 = smf.ols("A ~ zo + zg", d.assign(zo=z(d.obj), zg=z(d.gp))).fit()
    m2 = smf.ols("A ~ zt + zc + zg", d.assign(zt=z(d.lthe), zc=z(d.lcomma), zg=z(d.gp))).fit()
    w = b.set_index("stat")
    rows.append({"model": t, "A_case": w.est["A_case"], "lo": w.lo["A_case"], "hi": w.hi["A_case"],
                 "t_obj": m1.tvalues.zo, "t_gp": m1.tvalues.zg, "t_the": m2.tvalues.zt, "t_comma": m2.tvalues.zc})
r = pd.DataFrame(rows)
r.to_csv(RES / "summary.csv", index=False)
print(r.round(2).to_string(index=False))
n = len(r)
for name, col, sign in (("C1 obj>0", "t_obj", 1), ("C2 gp<0", "t_gp", -1), ("C3 comma<0 (should NOT hold)", "t_comma", -1)):
    k = int((np.sign(r[col]) == sign).sum())
    sig = int((sign * r[col] > 1.645).sum())
    print(f"{name}: sign {k}/{n} (p={binomtest(k, n, 0.5, alternative='greater').pvalue:.4f}); one-sided sig {sig}/{n}")
