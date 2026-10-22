"""Cross-model random-effects meta-analysis (DerSimonian-Laird) of per-model estimates.

Each model contributes est and a 95% interval (bootstrap or t); SE = (hi - lo) / 3.92.
Models are not independent samples of a population of LMs, so the pooled estimate is read as
"the typical model in this panel", and k_pos / k_sig are reported next to it.
"""
import numpy as np
import pandas as pd


def dl(est, lo, hi):
    y = np.asarray(est, float)
    se = (np.asarray(hi, float) - np.asarray(lo, float)) / 3.92
    ok = np.isfinite(y) & np.isfinite(se) & (se > 0)
    y, se = y[ok], se[ok]
    k = len(y)
    w = 1 / se**2
    yf = np.sum(w * y) / np.sum(w)
    Q = np.sum(w * (y - yf) ** 2)
    c = np.sum(w) - np.sum(w**2) / np.sum(w)
    tau2 = max(0.0, (Q - (k - 1)) / c) if k > 1 else 0.0
    wr = 1 / (se**2 + tau2)
    yr = np.sum(wr * y) / np.sum(wr)
    ser = np.sqrt(1 / np.sum(wr))
    I2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 else 0.0
    return {"k": k, "pooled": yr, "lo": yr - 1.96 * ser, "hi": yr + 1.96 * ser, "z": yr / ser,
            "tau": np.sqrt(tau2), "I2": I2, "k_pos": int(np.sum(y > 0)),
            "k_sig_pos": int(np.sum(y - 1.96 * se > 0)), "k_sig_neg": int(np.sum(y + 1.96 * se < 0))}


def pool(df, est="est", lo="lo", hi="hi"):
    return pd.Series(dl(df[est], df[lo], df[hi]))
