"""Manipulation check for the plausibility effect (family bootstrap, OT families).

For each sentence form, plausibility effect on OBS logodds = mean over lengths of
OBS(form, L, P) - OBS(form, L, I). In CUE/REORD/CTL the obsolete relation is unasserted, so a
P>I difference there shows the model *uses* the continuation to judge the hunting inference.
Compare with the same difference in GP (does the continuation also correct lingering?).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_v2 import RES, comp_table  # noqa: E402


def main(tags, qset="author"):
    rng = np.random.default_rng(0)
    for t in tags:
        g, fmt, _ = comp_table(pd.read_csv(RES / f"{t}.comp.csv"))
        x = g[(g.verb_class == "OT") & (g.qkey == f"OBS_{qset}")]
        w = x.pivot_table(index="family", columns=["form", "length", "plaus"], values="logodds")
        out = []
        for form in ("GP", "CUE", "REORD", "CTL", "TC"):
            d = np.mean([w[(form, L, "P")] - w[(form, L, "I")] for L in ("S", "L")], axis=0)
            bs = [np.mean(rng.choice(d, len(d))) for _ in range(2000)]
            out.append(f"{form}: {d.mean():+.2f} [{np.percentile(bs, 2.5):+.2f},{np.percentile(bs, 97.5):+.2f}]")
        print(f"{t:28s} plaus(P-I) on OBS_{qset}:  " + "  ".join(out))


if __name__ == "__main__":
    main(sys.argv[1:] or ["mistral-7b", "llama3.1-8b-instruct"])
    main(sys.argv[1:] or ["mistral-7b", "llama3.1-8b-instruct"], "template")
