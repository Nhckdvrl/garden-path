"""E005: derive per-model predictions from discovery (E002/E004) with the frozen rule, then
test them on held-out families. Usage: python analyze.py [--B 1000]
Writes results/gp/E005/predictions.json (discovery side) and results/gp/E005/confirmation.csv.
"""
import argparse
import glob
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import binomtest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
from prime_analysis import bootstrap  # noqa: E402

E2, E4, E5 = (ROOT / f"results/gp/{e}" for e in ("E002", "E004", "E005"))
CON = {
    "A": {"GP": 1, "NB": -1, "CUE": -1, "NC": 1},
    "Afull": {"TB": 1, "NB": -1, "CUE": -1, "NC": 1},
    "dA": {"GP>GP": 1, "NB>NB": -1, "CUE>CUE": -1, "NC>NC": 1, "GP": -1, "NB": 1, "CUE": 1, "NC": -1},
    "dAfull": {"TB>TB": 1, "NB>NB": -1, "CUE>CUE": -1, "NC>NC": 1, "TB": -1, "NB": 1, "CUE": 1, "NC": -1},
}
RAT = {"rA1": ("A", "Afull"), "r_inc": ("dA", "dAfull")}


def family_table(scores, probes):
    m = scores.assign(S=-scores.lpD).pivot_table(index="prime_family", columns="cond", values="S")
    p = probes.pivot_table(index="family", columns="probe", values="lp")
    d = pd.DataFrame({"A": m.GP - m.NB - m.CUE + m.NC})
    d["obj_expect"] = p.V_the - p.V_comma
    d["gp_strength"] = p.CUE_dis - p.GP_dis
    return d.dropna()


def regress(d):
    z = lambda x: (x - x.mean()) / x.std()
    f = smf.ols("A ~ zo + zg", d.assign(zo=z(d.obj_expect), zg=z(d.gp_strength))).fit()
    return {"b_obj": f.params.zo, "t_obj": f.tvalues.zo, "p_obj": f.pvalues.zo,
            "b_gp": f.params.zg, "t_gp": f.tvalues.zg, "p_gp": f.pvalues.zg, "n": int(f.nobs)}


def load(exp_dir, tag):
    s = pd.read_csv(exp_dir / f"{tag}.scores.csv.gz")
    p = pd.read_csv(exp_dir / f"{tag}.probes.csv")
    return s, p


def predictions(tag, B):
    s2, p2 = load(E2, tag)
    reg = regress(family_table(s2, p2))
    df = s2.assign(S=-s2.lpD)
    if (E4 / f"{tag}.meta.json").exists():
        s4 = pd.read_csv(E4 / f"{tag}.scores.csv.gz")
        df = pd.concat([df, s4[s4.cond != "CUE>CUE"].assign(S=-s4.lpD)])
    have4 = "GP>GP" in set(df.cond)
    con = CON if have4 else {k: CON[k] for k in ("A", "Afull")}
    rat = RAT if have4 else {"rA1": RAT["rA1"]}
    b = bootstrap(df, con, rat, B=B, value="S").set_index("stat")
    pr = {"discovery": {**reg, "A": b.est.A, "A_lo": b.lo.A, "A_hi": b.hi.A}}
    pr["P1_obj_pos"] = bool(reg["t_obj"] >= 2)
    pr["P2_gp_sign"] = -1 if reg["t_gp"] <= -2 else (1 if reg["t_gp"] >= 2 else 0)
    pr["P3_A_sign"] = 1 if b.lo.A > 0 else (-1 if b.hi.A < 0 else 0)
    pr["P4_history"] = bool(have4 and pr["P3_A_sign"] == 1)
    return pr


def confirm(tag, pr, B, exclude_overlap=False):
    s5, p5 = load(E5, tag)
    if exclude_overlap:
        fams = [json.loads(l) for l in open(ROOT / "data/gp_behavior/derived/npz_heldout_v1.jsonl")]
        keep = {f["family_id"] for f in fams if not f["verb_overlap_with_discovery"]}
        s5, p5 = s5[s5.prime_family.isin(keep)], p5[p5.family.isin(keep)]
    reg = regress(family_table(s5, p5))
    b = bootstrap(s5.assign(S=-s5.lpD), CON, RAT, B=B, value="S").set_index("stat")
    rows = []
    if pr["P1_obj_pos"]:
        rows.append(("P1_obj_pos", reg["b_obj"], reg["t_obj"], reg["t_obj"] > 1.645))
    if pr["P2_gp_sign"]:
        rows.append(("P2_gp_sign", reg["b_gp"], reg["t_gp"], pr["P2_gp_sign"] * reg["t_gp"] > 1.645))
    if pr["P3_A_sign"]:
        ok = (b.lo.A > 0) if pr["P3_A_sign"] > 0 else (b.hi.A < 0)
        # one-sided 95%: use 90% two-sided interval equivalent via bootstrap percentiles is not stored;
        # conservative: require the 95% two-sided CI to exclude 0 in the predicted direction.
        rows.append(("P3_A_sign", b.est.A, np.nan, bool(ok)))
    if pr["P4_history"]:
        rows.append(("P4_history", b.est.r_inc - b.est.rA1, np.nan, bool(b.est.r_inc < b.est.rA1)))
    out = pd.DataFrame(rows, columns=["prediction", "estimate", "t", "confirmed"])
    out.insert(0, "model", tag)
    extra = {"A": b.est.A, "A_lo": b.lo.A, "A_hi": b.hi.A, "rA1": b.est.rA1, "r_inc": b.est.r_inc,
             "dA": b.est.dA, "dAfull": b.est.dAfull, **{f"heldout_{k}": v for k, v in reg.items()}}
    return out, extra


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=1000)
    ap.add_argument("--predict_only", action="store_true")
    a = ap.parse_args()
    E5.mkdir(parents=True, exist_ok=True)
    pfile = E5 / "predictions.json"
    preds = json.load(open(pfile)) if pfile.exists() else {}
    tags = sorted(Path(p).name[: -len(".meta.json")] for p in glob.glob(str(E2 / "*.meta.json")))
    for t in tags:
        if t not in preds:  # predictions are written once and never overwritten
            preds[t] = predictions(t, a.B)
            print(f"[predict] {t}: {json.dumps({k: v for k, v in preds[t].items() if k != 'discovery'})}")
    json.dump(preds, open(pfile, "w"), indent=1, default=float)
    if a.predict_only:
        return
    allr, ext = [], []
    for t in sorted(Path(p).name[: -len(".meta.json")] for p in glob.glob(str(E5 / "*.meta.json"))):
        if t not in preds:
            print(f"{t}: no discovery predictions, reported descriptively only")
            continue
        for excl in (False, True):
            r, e = confirm(t, preds[t], a.B, excl)
            r.insert(1, "exclude_overlap", excl)
            allr.append(r)
            ext.append({"model": t, "exclude_overlap": excl, **e})
    if not allr:
        return
    R = pd.concat(allr)
    R.to_csv(E5 / "confirmation.csv", index=False)
    pd.DataFrame(ext).to_csv(E5 / "heldout_estimates.csv", index=False)
    print(R[~R.exclude_overlap].to_string(index=False))
    for p, g in R[~R.exclude_overlap].groupby("prediction"):
        k, n = int(g.confirmed.sum()), len(g)
        print(f"{p}: {k}/{n} confirmed; sign test p={binomtest(int((np.sign(g.estimate) == np.sign(g.estimate.mean())).sum()), n, 0.5, alternative='greater').pvalue:.4f}")


if __name__ == "__main__":
    main()
