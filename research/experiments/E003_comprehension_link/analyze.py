"""E003 analysis: item-level link between comprehension residue and priming residue A.

Per model (joined on the 69 Amouyal families present in both files):
  d_obs = logodds(Yes|GP,OBS) - logodds(Yes|CUE,OBS)      lingering obsolete relation
  d_fin = logodds(Yes|GP,FINAL) - logodds(Yes|CUE,FINAL)  (negative = final relation not built)
  A     = per-family misparse priming (E002 itemlevel.py, S measure; read-only input)
Reliability: A from split-half over target families (Spearman-Brown); comprehension from
cross-format agreement (plain vs chat) when both exist. Reports Spearman r, family-bootstrap
CI, and r disattenuated by sqrt(rel_A * rel_comp). Item-level test is declared uninformative
if either reliability < .5 (pre-specified in README).
"""
import glob
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[3]
E2 = ROOT / "results/gp/E002"
E3 = ROOT / "results/gp/E003"


def sb(r):
    return 2 * r / (1 + r) if r > -1 else np.nan


def boot_r(x, y, B=2000, seed=0):
    rng = np.random.default_rng(seed)
    n = len(x)
    rs = [spearmanr(x[i], y[i])[0] for i in (rng.integers(0, n, n) for _ in range(B))]
    return np.nanpercentile(rs, [2.5, 97.5])


def main():
    rows = []
    for f in sorted(glob.glob(str(E3 / "*.comprehension.csv"))):
        tag = Path(f).name[: -len(".comprehension.csv")]
        fa = E2 / f"{tag}.family_A.csv"
        if not fa.exists():
            print(f"[{tag}] no family_A yet; skip", file=sys.stderr)
            continue
        c = pd.read_csv(f)
        piv = c.pivot_table(index=["family_id", "format"], columns=["qtype", "form"], values="logodds")
        d = pd.DataFrame({"d_obs": piv[("OBS", "GP")] - piv[("OBS", "CUE")],
                          "d_fin": piv[("FINAL", "GP")] - piv[("FINAL", "CUE")],
                          "pos_ctrl": piv[("FINAL", "CUE")]}).reset_index()
        fmts = sorted(d.format.unique())
        rel_comp = {}
        if len(fmts) == 2:
            w = d.pivot(index="family_id", columns="format")
            for k in ("d_obs", "d_fin"):
                rel_comp[k] = sb(spearmanr(w[(k, fmts[0])], w[(k, fmts[1])])[0])
        dm = d.groupby("family_id")[["d_obs", "d_fin", "pos_ctrl"]].mean()
        A = pd.read_csv(fa).set_index("prime_family")
        rel_A = sb(spearmanr(A.A_half1, A.A_half2)[0])
        j = dm.join(A, how="inner")
        for k in ("d_obs", "d_fin"):
            r = spearmanr(j.A, j[k])[0]
            lo, hi = boot_r(j.A.to_numpy(), j[k].to_numpy())
            rc = rel_comp.get(k, np.nan)
            ceil = np.sqrt(rel_A * rc) if rc == rc else np.nan
            rows.append({"model": tag, "measure": k, "n": len(j), "r": r, "lo": lo, "hi": hi,
                         "rel_A": rel_A, "rel_comp": rc, "ceiling": ceil,
                         "r_disatt": r / ceil if ceil and ceil == ceil else np.nan,
                         "informative": bool(rel_A >= .5 and (rc != rc or rc >= .5)),
                         "mean_d": j[k].mean(), "pos_ctrl_mean": j.pos_ctrl.mean(),
                         "mean_A": j.A.mean()})
    out = pd.DataFrame(rows)
    if len(out):
        E3.mkdir(parents=True, exist_ok=True)
        out.to_csv(E3 / "summary.csv", index=False)
        print(out.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
