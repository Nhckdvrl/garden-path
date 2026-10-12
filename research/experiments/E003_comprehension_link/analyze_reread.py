"""E003b analysis: rereading / processing history and lingering comprehension.

Per model; chat format if present, else plain; averaged over answer orders and cells; family bootstrap.
Primary: reread = (GP2-GP1) - (CUE2-CUE1) on OBS_author (negative = rereading reduces lingering).
Also: GP1-CUE1 (baseline lingering), GP_CUE-CUE1 (residual after seeing the punctuated version),
QFIRST: (QFIRST_GP-GP1) - (QFIRST_CUE-CUE1); FINAL versions (positive = final relation restored).
Manipulation check (probes): disambiguator surprisal effect in GP1 (= lp CUE1 - lp GP1) vs the
second copy in GP2 / CUE_GP / GP_CUE (relative to CUE1).
"""
import glob
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RES = Path(__file__).resolve().parents[3] / "results/gp/E003b"
B = 2000


def boot(v, rng):
    v = np.asarray(v)
    bs = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(B)]
    return v.mean(), *np.percentile(bs, [2.5, 97.5])


def main(tags):
    rng = np.random.default_rng(0)
    for t in tags:
        c = pd.read_csv(RES / f"{t}.comp.csv")
        fmt = "chat" if (c.format == "chat").any() else "plain"
        c = c[c.format == fmt]
        print(f"== {t} ({fmt})")
        for vc in ("OT", "RAT"):
            for qk in ("OBS_author", "OBS_template", "FINAL_template"):
                x = c[(c.verb_class == vc) & (c.qkey == qk)]
                if x.empty:
                    continue
                w = x.groupby(["family", "cond"]).logodds.mean().unstack("cond")
                stats = {
                    "GP1-CUE1": w.GP1 - w.CUE1,
                    "reread": (w.GP2 - w.GP1) - (w.CUE2 - w.CUE1),
                    "GP2-CUE2": w.GP2 - w.CUE2,
                    "GP_CUE-CUE1": w.GP_CUE - w.CUE1,
                    "CUE_GP-CUE1": w.CUE_GP - w.CUE1,
                    "qfirst": (w.QFIRST_GP - w.GP1) - (w.QFIRST_CUE - w.CUE1),
                    "TC1-CUE1": w.TC1 - w.CUE1,
                }
                s = "  ".join(f"{k}={m:+.2f}[{lo:+.2f},{hi:+.2f}]" for k, (m, lo, hi) in
                              ((k, boot(v.dropna(), rng)) for k, v in stats.items()))
                print(f"  {vc:3s} {qk:15s} {s}")
        q = pd.read_csv(RES / f"{t}.probes.csv").pivot_table(index=["family", "length", "plaus"], columns="probe", values="lp")
        print("  manip (GP effect, nats, vs CUE1): " + "  ".join(
            f"{k}={(q.CUE1 - q[k]).mean():+.2f}" for k in ("GP1", "GP2_second", "CUE_GP_second"))
            + f"  GP_CUE_second-CUE1={(q.GP_CUE_second - q.CUE1).mean():+.2f}")


if __name__ == "__main__":
    main(sys.argv[1:] or sorted(Path(p).name[: -len(".meta.json")] for p in glob.glob(str(RES / "*.meta.json"))))
