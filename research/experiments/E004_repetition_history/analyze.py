"""E004 analysis: single (E002) vs exactly repeated (E004) primes. See README."""
import argparse
import glob
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
from prime_analysis import bootstrap, fmt  # noqa: E402

E2, E4 = ROOT / "results/gp/E002", ROOT / "results/gp/E004"
C = {
    "A1": {"GP": 1, "NB": -1, "CUE": -1, "NC": 1},
    "A1full": {"TB": 1, "NB": -1, "CUE": -1, "NC": 1},
    "A2": {"GP>GP": 1, "NB>NB": -1, "CUE>CUE": -1, "NC>NC": 1},
    "A2full": {"TB>TB": 1, "NB>NB": -1, "CUE>CUE": -1, "NC>NC": 1},
    "dA": {"GP>GP": 1, "NB>NB": -1, "CUE>CUE": -1, "NC>NC": 1, "GP": -1, "NB": 1, "CUE": 1, "NC": -1},
    "dAfull": {"TB>TB": 1, "NB>NB": -1, "CUE>CUE": -1, "NC>NC": 1, "TB": -1, "NB": 1, "CUE": 1, "NC": -1},
    "GP-TB_1": {"GP": 1, "TB": -1}, "GP-TB_2": {"GP>GP": 1, "TB>TB": -1},
}
R = {"rA1": ("A1", "A1full"), "rA2": ("A2", "A2full"), "r_increment": ("dA", "dAfull")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tags", nargs="*")
    ap.add_argument("--B", type=int, default=1000)
    a = ap.parse_args()
    tags = a.tags or sorted(Path(p).name[: -len(".scores.csv.gz")] for p in glob.glob(str(E4 / "*.scores.csv.gz")))
    rows = []
    for t in tags:
        if not (E2 / f"{t}.meta.json").exists():
            print(f"{t}: E002 singles missing, skip")
            continue
        d2 = pd.read_csv(E2 / f"{t}.scores.csv.gz")
        d4 = pd.read_csv(E4 / f"{t}.scores.csv.gz")
        df = pd.concat([d2[d2.cond.isin(["GP", "CUE", "TB", "NB", "NC"])], d4[d4.cond != "CUE>CUE"],
                        d2[d2.cond == "CUE>CUE"]])
        df["S"] = -df.lpD
        p = pd.read_csv(E4 / f"{t}.probes.csv").pivot_table(index="family", columns="probe", values="lp")
        p2 = pd.read_csv(E2 / f"{t}.probes.csv").pivot_table(index="family", columns="probe", values="lp")
        manip = (f"GPeff single={(p2.CUE_dis - p2.GP_dis).mean():+.2f}  copy2={(p.CUE2_dis - p.GP2_dis).mean():+.2f}  "
                 f"NBeff copy2={(p.NC2_dis - p.NB2_dis).mean():+.2f}  "
                 f"obj@V single={(p2.V_the - p2.V_comma).mean():+.2f} afterGP={(p.V_the_afterGP - p.V_comma_afterGP).mean():+.2f}")
        print(f"\n== {t}  manip: {manip}")
        for meas in ("S", "L"):
            r = bootstrap(df, C, R, B=a.B, value=meas)
            r.insert(0, "measure", meas)
            r.insert(0, "model", t)
            rows.append(r)
            print(f"  {meas}: A1={fmt(r,'A1')} A2={fmt(r,'A2')} rA1={fmt(r,'rA1')} rA2={fmt(r,'rA2')} "
                  f"dA={fmt(r,'dA')} dAfull={fmt(r,'dAfull')} r_inc={fmt(r,'r_increment')}", flush=True)
    if rows:
        pd.concat(rows).to_csv(E4 / "summary.csv", index=False)


if __name__ == "__main__":
    main()
