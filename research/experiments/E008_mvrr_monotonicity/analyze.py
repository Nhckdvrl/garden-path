"""E008 analysis (same frozen rule as E007; commitment = log[P(the)+P(a)] - log P(by))."""
import glob, importlib.util
from pathlib import Path
import numpy as np, pandas as pd
from scipy.stats import binomtest
ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("e7", ROOT / "research/experiments/E007_nps_generalization/analyze.py")
e7 = importlib.util.module_from_spec(spec); spec.loader.exec_module(e7)
EXP = "E008_within"
rows = []
for f in sorted(glob.glob(str(ROOT / f"results/gp/{EXP}/*.meta.json"))):
    t = Path(f).name[: -len(".meta.json")]
    s = pd.read_csv(ROOT / f"results/gp/{EXP}/{t}.scores.csv.gz")
    m = s.assign(S=-s.lpD).pivot_table(index="prime_family", columns="cond", values="S")
    p = pd.read_csv(ROOT / f"results/gp/{EXP}/{t}.probes.csv").pivot_table(index="family", columns="probe", values="lp")
    d = pd.DataFrame({"A": m.GP - m.NB - m.CUE + m.NC})
    d["obj_expect"] = np.logaddexp(p.V_the, p.V_a) - p.V_by
    d["gp_strength"] = p.CUE_dis - p.GP_dis
    d = d.dropna()
    bo, to, bg, tg = e7.reg(d)
    disc = pd.read_csv(e7.E2 / f"{t}.family_A.csv")
    _, dto, _, dtg = e7.reg(disc)
    rows.append({"model": t, "A": d.A.mean(), "b_obj": bo, "t_obj": to, "b_gp": bg, "t_gp": tg, "gp_mean": d.gp_strength.mean(),
                 "npz_t_obj": dto, "npz_t_gp": dtg, "M1": (to > 1.645) if dto >= 2 else None, "M2": (tg < -1.645) if dtg <= -2 else None})
r = pd.DataFrame(rows); r.to_csv(ROOT / f"results/gp/{EXP}/summary.csv", index=False)
print(r.round(2).to_string(index=False))
for g in ("M1", "M2"):
    x = r[g].dropna()
    if len(x):
        print(f"{g}: {int(x.sum())}/{len(x)} confirmed; sign test p={binomtest(int(x.sum()), len(x), 0.5, alternative='greater').pvalue:.4f}")
