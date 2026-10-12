"""E001 analysis. Primary (punctuation-matched): GP - TB. Others descriptive; DiD/r are
confounded by comma-position copying (see README)."""
import argparse, glob, sys
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
from prime_analysis import bootstrap, fmt  # noqa: E402
RES = ROOT / "results/gp/E001"
C = {
    "GP_minus_TB": {"GP": 1, "TB": -1},
    "struct_comma_TC_CUE": {"TC": 1, "CUE": -1},
    "GP_minus_CUE": {"GP": 1, "CUE": -1},
    "TB_minus_TC": {"TB": 1, "TC": -1},
    "DiD_confounded": {"GP": 1, "CUE": -1, "TB": -1, "TC": 1},
    "GP_minus_MAIN": {"GP": 1, "MAIN": -1}, "TB_minus_MAIN": {"TB": 1, "MAIN": -1},
    "CUE_minus_MAIN": {"CUE": 1, "MAIN": -1}, "MAIN_minus_NONE": {"MAIN": 1, "NONE": -1},
}
R = {"r_confounded": ("DiD_confounded", "struct_comma_TC_CUE")}
ap = argparse.ArgumentParser(); ap.add_argument("--tags", nargs="*"); ap.add_argument("--B", type=int, default=1000)
ap.add_argument("--subset"); a = ap.parse_args()
tags = a.tags or sorted(Path(p).name[: -len(".scores.csv.gz")] for p in glob.glob(str(RES / "*.scores.csv.gz")))
rows = []
for t in tags:
    df = pd.read_csv(RES / f"{t}.scores.csv.gz")
    if a.subset: df = df[df.prime_family.str.startswith(a.subset)]
    r = bootstrap(df, C, R, B=a.B); r.insert(0, "model", t); rows.append(r)
    print(f"{t:26s} GP-TB={fmt(r,'GP_minus_TB')}  TC-CUE={fmt(r,'struct_comma_TC_CUE')}  GP-MAIN={fmt(r,'GP_minus_MAIN')}  TB-MAIN={fmt(r,'TB_minus_MAIN')}  CUE-MAIN={fmt(r,'CUE_minus_MAIN')}", flush=True)
suffix = f"_{a.subset.strip(':')}" if a.subset else ""
pd.concat(rows).to_csv(RES / f"summary{suffix}.csv", index=False)
