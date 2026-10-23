"""E015b analysis: R_cell = M(CORR,cell) - M(CTRL,cell); rho = R_cell / R_none; classification H-direct / H-later."""
import glob
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
RES = ROOT / "results/gp/E015"


def main(B=2000):
    rng = np.random.default_rng(0)
    rows = []
    for f in sorted(glob.glob(str(RES / "*__knockout.csv"))):
        t = Path(f).name[: -len("__knockout.csv")]
        d = pd.read_csv(f).pivot_table(index="id", columns=["cond", "cell"], values="M")
        R = {c: d[("CORR", c)] - d[("CTRL", c)] for c in d["CORR"].columns}
        Rn = R["none"]
        est = {c: R[c].mean() / Rn.mean() for c in R if c != "none"}
        idx = np.arange(len(Rn))
        bs = {c: [] for c in est}
        for _ in range(B):
            i = rng.integers(0, len(idx), len(idx))
            for c in est:
                bs[c].append(R[c].values[i].mean() / Rn.values[i].mean())
        r = {"model": t, "R_none": Rn.mean()}
        for c in est:
            lo, hi = np.percentile(bs[c], [2.5, 97.5])
            r.update({f"rho_{c}": est[c], f"rho_{c}_lo": lo, f"rho_{c}_hi": hi})
        r["corr_control_up"] = float((d[("CORR", "KO_ANS_CORR")] - d[("CORR", "none")]).mean())
        a, al = r["rho_KO_ANS_CLAIM"], r["rho_KO_ALL_CLAIM"]
        r["class"] = "H-direct" if a <= .5 else ("H-later" if a >= .8 and al <= .5 else "neither")
        rows.append(r)
        print(f"{t:22s} R={Rn.mean():+.2f} | rho ANS_CLAIM={a:.2f} [{r['rho_KO_ANS_CLAIM_lo']:.2f},{r['rho_KO_ANS_CLAIM_hi']:.2f}] "
              f"ANS_VALUE={r['rho_KO_ANS_VALUE']:.2f} ALL_CLAIM={al:.2f} ANS_CORR={r['rho_KO_ANS_CORR']:.2f} | "
              f"control dM={r['corr_control_up']:+.2f} | {r['class']}", flush=True)
    dd = pd.DataFrame(rows)
    dd.to_csv(RES / "summary_knockout.csv", index=False)
    print(dd["class"].value_counts().to_dict(), "| control up:", int((dd.corr_control_up > 0).sum()), "/", len(dd))


if __name__ == "__main__":
    main()
