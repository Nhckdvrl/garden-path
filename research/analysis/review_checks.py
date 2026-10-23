"""Analyses added in response to the simulated ARR review (2026-10-24). All use existing scores; post-hoc.

1. Generic-uncertainty control: does the prime's garden-path strength also predict the residue on the
   *comma* target's disambiguating word (Sc = -lpDc), where that word is expected? A structural adaptation
   predicts an error slope on S but not on Sc.
2. Collinearity of the two item-level predictors, and the S error slope with the family's punctuation
   adaptation (NB - NC on S) as a covariate.
3. Joint item bootstrap of the panel mean of A_L and A_S (the same prime and target families are resampled
   for every model in each draw, so the dependence between models is kept).
4. Sampled text: the raw GP - CUE contrast recomputed after removing completions that are themselves
   comma-less garden-path sentences, and its across-model relation to the rate of such completions.
5. Spearman correlation of A_gen with A_L over all models with sampled text.
Writes paper/tables/review_checks.json.
"""
import glob
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[2]
R = ROOT / "results/gp"
out = {}


def fam_table(t):
    df = pd.read_csv(R / f"E002/{t}.scores.csv.gz", usecols=["prime_family", "cond", "target_family", "L", "lpD", "lpDc"])
    df["S"], df["Sc"] = -df.lpD, -df.lpDc
    return df


def A_of(m):
    return (m["GP"] - m["NB"]) - (m["CUE"] - m["NC"])


models = sorted(Path(p).name[: -len(".scores.csv.gz")] for p in glob.glob(str(R / "E002/*.scores.csv.gz")))
rows = []
cache = {}
for t in models:
    df = fam_table(t)
    cache[t] = df
    p = pd.read_csv(R / f"E002/{t}.probes.csv").pivot_table(index="family", columns="probe", values="lp")
    X = pd.DataFrame({"commit": p.V_the - p.V_comma, "err": p.CUE_dis - p.GP_dis})
    r = {"model": t, "corr_commit_err": X.corr().iloc[0, 1]}
    Xs = (X - X.mean()) / X.std()
    for v in ("S", "Sc", "L"):
        m = df.pivot_table(index="prime_family", columns="cond", values=v)
        A = A_of(m)
        f = sm.OLS(A, sm.add_constant(Xs.loc[A.index])).fit(cov_type="HC3")
        r[f"t_err_{v}"], r[f"t_commit_{v}"] = f.tvalues["err"], f.tvalues["commit"]
        if v == "S":
            punct = (m["NB"] - m["NC"]).rename("punct")
            Z = Xs.loc[A.index].join((punct - punct.mean()) / punct.std())
            f2 = sm.OLS(A, sm.add_constant(Z)).fit(cov_type="HC3")
            r["t_err_S_punctcov"] = f2.tvalues["err"]
    rows.append(r)
d = pd.DataFrame(rows)
vif = 1 / (1 - d.corr_commit_err ** 2)
out["collinearity"] = {"corr_median": float(d.corr_commit_err.median()), "corr_range": [float(d.corr_commit_err.min()), float(d.corr_commit_err.max())],
                       "vif_max": float(vif.max())}
out["error_slope"] = {
    "S_neg": int((d.t_err_S < 0).sum()), "S_sig_neg": int((d.t_err_S < -1.96).sum()),
    "Sc_neg": int((d.t_err_Sc < 0).sum()), "Sc_sig_neg": int((d.t_err_Sc < -1.96).sum()), "Sc_sig_pos": int((d.t_err_Sc > 1.96).sum()),
    "Sc_median_t": float(d.t_err_Sc.median()), "S_median_t": float(d.t_err_S.median()),
    "S_with_punct_cov_neg": int((d.t_err_S_punctcov < 0).sum()), "S_with_punct_cov_sig_neg": int((d.t_err_S_punctcov < -1.96).sum()),
    "n": len(d)}
print("collinearity", out["collinearity"])
print("error slopes", out["error_slope"])

# 3. joint item bootstrap of the panel mean
rng = np.random.default_rng(0)
arrs = {}
for t, df in cache.items():
    for v in ("L", "S"):
        piv = df.pivot_table(index=["prime_family", "target_family"], columns="cond", values=v)
        arrs[(t, v)] = {c: piv[c].unstack("target_family") for c in ["GP", "CUE", "NB", "NC"]}
P = sorted(cache[models[0]].prime_family.unique())
T = sorted(cache[models[0]].target_family.unique())
mats = {k: {c: a.reindex(index=P, columns=T).to_numpy() for c, a in v.items()} for k, v in arrs.items()}


def panel(pi, ti, v):
    vals = []
    for t in models:
        mm = {c: np.nanmean(np.nanmean(a[np.ix_(pi, ti)], axis=1)) for c, a in mats[(t, v)].items()}
        vals.append((mm["GP"] - mm["NB"]) - (mm["CUE"] - mm["NC"]))
    return np.mean(vals)


for v in ("L", "S"):
    full = panel(np.arange(len(P)), np.arange(len(T)), v)
    bs = [panel(rng.integers(0, len(P), len(P)), rng.integers(0, len(T), len(T)), v) for _ in range(500)]
    lo, hi = np.percentile(bs, [2.5, 97.5])
    out[f"panel_mean_A_{v}"] = [float(full), float(lo), float(hi)]
    print(f"panel mean A_{v} = {full:.3f} [{lo:.3f}, {hi:.3f}] (joint item bootstrap, {len(models)} models)")

# 4./5. sampled text
g = []
for f in sorted(glob.glob(str(R / "E012/*.coded.csv.gz"))):
    t = Path(f).name[: -len(".coded.csv.gz")]
    c = pd.read_csv(f, sep="\t", quoting=3, keep_default_na=False, usecols=["cond", "cls_v1", "gp_v1"])
    c = c[c.cls_v1 != "AMBIG"]
    tr = lambda x: (x.cls_v1 == "TRANS").mean()
    keep = c[c.gp_v1.astype(str).isin(["0", "False", "0.0"])]
    g.append({"model": t, "vG_raw": tr(c[c.cond == "GP"]) - tr(c[c.cond == "CUE"]),
              "vG_noGPstyle": tr(keep[keep.cond == "GP"]) - tr(keep[keep.cond == "CUE"]),
              "style_gap": c[c.cond == "GP"].gp_v1.astype(float).mean() - c[c.cond == "CUE"].gp_v1.astype(float).mean()})
g = pd.DataFrame(g)
s12 = pd.read_csv(R / "E012/summary_v1.csv")
Ag = s12[s12.stat == "A_gen"].set_index("model").est
e2 = pd.read_csv(ROOT / "paper/tables/residue_sets.csv")
AL = e2[(e2.set == "E002") & (e2.stat == "A_L")].set_index("model").est
common = Ag.index.intersection(AL.index)
rho = spearmanr(Ag[common], AL[common])
out["sampled"] = {"vG_raw_pos": int((g.vG_raw > 0).sum()), "vG_noGPstyle_pos": int((g.vG_noGPstyle > 0).sum()), "n": len(g),
                  "vG_noGPstyle_median": float(g.vG_noGPstyle.median()), "vG_raw_median": float(g.vG_raw.median()),
                  "rho_vG_style": float(spearmanr(g.vG_raw, g.style_gap).statistic),
                  "rho_Agen_AL": float(rho.statistic), "rho_Agen_AL_p": float(rho.pvalue), "rho_n": len(common)}
print(g.round(3).to_string(index=False))
print("sampled", out["sampled"])
json.dump(out, open(ROOT / "paper/tables/review_checks.json", "w"), indent=1)
