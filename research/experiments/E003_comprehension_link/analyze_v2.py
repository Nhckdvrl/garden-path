"""E003 v2 analysis. Family-level contrasts with bootstrap over families (comprehension) and
over prime x target families (priming). Prints per model; writes results/gp/E003/summary_v2.csv.

Comprehension score: logodds(Yes) - logodds(No), averaged over the two answer orders.
Format: 'chat' when present (instruct models), else 'plain'. Both question sets reported.
"""
import argparse
import glob
import sys
from pathlib import Path

import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=RuntimeWarning)  # empty slices / zero denominators in bootstrap

ROOT = Path(__file__).resolve().parents[3]
RES = ROOT / "results/gp/E003"
B = 1000
HUMAN_1B = {("GP", "S", "P"): 28.6, ("GP", "L", "P"): 43.7, ("GP", "S", "I"): 11.1,
            ("GP", "L", "I"): 31.4, ("CTL", "S", "P"): 10.7, ("CTL", "L", "P"): 16.3}


def fam_boot(mat, f, seed=0):
    """mat: DataFrame indexed by family; f: function(DataFrame)->float."""
    rng = np.random.default_rng(seed)
    idx = mat.index.to_numpy()
    est = f(mat)
    bs = [f(mat.loc[rng.choice(idx, len(idx))]) for _ in range(B)]
    lo, hi = np.nanpercentile(bs, [2.5, 97.5])
    return est, lo, hi


def comp_table(c):
    fmt = "chat" if (c.format == "chat").any() else "plain"
    c = c[c.format == fmt]
    g = c.groupby(["family", "verb_class", "length", "plaus", "form", "qkey"]).logodds.mean().reset_index()
    order_eff = c.pivot_table(index=["family", "length", "plaus", "form", "qkey"], columns="order", values="logodds")
    return g, fmt, float((order_eff.YN - order_eff.NY).mean())


def comp_contrasts(g, qset):
    rows = []
    for vc in ("OT", "RAT"):
        x = g[(g.verb_class == vc) & (g.qkey == f"OBS_{qset}")]
        w = x.pivot_table(index="family", columns=["form", "length", "plaus"], values="logodds")
        def C(expr):
            return lambda m: float(np.nanmean(expr(m)))
        cells = [(L, P) for L in ("S", "L") for P in (("P", "I") if vc == "OT" else ("P",))]
        defs = {}
        for L, P in cells:
            defs[f"GP-CUE_{L}{P}"] = C(lambda m, L=L, P=P: m[("GP", L, P)] - m[("CUE", L, P)])
            if vc == "OT":
                defs[f"GP-CTL_{L}{P}"] = C(lambda m, L=L, P=P: m[("GP", L, P)] - m[("CTL", L, P)])
            defs[f"CUE-REORD_{L}{P}"] = C(lambda m, L=L, P=P: m[("CUE", L, P)] - m[("REORD", L, P)])
            defs[f"GP-REORD_{L}{P}"] = C(lambda m, L=L, P=P: m[("GP", L, P)] - m[("REORD", L, P)])
            defs[f"TC-CUE_{L}{P}"] = C(lambda m, L=L, P=P: m[("TC", L, P)] - m[("CUE", L, P)])
        lin = lambda m, L, P: m[("GP", L, P)] - m[("CUE", L, P)]
        defs["linger_mean"] = C(lambda m: np.mean([lin(m, L, P) for L, P in cells], axis=0))
        defs["length_eff"] = C(lambda m: np.mean([lin(m, "L", P) - lin(m, "S", P) for P in {p for _, p in cells}], axis=0))
        if vc == "OT":
            defs["plaus_eff"] = C(lambda m: np.mean([lin(m, L, "P") - lin(m, L, "I") for L in ("S", "L")], axis=0))
        defs["comp_frac"] = lambda m: float(np.nanmean(np.mean([lin(m, L, P) for L, P in cells], axis=0)) /
                                            np.nanmean(np.mean([m[("TC", L, P)] - m[("CUE", L, P)] for L, P in cells], axis=0)))
        for k, f in defs.items():
            e, lo, hi = fam_boot(w, f)
            rows.append({"part": f"comp_OBS_{qset}", "verb_class": vc, "stat": k, "est": e, "lo": lo, "hi": hi, "n": len(w)})
        # positive control: FINAL in CUE
        y = g[(g.verb_class == vc) & (g.qkey == f"FINAL_{qset}") & (g.form == "CUE")]
        if len(y):
            rows.append({"part": f"comp_FINAL_{qset}", "verb_class": vc, "stat": "posctrl_FINAL_CUE",
                         "est": y.logodds.mean(), "lo": np.nan, "hi": np.nan, "n": y.family.nunique()})
            z = g[(g.verb_class == vc) & (g.qkey == f"FINAL_{qset}")].pivot_table(index="family", columns=["form", "length", "plaus"], values="logodds")
            e, lo, hi = fam_boot(z, lambda m: float(np.nanmean(np.mean([m[("GP", L, P)] - m[("CUE", L, P)] for L, P in cells if ("GP", L, P) in m], axis=0))))
            rows.append({"part": f"comp_FINAL_{qset}", "verb_class": vc, "stat": "final_GP-CUE", "est": e, "lo": lo, "hi": hi, "n": len(z)})
        # descriptive P(yes) per cell vs human Exp 1b
        if vc == "OT":
            for (form, L, P), h in HUMAN_1B.items():
                v = x[(x.form == form) & (x.length == L) & (x.plaus == P)].logodds
                rows.append({"part": f"human_cmp_{qset}", "verb_class": vc, "stat": f"pyes_{form}_{L}{P}",
                             "est": float((1 / (1 + np.exp(-v))).mean()), "lo": np.nan, "hi": h / 100, "n": len(v)})
    return rows


def prime_contrasts(p, value):
    rows = []
    p = p.copy()
    p["S"] = -p.lpD
    for vc in ("OT", "RAT"):
        x = p[p.verb_class == vc]
        cells = sorted({(L, P) for L, P in zip(x.length, x.plaus)})
        piv = x.pivot_table(index=["family", "target_family"], columns=["form", "length", "plaus"], values=value)
        fams = piv.index.get_level_values(0).unique().to_numpy()
        tgts = piv.index.get_level_values(1).unique().to_numpy()
        arr = {k: piv[k].unstack("target_family").reindex(index=fams, columns=tgts).to_numpy() for k in piv.columns}
        def stat(fi, ti):
            m = {k: np.nanmean(np.nanmean(a[np.ix_(fi, ti)], axis=1)) for k, a in arr.items()}
            A = {c: (m[("GP",) + c] - m[("NB",) + c]) - (m[("CUE",) + c] - m[("NC",) + c]) for c in cells}
            Af = {c: (m[("TB",) + c] - m[("NB",) + c]) - (m[("CUE",) + c] - m[("NC",) + c]) for c in cells}
            out = {f"A_{L}{P}": A[(L, P)] for L, P in cells}
            out["A_mean"] = np.mean(list(A.values()))
            out["Afull_mean"] = np.mean(list(Af.values()))
            out["rA"] = out["A_mean"] / out["Afull_mean"] if out["Afull_mean"] else np.nan
            out["A_length_eff"] = np.mean([A[("L", P)] - A[("S", P)] for P in {P for _, P in cells}])
            if vc == "OT":
                out["A_plaus_eff"] = np.mean([A[(L, "P")] - A[(L, "I")] for L in ("S", "L")])
                out["GP-CTL_mean"] = np.mean([m[("GP",) + c] - m[("CTL",) + c] for c in cells])
            out["GP-TB_mean"] = np.mean([m[("GP",) + c] - m[("TB",) + c] for c in cells])
            return out
        rng = np.random.default_rng(0)
        full = stat(np.arange(len(fams)), np.arange(len(tgts)))
        bs = pd.DataFrame([stat(rng.integers(0, len(fams), len(fams)), rng.integers(0, len(tgts), len(tgts))) for _ in range(B)])
        for k, v in full.items():
            lo, hi = np.nanpercentile(bs[k], [2.5, 97.5])
            rows.append({"part": f"prime_{value}", "verb_class": vc, "stat": k, "est": v, "lo": lo, "hi": hi, "n": len(fams)})
    return rows


def strength(q):
    w = q.pivot_table(index=["family", "verb_class", "length", "plaus"], columns="probe", values="lp").reset_index()
    w["gp_eff"] = w.CUE_dis - w.GP_dis
    rows = []
    for (vc, L, P), d in w.groupby(["verb_class", "length", "plaus"]):
        rows.append({"part": "strength", "verb_class": vc, "stat": f"gp_eff_{L}{P}", "est": d.gp_eff.mean(),
                     "lo": np.nan, "hi": np.nan, "n": len(d)})
    return rows


def cell_level(p, q, g):
    """Within-family slopes across the length x plausibility cells (OT only).

    Per (family, cell): A on S (averaged over targets), comprehension lingering (GP-CUE on
    OBS_author), garden-path strength gp_eff = lp CUE_dis - lp GP_dis. Family-demeaned
    regressions: slope of A and of lingering on gp_eff. Family bootstrap.
    Motivated by the parallel session's two-force account (commitment raises priming;
    disambiguation error lowers it): E003's L/P manipulations vary gp_eff within family.
    """
    p = p[p.verb_class == "OT"].copy()
    p["S"] = -p.lpD
    m = p.groupby(["family", "length", "plaus", "form"]).S.mean().unstack("form")
    A = ((m.GP - m.NB) - (m.CUE - m.NC)).rename("A")
    x = g[(g.verb_class == "OT") & (g.qkey == "OBS_author")].pivot_table(
        index=["family", "length", "plaus"], columns="form", values="logodds")
    lin = (x.GP - x.CUE).rename("linger")
    w = q[q.verb_class == "OT"].pivot_table(index=["family", "length", "plaus"], columns="probe", values="lp")
    ge = (w.CUE_dis - w.GP_dis).rename("gp_eff")
    # commitment over the NP: log P(clause close) at the end of the ambiguous region, i.e.
    # log(P(",") + P(".")) minus log P(disambiguating word) is NOT used (it contains gp_eff);
    # we use the closure mass itself.
    ce = np.logaddexp(w.NPend_comma, w.NPend_period).rename("commit_end")
    d = pd.concat([A, lin, ge, ce], axis=1).dropna().reset_index()
    for k in ("A", "linger", "gp_eff", "commit_end"):
        d[k + "_w"] = d[k] - d.groupby("family")[k].transform("mean")

    def slope(dd, y):
        v = (dd.gp_eff_w ** 2).sum()
        return float((dd.gp_eff_w * dd[y + "_w"]).sum() / v) if v else np.nan

    def slopes2(dd, y):
        X = dd[["gp_eff_w", "commit_end_w"]].to_numpy()
        try:
            return np.linalg.lstsq(X, dd[y + "_w"].to_numpy(), rcond=None)[0]
        except np.linalg.LinAlgError:
            return np.array([np.nan, np.nan])

    fams = d.family.unique()
    rng = np.random.default_rng(0)
    rows = []
    for y in ("A", "linger"):
        est = slopes2(d, y)
        bs = np.array([slopes2(pd.concat([d[d.family == f] for f in rng.choice(fams, len(fams))]), y) for _ in range(300)])
        for k, name in enumerate(("gp_eff", "commit_end")):
            lo, hi = np.nanpercentile(bs[:, k], [2.5, 97.5])
            rows.append({"part": "cell_level", "verb_class": "OT", "stat": f"partial_{y}_on_{name}", "est": float(est[k]),
                         "lo": lo, "hi": hi, "n": len(fams)})
    # prefix-matched: within (family, length) only plausibility varies; the prefix (V + NP region)
    # is identical, so commitment over the NP is constant and gp_eff varies through the continuation.
    dl = d.copy()
    for k in ("A", "linger", "gp_eff"):
        dl[k + "_w"] = dl[k] - dl.groupby(["family", "length"])[k].transform("mean")
    for y in ("A", "linger"):
        est = slope(dl, y)
        bs = [slope(pd.concat([dl[dl.family == f] for f in rng.choice(fams, len(fams))]), y) for _ in range(300)]
        lo, hi = np.nanpercentile(bs, [2.5, 97.5])
        rows.append({"part": "cell_level", "verb_class": "OT", "stat": f"prefixmatched_{y}_on_gp_eff", "est": est,
                     "lo": lo, "hi": hi, "n": len(fams)})
    for y in ("A", "linger"):
        est = slope(d, y)
        bs = [slope(pd.concat([d[d.family == f] for f in rng.choice(fams, len(fams))]), y) for _ in range(300)]
        lo, hi = np.nanpercentile(bs, [2.5, 97.5])
        rows.append({"part": "cell_level", "verb_class": "OT", "stat": f"slope_{y}_on_gp_eff", "est": est,
                     "lo": lo, "hi": hi, "n": len(fams)})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tags", nargs="*")
    a = ap.parse_args()
    tags = a.tags or sorted(Path(p).name[: -len(".meta.json")] for p in glob.glob(str(RES / "*.meta.json")))
    allrows = []
    for t in tags:
        rows = []
        g, fmt, oe = comp_table(pd.read_csv(RES / f"{t}.comp.csv"))
        for qs in ("author", "template"):
            rows += comp_contrasts(g, qs)
        p = pd.read_csv(RES / f"{t}.prime.csv.gz")
        for v in ("S", "L"):
            rows += prime_contrasts(p, v)
        q = pd.read_csv(RES / f"{t}.probes.csv")
        rows += strength(q)
        rows += cell_level(p, q, g)
        df = pd.DataFrame(rows)
        df.insert(0, "model", t)
        df["format"] = fmt
        df["order_effect_YN_minus_NY"] = oe
        allrows.append(df)
        s = df.set_index(["part", "verb_class", "stat"])
        f = lambda k: f"{s.loc[k].est:+.2f}[{s.loc[k].lo:+.2f},{s.loc[k].hi:+.2f}]"
        print(f"== {t} ({fmt}; order eff {oe:+.2f})")
        print("  comp OT:  linger", f(("comp_OBS_author", "OT", "linger_mean")), "length", f(("comp_OBS_author", "OT", "length_eff")),
              "plaus", f(("comp_OBS_author", "OT", "plaus_eff")), "frac", f(("comp_OBS_author", "OT", "comp_frac")))
        print("  prime OT: A", f(("prime_S", "OT", "A_mean")), "rA", f(("prime_S", "OT", "rA")), "length", f(("prime_S", "OT", "A_length_eff")),
              "plaus", f(("prime_S", "OT", "A_plaus_eff")), "GP-CTL", f(("prime_S", "OT", "GP-CTL_mean")))
        print("  RAT comp: GP-REORD_LP", f(("comp_OBS_author", "RAT", "GP-REORD_LP")), "CUE-REORD_LP", f(("comp_OBS_author", "RAT", "CUE-REORD_LP")),
              "| OT GP-REORD_LP", f(("comp_OBS_author", "OT", "GP-REORD_LP")))
        print("  within-family slopes on gp_eff: A", f(("cell_level", "OT", "slope_A_on_gp_eff")),
              "linger", f(("cell_level", "OT", "slope_linger_on_gp_eff")))
        print("  PREFIX-MATCHED slopes on gp_eff: A", f(("cell_level", "OT", "prefixmatched_A_on_gp_eff")),
              "linger", f(("cell_level", "OT", "prefixmatched_linger_on_gp_eff")))
        print("  partial (gp_eff | commit_end): A", f(("cell_level", "OT", "partial_A_on_gp_eff")), f(("cell_level", "OT", "partial_A_on_commit_end")),
              "linger", f(("cell_level", "OT", "partial_linger_on_gp_eff")), f(("cell_level", "OT", "partial_linger_on_commit_end")))
    pd.concat(allrows).to_csv(RES / "summary_v2.csv", index=False)


if __name__ == "__main__":
    main()
