"""Item-level (prime family) analysis for E002: per-family A on S, its split-half
reliability over targets, and its correlation with prime-internal garden-path strength."""
import argparse, glob
from pathlib import Path
import numpy as np, pandas as pd
from scipy.stats import spearmanr
ROOT = Path(__file__).resolve().parents[3]
RES = ROOT / "results/gp/E002"

def family_A(df, targets=None):
    if targets is not None: df = df[df.target_family.isin(targets)]
    m = df.pivot_table(index="prime_family", columns="cond", values="S")
    return pd.DataFrame({"A": m.GP - m.NB - m.CUE + m.NC, "Afull": m.TB - m.NB - m.CUE + m.NC,
                         "GPminusTB": m.GP - m.TB})

ap = argparse.ArgumentParser(); ap.add_argument("--tags", nargs="*"); a = ap.parse_args()
tags = a.tags or sorted(Path(p).name[:-len(".scores.csv.gz")] for p in glob.glob(str(RES / "*.scores.csv.gz")))
rng = np.random.default_rng(0)
for t in tags:
    df = pd.read_csv(RES / f"{t}.scores.csv.gz"); df["S"] = -df.lpD
    T = np.array(sorted(df.target_family.unique())); rng.shuffle(T); h = len(T) // 2
    a1, a2 = family_A(df, T[:h]).A, family_A(df, T[h:]).A
    rel = np.corrcoef(a1, a2)[0, 1]; sb = 2 * rel / (1 + rel)
    fa = family_A(df)
    fa["A_half1"], fa["A_half2"] = a1, a2   # fixed random split of target families (seed 0)
    p = pd.read_csv(RES / f"{t}.probes.csv").pivot_table(index="family", columns="probe", values="lp")
    fa["gp_strength"] = p.CUE_dis - p.GP_dis          # prime-internal GP surprisal effect
    fa["obj_expect"] = p.V_the - p.V_comma            # object expectation at the ambiguous verb
    fa["src"] = [i.split(":")[0] for i in fa.index]
    fa.to_csv(RES / f"{t}.family_A.csv")
    r1 = spearmanr(fa.A, fa.gp_strength); r2 = spearmanr(fa.A, fa.obj_expect)
    print(f"{t:26s} splithalf(A) r={rel:+.2f} SB={sb:+.2f} | rho(A,gp_strength)={r1.statistic:+.2f} p={r1.pvalue:.3f} "
          f"| rho(A,obj_expect)={r2.statistic:+.2f} p={r2.pvalue:.3f} | A>0 in {np.mean(fa.A>0):.0%} of families")
