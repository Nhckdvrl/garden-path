"""E013 analysis (contrasts frozen in README).

A_cell = (GP|cell - NB|cell) - (CUE - NC); cell in none / NP / MC / both.
rho_cell = A_cell / A_none; D_cell = A_cell - A_none. Measures L and S (= -lpD).
M1 (L): rho_NP <= 0.5 and rho_NP < rho_MC.   M2 (S): |D_MC| > |D_NP|.
"""
import glob
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
from prime_analysis import bootstrap, fmt  # noqa: E402

RES = ROOT / "results/gp/E013"
CELLS = ["none", "NP", "MC", "both"]
C = {f"A_{c}": {f"GP|{c}": 1, f"NB|{c}": -1, "CUE": -1, "NC": 1} for c in CELLS}
C.update({f"D_{c}": {f"GP|{c}": 1, f"NB|{c}": -1, "GP|none": -1, "NB|none": 1} for c in CELLS[1:]})
C.update({f"dGP_{c}": {f"GP|{c}": 1, "GP|none": -1} for c in CELLS[1:]})
C.update({f"dNB_{c}": {f"NB|{c}": 1, "NB|none": -1} for c in CELLS[1:]})
R = {f"rho_{c}": (f"A_{c}", "A_none") for c in CELLS[1:]}


def main(B=1000):
    rows, tally = [], {"M1": [], "M2": []}
    for f in sorted(glob.glob(str(RES / "*.scores.csv.gz"))):
        t = Path(f).name[: -len(".scores.csv.gz")]
        df = pd.read_csv(f)
        df["S"] = -df.lpD
        out = {}
        for meas in ("L", "S"):
            r = bootstrap(df, C, R, B=B, value=meas)
            r.insert(0, "measure", meas)
            r.insert(0, "model", t)
            rows.append(r)
            out[meas] = r.set_index("stat").est
            print(f"{t:22s} {meas}: A_none={fmt(r,'A_none')} rho_NP={fmt(r,'rho_NP')} rho_MC={fmt(r,'rho_MC')} "
                  f"rho_both={fmt(r,'rho_both')} | D_NP={fmt(r,'D_NP')} D_MC={fmt(r,'D_MC')}", flush=True)
        L, S = out["L"], out["S"]
        tally["M1"].append(bool(L.rho_NP <= 0.5 and L.rho_NP < L.rho_MC))
        tally["M2"].append(bool(abs(S.D_MC) > abs(S.D_NP)))
    pd.concat(rows).to_csv(RES / "summary.csv", index=False)
    for k, v in tally.items():
        print(f"{k}: {sum(v)}/{len(v)}")


if __name__ == "__main__":
    main()
