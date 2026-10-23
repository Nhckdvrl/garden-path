"""E017 analysis (predictions frozen in README): residue of NP/S primes on NP/Z targets (E007_cross scores).

A_L = (GP - NB) - (CUE - NC); A_full = (TB - NB) - (CUE - NC); ratio = A_L / A_full, compared with the NP/Z
ratio of the same model (E002). Models whose E007_cross scores existed before the card are marked "old".
N1: A_L > 0 in the majority of new models; N2: NP/S ratio < NP/Z ratio in the majority of new models.
"""
import glob
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
from prime_analysis import bootstrap  # noqa: E402

OLD = {"gemma2-2b", "gpt2", "llama2-7b", "llama3.2-3b", "mistral-7b", "pythia-1.4b", "pythia-2.8b",
       "pythia-410m-s1", "qwen2.5-0.5b", "qwen2.5-7b", "qwen3-1.7b-base"}
C = {"A_L": {"GP": 1, "NB": -1, "CUE": -1, "NC": 1}, "A_full": {"TB": 1, "NB": -1, "CUE": -1, "NC": 1}}


def main(B=1000):
    rs = pd.read_csv(ROOT / "paper/tables/residue_sets.csv")
    e2 = rs[rs.set == "E002"].pivot_table(index="model", columns="stat", values="est")
    rows = []
    for f in sorted(glob.glob(str(ROOT / "results/gp/E007_cross/*.scores.csv.gz"))):
        t = Path(f).name[: -len(".scores.csv.gz")]
        df = pd.read_csv(f, usecols=["prime_family", "cond", "target_family", "L"])
        r = bootstrap(df, C, {"ratio": ("A_L", "A_full")}, B=B, value="L").set_index("stat")
        npz_ratio = e2.loc[t, "A_L"] / e2.loc[t, "Afull_L"] if t in e2.index else float("nan")
        rows.append({"model": t, "old": t in OLD, "A_L": r.est["A_L"], "lo": r.lo["A_L"], "hi": r.hi["A_L"],
                     "A_full": r.est["A_full"], "ratio": r.est["ratio"], "npz_ratio": npz_ratio})
        print(f"{t:22s} {'old' if t in OLD else 'NEW'} A_L={r.est['A_L']:+.3f} [{r.lo['A_L']:+.3f},{r.hi['A_L']:+.3f}] "
              f"A_full={r.est['A_full']:+.3f} ratio={r.est['ratio']:.2f} (NP/Z {npz_ratio:.2f})", flush=True)
    d = pd.DataFrame(rows)
    d.to_csv(ROOT / "results/gp/E007_cross/summary_E017.csv", index=False)
    new = d[~d.old]
    print(f"all: A_L>0 {int((d.A_L > 0).sum())}/{len(d)}, CI>0 {int((d.lo > 0).sum())}")
    print(f"N1 new A_L>0: {int((new.A_L > 0).sum())}/{len(new)} (CI>0 {int((new.lo > 0).sum())}) | "
          f"N2 new ratio<NP/Z: {int((new.ratio < new.npz_ratio).sum())}/{len(new)}")


if __name__ == "__main__":
    main()
