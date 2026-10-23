"""E015 analysis (predictions frozen in README).

R = M(CORR) - M(CTRL); O = M(CORR) - M(PRE); rho_CLAIM = R(CLAIM) / R; rho_FULL = R(FULL) / R, with
R(cell) = M(CORR|cell) - M(CTRL|cell). Item bootstrap (2,000 draws). Also reported per frame.
F1 R > 0 with CI above 0 (majority); F2 O > 0 (majority); F3 rho_CLAIM <= .7 (majority).
"""
import glob
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
RES = ROOT / "results/gp/E015"


def stats(w):
    R = (w.CORR - w.CTRL).mean()
    return {"R": R, "O": (w.CORR - w.PRE).mean(),
            "rho_CLAIM": (w["CORR|CLAIM"] - w["CTRL|CLAIM"]).mean() / R,
            "rho_FULL": (w["CORR|FULL"] - w["CTRL|FULL"]).mean() / R}


def main(B=2000):
    rng = np.random.default_rng(0)
    rows = []
    for f in sorted(glob.glob(str(RES / "*.csv"))):
        if Path(f).name.startswith("summary"):
            continue
        t = Path(f).stem
        w = pd.read_csv(f).pivot_table(index="id", columns="cond", values="M").dropna()
        est = stats(w)
        bs = pd.DataFrame([stats(w.iloc[rng.integers(0, len(w), len(w))]) for _ in range(B)])
        r = {"model": t, "n": len(w)}
        for k, v in est.items():
            lo, hi = np.percentile(bs[k], [2.5, 97.5])
            r.update({k: v, f"{k}_lo": lo, f"{k}_hi": hi})
        w2 = w.assign(frame=[int(i.split("_")[0][1:]) for i in w.index])
        r["R_frames_pos"] = int((w2.groupby("frame").apply(lambda g: (g.CORR - g.CTRL).mean()) > 0).sum())
        rows.append(r)
        print(f"{t:22s} n={len(w)} R={r['R']:+.2f} [{r['R_lo']:+.2f},{r['R_hi']:+.2f}] (frames>0 {r['R_frames_pos']}/10) "
              f"O={r['O']:+.2f} [{r['O_lo']:+.2f},{r['O_hi']:+.2f}] rho_CLAIM={r['rho_CLAIM']:.2f} [{r['rho_CLAIM_lo']:.2f},{r['rho_CLAIM_hi']:.2f}] "
              f"rho_FULL={r['rho_FULL']:.2f} [{r['rho_FULL_lo']:.2f},{r['rho_FULL_hi']:.2f}]", flush=True)
    d = pd.DataFrame(rows)
    d.to_csv(RES / "summary.csv", index=False)
    n = len(d)
    print(f"F1 R>0 CI>0: {(d.R_lo > 0).sum()}/{n} | F2 O>0: {(d.O > 0).sum()}/{n} | F3 rho_CLAIM<=.7: {(d.rho_CLAIM <= .7).sum()}/{n}")


if __name__ == "__main__":
    main()
