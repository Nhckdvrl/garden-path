"""Which item properties predict lingering vs production-priming residue? (OT, family level)

Predictors per family (mean over cells): obj_expect = lp V_the - lp V_comma (commitment at V),
gp_eff = lp CUE_dis - lp GP_dis (garden-path strength), prior_cue = OBS(CUE) logodds
(pragmatic inference that V acted on NP without any misparse), prior_ctl = OBS(CTL).
Outcomes: linger (GP-CUE, OBS_author), A_L, A_S. Spearman r, family bootstrap CI.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_v2 import RES, comp_table  # noqa: E402


def main(tags):
    rng = np.random.default_rng(0)
    for t in tags:
        g, fmt, _ = comp_table(pd.read_csv(RES / f"{t}.comp.csv"))
        x = g[(g.verb_class == "OT") & (g.qkey == "OBS_author")].pivot_table(index=["family", "length", "plaus"], columns="form", values="logodds")
        fam = pd.DataFrame({"linger": (x.GP - x.CUE), "prior_cue": x.CUE, "prior_ctl": x.CTL}).groupby("family").mean()
        p = pd.read_csv(RES / f"{t}.prime.csv.gz")
        p = p[p.verb_class == "OT"].copy()
        p["S"] = -p.lpD
        for v in ("L", "S"):
            m = p.groupby(["family", "length", "plaus", "form"])[v].mean().unstack("form")
            fam[f"A_{v}"] = ((m.GP - m.NB) - (m.CUE - m.NC)).groupby("family").mean()
        q = pd.read_csv(RES / f"{t}.probes.csv")
        w = q[q.verb_class == "OT"].pivot_table(index=["family", "length", "plaus"], columns="probe", values="lp")
        fam["obj_expect"] = (w.V_the - w.V_comma).groupby("family").mean()
        fam["gp_eff"] = (w.CUE_dis - w.GP_dis).groupby("family").mean()
        lines = [f"== {t}"]
        for y in ("linger", "A_L", "A_S"):
            parts = []
            for xv in ("obj_expect", "gp_eff", "prior_cue", "prior_ctl"):
                d = fam[[y, xv]].dropna()
                r = spearmanr(d[y], d[xv])[0]
                bs = [spearmanr(*d.loc[rng.choice(d.index, len(d))].T.values)[0] for _ in range(1000)]
                lo, hi = np.nanpercentile(bs, [2.5, 97.5])
                star = "*" if lo > 0 or hi < 0 else " "
                parts.append(f"{xv}={r:+.2f}{star}")
            lines.append(f"   {y:7s} " + "  ".join(parts))
        print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1:] or ["llama3.1-8b-instruct", "gemma3-12b-it", "mistral-7b", "qwen3-8b"])
