"""Cross-model summaries for the paper (random-effects meta-analysis over models; see research/tools/meta.py).

Reads the committed per-experiment summaries and writes
  paper/tables/pooled.csv     one row per headline statistic
  paper/tables/models.csv     which models enter which experiment
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research/tools"))
from meta import dl  # noqa: E402

R = ROOT / "results/gp"
OUT = ROOT / "paper/tables"
OUT.mkdir(parents=True, exist_ok=True)

rows, use = [], {}


def add(exp, stat, d, est="est", lo="lo", hi="hi", note=""):
    res = dl(d[est], d[lo], d[hi])
    rows.append({"exp": exp, "stat": stat, **res, "note": note})
    use.setdefault(exp, set()).update(d["model"] if "model" in d else [])


e2 = pd.read_csv(R / "E002/summary.csv")
for m in ("L", "S"):
    add("E002", f"A_{m}", e2[(e2.measure == m) & (e2.stat == "A_objanalysis")])
add("E002", "rA_L", e2[(e2.measure == "L") & (e2.stat == "rA")], note="residue / full transitive prime")
add("E002", "NB-NC_S", e2[(e2.measure == "S") & (e2.stat == "NB-NC")], note="comma-omission adaptation")

e5 = pd.read_csv(R / "E005/heldout_estimates.csv")
add("E005", "A_S_heldout", e5[~e5.exclude_overlap], est="A", lo="A_lo", hi="A_hi")

e9 = pd.read_csv(R / "E009/summary.csv")
add("E009", "A_case_S", e9, est="A_case")
t9 = {"k": len(e9), "k_obj_pos": int((e9.t_obj > 0).sum()), "k_obj_sig": int((e9.t_obj > 1.645).sum()),
      "k_gp_neg": int((e9.t_gp < 0).sum()), "k_gp_sig": int((e9.t_gp < -1.645).sum())}

e11 = pd.read_csv(R / "E011/summary.csv")
d11 = e11[(e11.subset == "all") & (e11.measure == "L")]
add("E011", "A_pass_L", d11, est="A_pass", lo="A_pass_lo", hi="A_pass_hi",
    note=f"median A_pass/A_GP = {d11.ratio.median():.2f}")

e12 = pd.read_csv(R / "E012/summary_v1.csv")
for st in ("A_gen", "vG", "style_GP-CUE"):
    add("E012", st, e12[e12.stat == st])

e13 = pd.read_csv(R / "E013/summary.csv")
for m, st in (("L", "rho_NP"), ("L", "rho_MC"), ("S", "D_NP"), ("S", "D_MC")):
    add("E013", f"{st}_{m}", e13[(e13.measure == m) & (e13.stat == st)])

e14 = pd.read_csv(R / "E014/summary.csv")
for m in ("L", "S"):
    d = e14.assign(est=e14[f"dA_{m}(OBJ-INT)"], lo=e14[f"dA_{m}(OBJ-INT)"] - 1.96 * e14[f"dA_{m}_se"],
                   hi=e14[f"dA_{m}(OBJ-INT)"] + 1.96 * e14[f"dA_{m}_se"])
    add("E014", f"dA_{m}(OBJ-INT)", d, note="post-hoc")

p = pd.DataFrame(rows)
p.to_csv(OUT / "pooled.csv", index=False)
pd.set_option("display.width", 200)
print(p[["exp", "stat", "k", "pooled", "lo", "hi", "I2", "k_pos", "k_sig_pos", "k_sig_neg", "note"]].round(3).to_string(index=False))
print("E009 item slopes:", t9)

allm = sorted(set().union(*use.values()))
pd.DataFrame([{"model": m, **{e: int(m in s) for e, s in use.items()}} for m in allm]).to_csv(OUT / "models.csv", index=False)
print(len(allm), "models")
