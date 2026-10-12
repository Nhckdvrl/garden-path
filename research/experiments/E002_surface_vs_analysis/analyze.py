"""E002 analysis: surface string vs processing history.

Two target measures:
  L  = lpT - lpI         comma-placement preference (higher = object attachment)
  S  = -lpD              surprisal of the disambiguating word in a GP target (higher = more
                         transitive expectation); comma-free at the target.
For both, only comma-matched contrasts are interpreted:
  GP-TB, GP-NB, TB-NB (no-comma triad) and
  H = [X(CUE>GP) - X(CUE>TB)] - [X(GP>CUE) - X(TB>CUE)]  (order/processing-history test).
"""
import argparse
import glob
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
from prime_analysis import bootstrap, fmt  # noqa: E402

RES = ROOT / "results/gp/E002"
C = {
    "GP-TB": {"GP": 1, "TB": -1}, "GP-NB": {"GP": 1, "NB": -1}, "TB-NB": {"TB": 1, "NB": -1},
    "NB-NC": {"NB": 1, "NC": -1}, "GP-CUE": {"GP": 1, "CUE": -1}, "TC-CUE": {"TC": 1, "CUE": -1},
    "first_GP-TB": {"GP>CUE": 1, "TB>CUE": -1},
    "second_GP-TB": {"CUE>GP": 1, "CUE>TB": -1},
    "H": {"CUE>GP": 1, "CUE>TB": -1, "GP>CUE": -1, "TB>CUE": 1},
    "first_TB-CUE": {"TB>CUE": 1, "CUE>CUE": -1}, "second_TB-CUE": {"CUE>TB": 1, "CUE>CUE": -1},
    "first_GP-CUE": {"GP>CUE": 1, "CUE>CUE": -1}, "second_GP-CUE": {"CUE>GP": 1, "CUE>CUE": -1},
    # Added after the first two models (GPT-2, Pythia-160m) were inspected; see README "Post-hoc".
    # Punctuation-matched within pairs (GP/NB no comma; CUE/NC comma after V) and verb-bias-matched
    # across pairs (GP,CUE share the ambiguous verb; NB,NC share the intransitive verb):
    "A_objanalysis": {"GP": 1, "NB": -1, "CUE": -1, "NC": 1},
    "A_fulltrans": {"TB": 1, "NB": -1, "CUE": -1, "NC": 1},
    "verb_bias_CUE-NC": {"CUE": 1, "NC": -1},
}
R = {"rprime_GPvsNB_TB": ("GP-NB", "TB-NB"), "rA": ("A_objanalysis", "A_fulltrans")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tags", nargs="*")
    ap.add_argument("--B", type=int, default=1000)
    a = ap.parse_args()
    tags = a.tags or sorted(Path(p).name[: -len(".scores.csv.gz")] for p in glob.glob(str(RES / "*.scores.csv.gz")))
    rows = []
    for t in tags:
        df = pd.read_csv(RES / f"{t}.scores.csv.gz")
        df["S"] = -df.lpD
        for meas in ("L", "S"):
            r = bootstrap(df, C, R, B=a.B, value=meas)
            r.insert(0, "measure", meas)
            r.insert(0, "model", t)
            rows.append(r)
            print(f"{t:24s} {meas}: GP-TB={fmt(r,'GP-TB')} GP-NB={fmt(r,'GP-NB')} TB-NB={fmt(r,'TB-NB')} "
                  f"H={fmt(r,'H')} | A={fmt(r,'A_objanalysis')} Afull={fmt(r,'A_fulltrans')} rA={fmt(r,'rA')} verb={fmt(r,'verb_bias_CUE-NC')}", flush=True)
        p = pd.read_csv(RES / f"{t}.probes.csv").pivot_table(index="family", columns="probe", values="lp")
        print(f"{'':24s} manip: GPeff(alone)={(p.CUE_dis-p.GP_dis).mean():+.2f} "
              f"GPeff(afterCUE)={(p.CUEafterCUE_dis-p.GPafterCUE_dis).mean():+.2f} "
              f"NBeff={(p.NC_dis-p.NB_dis).mean():+.2f} "
              f"logodds(the vs ,)@V alone={(p.V_the-p.V_comma).mean():+.2f} afterCUE={(p.V_the_afterCUE-p.V_comma_afterCUE).mean():+.2f} "
              f"intrV={(p.NV_the-p.NV_comma).mean():+.2f}", flush=True)
    pd.concat(rows).to_csv(RES / "summary.csv", index=False)


if __name__ == "__main__":
    main()
