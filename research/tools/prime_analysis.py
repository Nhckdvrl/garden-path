"""Family-level priming contrasts with two-way (prime family x target family) bootstrap.

Contrasts are linear combinations of condition means, written as dicts
{cond: weight}. Ratios are given as (numerator_contrast, denominator_contrast).
"""
import numpy as np
import pandas as pd


def load_arrays(df, value="L"):
    P = np.array(sorted(df.prime_family.unique()))
    T = np.array(sorted(df.target_family.unique()))
    piv = df.pivot_table(index=["prime_family", "target_family"], columns="cond", values=value)
    arr = {c: piv[c].unstack("target_family").reindex(index=P, columns=T).to_numpy() for c in piv.columns}
    return P, T, arr


def evaluate(arr, pi, ti, contrasts, ratios):
    m = {c: np.nanmean(np.nanmean(a[np.ix_(pi, ti)], axis=1)) for c, a in arr.items()}
    out = {}
    for name, w in contrasts.items():
        out[name] = sum(m[c] * x for c, x in w.items())
    for name, (num, den) in ratios.items():
        out[name] = out[num] / out[den] if out[den] != 0 else np.nan
    return out


def bootstrap(df, contrasts, ratios=None, B=1000, seed=0, value="L"):
    ratios = ratios or {}
    P, T, arr = load_arrays(df, value)
    rng = np.random.default_rng(seed)
    full = evaluate(arr, np.arange(len(P)), np.arange(len(T)), contrasts, ratios)
    bs = pd.DataFrame([evaluate(arr, rng.integers(0, len(P), len(P)), rng.integers(0, len(T), len(T)),
                                contrasts, ratios) for _ in range(B)])
    rows = []
    for k, v in full.items():
        lo, hi = np.nanpercentile(bs[k], [2.5, 97.5])
        rows.append({"stat": k, "est": v, "lo": lo, "hi": hi, "n_prime": len(P), "n_target": len(T)})
    return pd.DataFrame(rows)


def fmt(r, k):
    w = r.set_index("stat")
    return f"{w.est[k]:+.3f} [{w.lo[k]:+.3f},{w.hi[k]:+.3f}]"
