"""E011 analysis: A_pass vs A_GP on L (primary) and S, all families and plausible half."""
import glob, json, sys
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
from prime_analysis import bootstrap  # noqa: E402
E2, E11 = ROOT / "results/gp/E002", ROOT / "results/gp/E011"
C = {"A_GP": {"GP": 1, "NB": -1, "CUE": -1, "NC": 1}, "A_pass": {"PASS_B": 1, "PASS_C": -1, "NB": -1, "NC": 1}}
R = {"ratio": ("A_pass", "A_GP")}
nat = json.load(open(E11 / "passive_naturalness.json")) if (E11 / "passive_naturalness.json").exists() else {}
rows = []
for f in sorted(glob.glob(str(E11 / "*.meta.json"))):
    t = Path(f).name[: -len(".meta.json")]
    d11 = pd.read_csv(E11 / f"{t}.scores.csv.gz")
    d2 = pd.read_csv(E2 / f"{t}.scores.csv.gz")
    fams = set(d11.prime_family)
    d = pd.concat([d11, d2[d2.cond.isin(["GP", "CUE", "NB", "NC"]) & d2.prime_family.isin(fams)]])
    d["S"] = -d.lpD
    p = pd.read_csv(E11 / f"{t}.probes.csv").pivot_table(index="family", columns="probe", values="lp")
    p2 = pd.read_csv(E2 / f"{t}.probes.csv").pivot_table(index="family", columns="probe", values="lp")
    pas_eff = float((p.PC_dis - p.PB_dis).mean()); gp_eff = float((p2.CUE_dis - p2.GP_dis).loc[list(fams)].mean())
    subsets = {"all": fams}
    if nat:
        med = np.median([nat[x] for x in fams])
        subsets["plausible"] = {x for x in fams if nat[x] >= med}
    for sub, fs in subsets.items():
        for meas in ("L", "S"):
            b = bootstrap(d[d.prime_family.isin(fs)], C, R, B=500, value=meas).set_index("stat")
            rows.append({"model": t, "subset": sub, "measure": meas, "A_GP": b.est.A_GP, "A_pass": b.est.A_pass,
                         "A_pass_lo": b.lo.A_pass, "A_pass_hi": b.hi.A_pass, "ratio": b.est.ratio,
                         "gp_dis_effect": gp_eff, "pass_dis_effect": pas_eff, "n_fam": len(fs)})
r = pd.DataFrame(rows); r.to_csv(E11 / "summary.csv", index=False)
print(r.round(2).to_string(index=False))
for sub in r.subset.unique():
    x = r[(r.subset == sub) & (r.measure == "L")]
    pos = int((x.A_pass_lo > 0).sum())
    print(f"[{sub}] L: median ratio={x.ratio.median():.2f}; A_pass CI>0 in {pos}/{len(x)}; "
          f"P-CONF={'YES' if x.ratio.median() >= .5 and pos > len(x)/2 else 'no'}  "
          f"P-ANAL={'YES' if x.ratio.median() < .25 and (x.A_pass_lo <= 0).sum() > len(x)/2 else 'no'}")
