"""E006: within-family slope of A_k on disambiguation surprisal err_k (family FE, clustered SE)."""
import glob
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[3]
RES = ROOT / "results/gp/E006"
VAR = pd.read_json(ROOT / "data/gp_behavior/derived/e006_variants_v1.jsonl", lines=True)


def table(tag):
    s = pd.read_csv(RES / f"{tag}.scores.csv.gz")
    s["S"] = -s.lpD
    s[["c", "k"]] = s.cond.str.split("#", expand=True)
    m = s.groupby(["prime_family", "k", "c"]).S.mean().unstack("c")
    d = pd.DataFrame({"A": m.GP - m.NB - m.CUE + m.NC}).reset_index()
    p = pd.read_csv(RES / f"{tag}.probes.csv")
    p[["probe_name", "k"]] = p.probe.str.split("#", expand=True)
    pp = p.pivot_table(index=["family", "k"], columns="probe_name", values="lp").reset_index()
    pp["err"] = pp.CUE_dis - pp.GP_dis
    pp["err_cont"] = pp.CUE_cont - pp.GP_cont
    d = d.merge(pp[["family", "k", "err", "err_cont"]], left_on=["prime_family", "k"], right_on=["family", "k"])
    d["k"] = d.k.astype(int)
    d = d.merge(VAR[["family_id", "variant", "is_original", "naturalness_llama31_8b"]],
                left_on=["prime_family", "k"], right_on=["family_id", "variant"])
    return d


def within(d, x):
    d = d.copy()
    for c in ("A", x):
        d[c + "_w"] = d[c] - d.groupby("prime_family")[c].transform("mean")
    sd = d[x + "_w"].std()
    d["xz"] = d[x + "_w"] / sd
    f = smf.ols("A_w ~ xz", d).fit(cov_type="cluster", cov_kwds={"groups": d.prime_family.astype("category").cat.codes})
    return f.params.xz, f.bse.xz, f.tvalues.xz, sd


def main():
    tags = sorted(Path(p).name[: -len(".scores.csv.gz")] for p in glob.glob(str(RES / "*.scores.csv.gz")))
    rows = []
    for t in tags:
        d = table(t)
        for x in ("err", "err_cont"):
            b, se, tv, sd = within(d, x)
            rows.append({"model": t, "x": x, "b_per_withinSD": b, "se": se, "t": tv, "within_sd": sd,
                         "n_fam": d.prime_family.nunique(), "n_var": len(d)})
        # robustness: generated-only variants, and naturalness-adjusted
        b2, _, t2, _ = within(d[~d.is_original], "err")
        dd = d.copy()
        for c in ("A", "err", "naturalness_llama31_8b"):
            dd[c + "_w"] = dd[c] - dd.groupby("prime_family")[c].transform("mean")
        f = smf.ols("A_w ~ err_w + naturalness_llama31_8b_w", dd).fit(
            cov_type="cluster", cov_kwds={"groups": dd.prime_family.astype("category").cat.codes})
        print(f"{t:18s} within-family slope A~err: b={rows[-2]['b_per_withinSD']:+.3f} t={rows[-2]['t']:+.2f} | "
              f"A~err_cont: b={rows[-1]['b_per_withinSD']:+.3f} t={rows[-1]['t']:+.2f} | generated-only t={t2:+.2f} | "
              f"+naturalness ctrl t_err={f.tvalues.err_w:+.2f} (within SD err={rows[-2]['within_sd']:.2f}, {len(d)} variants)")
    pd.DataFrame(rows).to_csv(RES / "summary.csv", index=False)


if __name__ == "__main__":
    main()
