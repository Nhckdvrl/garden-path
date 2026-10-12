"""E003c analysis (statistics as defined in the E003c card, written before data).

OT families, OBS questions (author and template), logodds averaged over answer orders and cells.
Format: chat when available, else plain.
  lin_X        = (GP - CUE) under context X in {DIS, NEU, REORD}
  hist         = lin_DIS - lin_NEU        processing history predicts < 0; primacy predicts ~ 0
  hist_reord   = lin_REORD - lin_NEU
  order        = VER_GP_CUE - VER_CUE_GP  (neutral 'Version 1/2' labels)
  manip        = disambiguator logprob, GP after DIS minus GP after NEU (> 0: garden path removed)
Family bootstrap (2000).
"""
import glob
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
RES = ROOT / "results/gp/E003c"


def boot(x, B=2000, seed=0):
    rng = np.random.default_rng(seed)
    x = np.asarray(x)
    bs = [x[rng.integers(0, len(x), len(x))].mean() for _ in range(B)]
    return x.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5)


def main(tags=None):
    tags = tags or sorted(Path(p).name[: -len(".meta.json")] for p in glob.glob(str(RES / "*.meta.json")))
    rows = []
    for t in tags:
        c = pd.read_csv(RES / f"{t}.comp.csv")
        fmt = "chat" if (c.format == "chat").any() else "plain"
        c = c[(c.format == fmt) & (c.verb_class == "OT")]
        q = pd.read_csv(RES / f"{t}.probes.csv")
        q = q[q.verb_class == "OT"].pivot_table(index="family", columns="probe", values="lp")
        manip = boot((q["CTX_DIS_GP"] - q["CTX_NEU_GP"]).to_numpy())
        for qs in ("author", "template"):
            w = c[c.qkey == f"OBS_{qs}"].groupby(["family", "cond"]).logodds.mean().unstack("cond")
            lin = {x: w[f"CTX_{x}_GP"] - w[f"CTX_{x}_CUE"] for x in ("DIS", "NEU", "REORD")}
            stats = {"lin_NEU": lin["NEU"], "lin_DIS": lin["DIS"], "lin_REORD": lin["REORD"],
                     "hist": lin["DIS"] - lin["NEU"], "hist_reord": lin["REORD"] - lin["NEU"],
                     "order": w["VER_GP_CUE"] - w["VER_CUE_GP"]}
            for k, v in stats.items():
                e, lo, hi = boot(v.to_numpy())
                rows.append({"model": t, "format": fmt, "qset": qs, "stat": k, "est": e, "lo": lo, "hi": hi, "n": len(v)})
        rows.append({"model": t, "format": fmt, "qset": "-", "stat": "manip_dis_lp_gain", "est": manip[0],
                     "lo": manip[1], "hi": manip[2], "n": len(q)})
    df = pd.DataFrame(rows)
    df.to_csv(RES / "summary.csv", index=False)
    for t in tags:
        x = df[(df.model == t) & (df.qset.isin(["author", "-"]))].set_index("stat")
        f = lambda k: f"{x.est[k]:+.2f}[{x.lo[k]:+.2f},{x.hi[k]:+.2f}]"
        print(f"{t:22s} lin_NEU={f('lin_NEU')} lin_DIS={f('lin_DIS')} hist={f('hist')} hist_reord={f('hist_reord')} "
              f"order={f('order')} manip={f('manip_dis_lp_gain')}")


if __name__ == "__main__":
    main(sys.argv[1:] or None)
