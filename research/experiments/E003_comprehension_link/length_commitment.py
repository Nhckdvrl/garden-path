"""Post-hoc analysis of E003 data: ambiguous-region length as a commitment manipulation
(van Gompel 2006 Exp. 1 manipulated exactly this; humans: long > short transitive completions).

Per model, OT families, within family and plausibility:
  d_commit = commit_end(long) - commit_end(short)   log P(clause close) at end of NP region
  d_gpeff  = gp_eff(long) - gp_eff(short)           disambiguation error
  dA_L     = A_L(long) - A_L(short)                 production-like residue (comma-placement)
  dA_S     = A_S(long) - A_S(short)                 comprehension-like (target surprisal)
Family bootstrap CIs. Writes results/gp/E003/length_commitment.csv.
"""
import glob
from pathlib import Path

import numpy as np
import pandas as pd

RES = Path(__file__).resolve().parents[3] / "results/gp/E003"


def boot(x, B=2000, seed=0):
    x = np.asarray(x)
    rng = np.random.default_rng(seed)
    bs = [x[rng.integers(0, len(x), len(x))].mean() for _ in range(B)]
    return x.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5)


rows = []
for f in sorted(glob.glob(str(RES / "*.meta.json"))):
    t = Path(f).name[: -len(".meta.json")]
    p = pd.read_csv(RES / f"{t}.prime.csv.gz")
    p = p[p.verb_class == "OT"]
    p["S"] = -p.lpD
    out = {"model": t}
    for meas in ("L", "S"):
        m = p.groupby(["family", "length", "plaus", "form"])[meas].mean().unstack("form")
        A = ((m["GP"] - m["NB"]) - (m["CUE"] - m["NC"])).unstack("length")
        d = (A["L"] - A["S"]).groupby("family").mean()
        out[f"dA_{meas}"], out[f"dA_{meas}_lo"], out[f"dA_{meas}_hi"] = boot(d)
        out[f"A_{meas}_short"], out[f"A_{meas}_long"] = A["S"].mean(), A["L"].mean()
    q = pd.read_csv(RES / f"{t}.probes.csv")
    q = q[q.verb_class == "OT"].pivot_table(index=["family", "length", "plaus"], columns="probe", values="lp")
    ce = np.logaddexp(q["NPend_comma"], q["NPend_period"]).unstack("length")
    ge = (q["CUE_dis"] - q["GP_dis"]).unstack("length")
    out["d_commit"], out["d_commit_lo"], out["d_commit_hi"] = boot((ce["L"] - ce["S"]).groupby("family").mean())
    out["d_gpeff"], out["d_gpeff_lo"], out["d_gpeff_hi"] = boot((ge["L"] - ge["S"]).groupby("family").mean())
    rows.append(out)
df = pd.DataFrame(rows)
df.to_csv(RES / "length_commitment.csv", index=False)
cols = ["model", "d_commit", "d_gpeff", "A_L_short", "A_L_long", "dA_L", "dA_L_lo", "dA_L_hi", "dA_S", "dA_S_lo", "dA_S_hi"]
print(df[cols].round(2).to_string(index=False))
print(f"dA_L > 0 (CI): {(df.dA_L_lo > 0).sum()}/{len(df)};  dA_L < 0 (CI): {(df.dA_L_hi < 0).sum()}/{len(df)};  "
      f"d_commit > 0 (CI): {(df.d_commit_lo > 0).sum()}/{len(df)};  d_gpeff < 0 (CI): {(df.d_gpeff_hi < 0).sum()}/{len(df)}")
