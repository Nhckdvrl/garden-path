"""E016 analysis (predictions frozen in README).

rho_cell = A_L(cell) / A_L(none), with A = (GP|cell - NB|cell) - (CUE - NC); D_cell = A_S(cell) - A_S(none).
Probes: best CV accuracy, first layer with accuracy >= .9, mean P(object) of NB and PASS NP states over the
middle half of the layers (L/4..3L/4, the layers edited in the role intervention).
P1 rho_SAME >= .8 (majority) and rho_SAME > rho_CUE-donor (E013) in every model; P2 rho_NBD <= .6 (majority);
P3 best acc >= .9 in every model and NB mean P(object) < .5 in the majority; P4 rho_ROLE <= .7 (majority) and
rho_ROLE < mean rho_RAND in every model; P5 PASS P(object) vs E011 ratio (exploratory).
"""
import glob
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
from prime_analysis import bootstrap, fmt  # noqa: E402

RES = ROOT / "results/gp/E016"
CELLS = ["none", "SAME", "NBD", "ROLE", "RAND0", "RAND1", "RAND2"]


def main(B=1000):
    e13 = pd.read_csv(ROOT / "results/gp/E013/summary.csv")
    e11 = pd.read_csv(ROOT / "results/gp/E011/summary.csv")
    e11 = e11[(e11.subset == "all") & (e11.measure == "L")].set_index("model").ratio
    rows, summ = [], []
    for f in sorted(glob.glob(str(RES / "*.scores.csv.gz"))):
        t = Path(f).name[: -len(".scores.csv.gz")]
        df = pd.read_csv(f)
        df["S"] = -df.lpD
        cells = [c for c in CELLS if f"GP|{c}" in set(df.cond)]
        C = {f"A_{c}": {f"GP|{c}": 1, f"NB|{c}": -1, "CUE": -1, "NC": 1} for c in cells}
        R = {f"rho_{c}": (f"A_{c}", "A_none") for c in cells if c != "none"}
        out = {}
        for v in ("L", "S"):
            r = bootstrap(df, C, R, B=B, value=v)
            r.insert(0, "measure", v)
            r.insert(0, "model", t)
            rows.append(r)
            out[v] = r.set_index("stat")
        L, S = out["L"], out["S"]
        pr = pd.read_csv(RES / f"{t}.probe.csv")
        nL = len(pr)
        mid = pr.iloc[nL // 4: (3 * nL) // 4]
        first90 = int(pr[pr.cv_acc >= 0.9].layer.min()) if (pr.cv_acc >= 0.9).any() else -1
        cue = e13[(e13.model == t) & (e13.measure == "L") & (e13.stat == "rho_NP")]
        s = {"model": t, "rho_SAME": L.est.get("rho_SAME"), "rho_SAME_lo": L.lo.get("rho_SAME"),
             "rho_NBD": L.est.get("rho_NBD"), "rho_ROLE": L.est.get("rho_ROLE"), "rho_ROLE_lo": L.lo.get("rho_ROLE"),
             "rho_ROLE_hi": L.hi.get("rho_ROLE"),
             "rho_RAND": np.mean([L.est.get(f"rho_RAND{k}") for k in range(3)]),
             "rho_CUE_E013": float(cue.est.iloc[0]) if len(cue) else np.nan,
             "dS_ROLE": S.est.get("A_ROLE") - S.est.get("A_none"),
             "dS_RAND": np.mean([S.est.get(f"A_RAND{k}") for k in range(3)]) - S.est.get("A_none"),
             "probe_best": pr.cv_acc.max(), "probe_first90_layer": first90, "n_layers": nL,
             "pobj_NB_mid": mid.p_obj_NB.mean(), "pobj_PASS_mid": mid.p_obj_PASS.mean(),
             "e011_ratio": e11.get(t, np.nan)}
        summ.append(s)
        print(f"{t:22s} L: rho SAME={fmt(L,'rho_SAME')} NBD={fmt(L,'rho_NBD')} ROLE={fmt(L,'rho_ROLE')} RAND={s['rho_RAND']:.2f} "
              f"(E013 CUE donor {s['rho_CUE_E013']:.2f}) | S: dROLE={s['dS_ROLE']:+.2f} dRAND={s['dS_RAND']:+.2f} | "
              f"probe best={s['probe_best']:.2f} first>=.9 at {first90}/{nL} P(obj) NB={s['pobj_NB_mid']:.2f} PASS={s['pobj_PASS_mid']:.2f}",
              flush=True)
    pd.concat(rows).to_csv(RES / "summary.csv", index=False)
    d = pd.DataFrame(summ)
    d.to_csv(RES / "summary_models.csv", index=False)
    n = len(d)
    print(f"P1 rho_SAME>=.8: {(d.rho_SAME >= .8).sum()}/{n}; SAME>CUE-donor: {(d.rho_SAME > d.rho_CUE_E013).sum()}/{n}")
    print(f"P2 rho_NBD<=.6: {(d.rho_NBD <= .6).sum()}/{n}")
    print(f"P3 best acc>=.9: {(d.probe_best >= .9).sum()}/{n}; NB P(obj)<.5: {(d.pobj_NB_mid < .5).sum()}/{n}")
    print(f"P4 rho_ROLE<=.7: {(d.rho_ROLE <= .7).sum()}/{n}; ROLE<RAND: {(d.rho_ROLE < d.rho_RAND).sum()}/{n}")
    ok = d.dropna(subset=["e011_ratio"])
    if len(ok) >= 4:
        r = spearmanr(ok.pobj_PASS_mid, ok.e011_ratio)
        print(f"P5 (exploratory) PASS P(obj) vs E011 ratio: rho={r.statistic:.2f} p={r.pvalue:.3f} (n={len(ok)})")


if __name__ == "__main__":
    main()
