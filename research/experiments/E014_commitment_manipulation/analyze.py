"""E014 analysis (frozen in README).

Per model: A(f, c) = (GP - NB) - (CUE - NC) within context c, on L and on S (= -lpD), averaged
over targets. Predictors from the scored model itself, per (f, c):
  commit = log P(" the") - log P(",") after c + "While <subj> <verb>"
  error  = -log P(disambiguating word | c + GP prefix up to the NP)
Within-family regression (family-demeaned, no intercept): A ~ commit + error; bootstrap over families.
POST-HOC (labelled PH_, added after two models): gp_eff = log P(w|CUE prefix) - log P(w|GP prefix), the
NP-specific garden-path strength, as an alternative manipulation check and predictor.
K0: commit(OBJ) > commit(INT) on average and in > 70% of families.
K1: commit coefficient on A_L > 0; A_L(OBJ) - A_L(INT) > 0.
K2: on A_S, error coefficient < 0 and commit coefficient > 0.
K3: error coefficient on S < error coefficient on L.
"""
import glob
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
RES = ROOT / "results/gp/E014"


def cell_table(tag):
    df = pd.read_csv(RES / f"{tag}.scores.csv.gz")
    df["S"] = -df.lpD
    df[["ctx", "prime"]] = df.cond.str.split(":", expand=True)
    m = df.groupby(["prime_family", "ctx", "prime"])[["L", "S"]].mean().unstack("prime")
    out = pd.DataFrame({f"A_{v}": m[(v, "GP")] - m[(v, "NB")] - m[(v, "CUE")] + m[(v, "NC")] for v in ("L", "S")})
    p = pd.read_csv(RES / f"{tag}.probes.csv")
    p["ctx"] = p.cond.str.split(":").str[0]
    p = p.pivot_table(index=["family", "ctx"], columns="probe", values="lp")
    pr = pd.DataFrame({"commit": p.V_the - p.V_comma, "error": -p.GP_dis,
                       "intr_commit": p.NV_the - p.NV_comma,
                       # POST-HOC (added after 2 models, 2026-10-23): NP-specific garden-path strength
                       "gp_eff": p.CUE_dis - p.GP_dis})
    pr.index.names = ["prime_family", "ctx"]
    return out.join(pr).reset_index()


def within(t, y, xs):
    d = t.copy()
    cols = [y] + xs
    d[cols] = d[cols] - d.groupby("prime_family")[cols].transform("mean")
    X = d[xs].to_numpy()
    return np.linalg.lstsq(X, d[y].to_numpy(), rcond=None)[0]


def boot(t, y, xs, B=1000, seed=0):
    """Family bootstrap of the within-family OLS. Demeaning is within family, so a resampled family
    keeps its demeaned rows; the estimate is (sum X'X)^-1 (sum X'y) over the drawn families."""
    rng = np.random.default_rng(seed)
    cols = [y] + xs
    d = t.copy()
    d[cols] = d[cols] - d.groupby("prime_family")[cols].transform("mean")
    fams = d.prime_family.unique()
    XtX = np.stack([g[xs].to_numpy().T @ g[xs].to_numpy() for _, g in d.groupby("prime_family")])
    Xty = np.stack([g[xs].to_numpy().T @ g[y].to_numpy() for _, g in d.groupby("prime_family")])
    est = np.linalg.solve(XtX.sum(0), Xty.sum(0))
    bs = []
    for _ in range(B):
        i = rng.integers(0, len(fams), len(fams))
        bs.append(np.linalg.solve(XtX[i].sum(0), Xty[i].sum(0)))
    lo, hi = np.percentile(np.array(bs), [2.5, 97.5], axis=0)
    return est, lo, hi


def main(B=1000):
    rows = []
    for f in sorted(glob.glob(str(RES / "*.scores.csv.gz"))):
        tag = Path(f).name[: -len(".scores.csv.gz")]
        t = cell_table(tag)
        t["grp"] = t.ctx.str[:3]
        fam = t.groupby(["prime_family", "grp"])[["commit", "error", "gp_eff", "A_L", "A_S"]].mean().unstack("grp")
        dC = fam[("commit", "OBJ")] - fam[("commit", "INT")]
        dE = fam[("error", "OBJ")] - fam[("error", "INT")]
        dAL = fam[("A_L", "OBJ")] - fam[("A_L", "INT")]
        dAS = fam[("A_S", "OBJ")] - fam[("A_S", "INT")]
        dG = fam[("gp_eff", "OBJ")] - fam[("gp_eff", "INT")]
        r = {"model": tag, "n_fam": t.prime_family.nunique(), "dCommit": dC.mean(), "pFam_dCommit>0": (dC > 0).mean(),
             "PH_dGPeff": dG.mean(), "PH_pFam_dGPeff>0": (dG > 0).mean(),
             "dError": dE.mean(), "dA_L(OBJ-INT)": dAL.mean(), "dA_L_se": dAL.std() / np.sqrt(len(dAL)),
             "dA_S(OBJ-INT)": dAS.mean(), "dA_S_se": dAS.std() / np.sqrt(len(dAS))}
        for y in ("A_L", "A_S"):
            e, lo, hi = boot(t, y, ["commit", "error"], B)
            r.update({f"{y}_commit": e[0], f"{y}_commit_lo": lo[0], f"{y}_commit_hi": hi[0],
                      f"{y}_error": e[1], f"{y}_error_lo": lo[1], f"{y}_error_hi": hi[1]})
            e1, lo1, hi1 = boot(t, y, ["commit"], B)
            r.update({f"{y}_commitonly": e1[0], f"{y}_commitonly_lo": lo1[0], f"{y}_commitonly_hi": hi1[0]})
        # POST-HOC: within-family slope of A on NP-specific garden-path strength
        for y in ("A_L", "A_S"):
            e, lo, hi = boot(t, y, ["gp_eff"], B)
            r.update({f"PH_{y}_gpeff": e[0], f"PH_{y}_gpeff_lo": lo[0], f"PH_{y}_gpeff_hi": hi[0]})
        rows.append(r)
        print(f"{tag:22s} POST-HOC dGPeff(OBJ-INT)={r['PH_dGPeff']:+.2f} ({r['PH_pFam_dGPeff>0']:.0%} fams); gp_eff slope: A_L {r['PH_A_L_gpeff']:+.3f} [{r['PH_A_L_gpeff_lo']:+.3f},{r['PH_A_L_gpeff_hi']:+.3f}] "
              f"A_S {r['PH_A_S_gpeff']:+.3f} [{r['PH_A_S_gpeff_lo']:+.3f},{r['PH_A_S_gpeff_hi']:+.3f}]", flush=True)
        print(f"{tag:22s} K0 dCommit={r['dCommit']:+.2f} ({r['pFam_dCommit>0']:.0%} fams) dError={r['dError']:+.2f} | "
              f"dA_L={r['dA_L(OBJ-INT)']:+.3f}±{r['dA_L_se']:.3f} dA_S={r['dA_S(OBJ-INT)']:+.3f}±{r['dA_S_se']:.3f} | "
              f"L: commit {r['A_L_commit']:+.3f} [{r['A_L_commit_lo']:+.3f},{r['A_L_commit_hi']:+.3f}] "
              f"error {r['A_L_error']:+.3f} | S: commit {r['A_S_commit']:+.3f} [{r['A_S_commit_lo']:+.3f},{r['A_S_commit_hi']:+.3f}] "
              f"error {r['A_S_error']:+.3f} [{r['A_S_error_lo']:+.3f},{r['A_S_error_hi']:+.3f}]", flush=True)
    s = pd.DataFrame(rows)
    s.to_csv(RES / "summary.csv", index=False)
    n = len(s)
    print(f"K0 {((s.dCommit > 0) & (s['pFam_dCommit>0'] > .7)).sum()}/{n} | "
          f"K1 commit>0 {(s.A_L_commit > 0).sum()}/{n} (CI>0 {(s.A_L_commit_lo > 0).sum()}), dA_L>0 {(s['dA_L(OBJ-INT)'] > 0).sum()}/{n} | "
          f"K2 S error<0 {(s.A_S_error < 0).sum()}/{n}, S commit>0 {(s.A_S_commit > 0).sum()}/{n} | "
          f"K3 errS<errL {(s.A_S_error < s.A_L_error).sum()}/{n}")


if __name__ == "__main__":
    main()
