"""Family-level link between comprehension lingering and priming residues (OT, 42 families).

Per family (mean over the 4 L x P cells): linger = OBS_author(GP) - OBS_author(CUE) (chat format if
present), A_L and A_S as in report_for_E010. Spearman r with family bootstrap CI. Reliability:
A split-half over target families (even/odd index in sorted order, Spearman-Brown); lingering
reliability = cross-question-set (author vs template) Spearman-Brown.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_v2 import RES, comp_table  # noqa: E402


def sb(r):
    return 2 * r / (1 + r)


def main(tags):
    rng = np.random.default_rng(0)
    for t in tags:
        g, fmt, _ = comp_table(pd.read_csv(RES / f"{t}.comp.csv"))
        lin = {}
        for qs in ("author", "template"):
            x = g[(g.verb_class == "OT") & (g.qkey == f"OBS_{qs}")].pivot_table(index=["family", "length", "plaus"], columns="form", values="logodds")
            lin[qs] = (x.GP - x.CUE).groupby("family").mean()
        p = pd.read_csv(RES / f"{t}.prime.csv.gz")
        p = p[p.verb_class == "OT"].copy()
        p["S"] = -p.lpD
        tg = sorted(p.target_family.unique())
        half = {f: i % 2 for i, f in enumerate(tg)}
        p["half"] = p.target_family.map(half)
        A = {}
        for v in ("L", "S"):
            for h in (None, 0, 1):
                q = p if h is None else p[p.half == h]
                m = q.groupby(["family", "length", "plaus", "form"])[v].mean().unstack("form")
                A[(v, h)] = ((m.GP - m.NB) - (m.CUE - m.NC)).groupby("family").mean()
        rel_lin = sb(spearmanr(lin["author"], lin["template"].reindex(lin["author"].index))[0])
        out = [f"{t:22s} rel_linger={rel_lin:.2f}"]
        for v in ("L", "S"):
            rel_A = sb(spearmanr(A[(v, 0)], A[(v, 1)])[0])
            d = pd.concat([lin["author"].rename("lin"), A[(v, None)].rename("A")], axis=1).dropna()
            r = spearmanr(d.lin, d.A)[0]
            bs = [spearmanr(*d.loc[rng.choice(d.index, len(d))].T.values)[0] for _ in range(2000)]
            lo, hi = np.nanpercentile(bs, [2.5, 97.5])
            ceil = np.sqrt(max(rel_A, 0) * max(rel_lin, 0))
            out.append(f"A_{v}: rel={rel_A:.2f} r(lin,A)={r:+.2f} [{lo:+.2f},{hi:+.2f}] ceiling={ceil:.2f}")
        print("  ".join(out))


if __name__ == "__main__":
    main(sys.argv[1:] or ["llama3.1-8b-instruct", "gemma3-12b-it", "mistral-7b", "qwen3-8b"])
