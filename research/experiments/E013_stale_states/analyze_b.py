"""E013b (exploratory): analyse variant runs <tag>__<variant>.scores.csv.gz.

For every patch cell c present (none, NP, MC, both, NPfrom<frac>):
  A_c = (GP|c - NB|c) - (CUE - NC);  rho_c = A_c / A_none   on L and S (= -lpD).
"""
import glob
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
from prime_analysis import bootstrap, fmt  # noqa: E402

RES = ROOT / "results/gp/E013"


def main(B=1000):
    rows = []
    for f in sorted(glob.glob(str(RES / "*__*.scores.csv.gz"))):
        t = Path(f).name[: -len(".scores.csv.gz")]
        df = pd.read_csv(f)
        df["S"] = -df.lpD
        cells = sorted({c.split("|")[1] for c in df.cond.unique() if "|" in c})
        C = {f"A_{c}": {f"GP|{c}": 1, f"NB|{c}": -1, "CUE": -1, "NC": 1} for c in cells}
        R = {f"rho_{c}": (f"A_{c}", "A_none") for c in cells if c != "none"}
        for meas in ("L", "S"):
            r = bootstrap(df, C, R, B=B, value=meas)
            r.insert(0, "measure", meas)
            r.insert(0, "run", t)
            rows.append(r)
            print(f"{t:34s} {meas}: A_none={fmt(r, 'A_none')} " +
                  " ".join(f"{k}={fmt(r, k)}" for k in R), flush=True)
    if rows:
        pd.concat(rows).to_csv(RES / "summary_b.csv", index=False)


if __name__ == "__main__":
    main()
