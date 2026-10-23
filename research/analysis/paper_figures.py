"""Paper figures (static PDF). Palette validated with the dataviz validator (blue/orange/aqua, light mode).

fig_residue.pdf : per-model residue A_L on three item sets (left) and free-generation A_gen (right).
fig_patching.pdf: E013 retained fraction rho on L for NP vs MC patches (left) and E013b depth (right).
"""
import re
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False,
                            "axes.edgecolor": "#777777", "axes.labelcolor": "#333333",
                            "xtick.color": "#555555", "ytick.color": "#333333", "pdf.fonttype": 42})
BLUE, ORANGE, AQUA, INK, GRID = "#2a78d6", "#eb6834", "#1baf7a", "#333333", "#e6e6e6"
ROOT = Path(__file__).resolve().parents[2]
R, T, OUT = ROOT / "results/gp", ROOT / "paper/tables", ROOT / "paper/figures"
OUT.mkdir(parents=True, exist_ok=True)

NAMES = {"gpt2": "GPT-2", "pythia-160m": "Pythia-160M", "pythia-410m-s1": "Pythia-410M", "pythia-1.4b": "Pythia-1.4B",
         "pythia-2.8b": "Pythia-2.8B", "qwen2.5-0.5b": "Qwen2.5-0.5B", "qwen3-1.7b-base": "Qwen3-1.7B",
         "gemma2-2b": "Gemma-2-2B", "qwen2.5-3b": "Qwen2.5-3B", "llama3.2-3b": "Llama-3.2-3B", "llama2-7b": "Llama-2-7B",
         "mistral-7b": "Mistral-7B", "qwen2.5-7b": "Qwen2.5-7B", "qwen2.5-7b-instruct": "Qwen2.5-7B-Inst.",
         "llama3.1-8b-instruct": "Llama-3.1-8B-Inst.", "qwen3-8b-base": "Qwen3-8B-Base", "gemma2-9b": "Gemma-2-9B",
         "gemma3-12b-it": "Gemma-3-12B-it", "qwen3-8b": "Qwen3-8B (post-tr.)", "qwen2.5-14b-instruct": "Qwen2.5-14B-Inst.", "qwen3-30b-a3b": "Qwen3-30B-A3B", "qwen2.5-32b": "Qwen2.5-32B",
         "qwen3-32b": "Qwen3-32B", "llama3.1-70b": "Llama-3.1-70B"}
ORDER = list(NAMES)  # roughly by size


def ylabels(ax, models):
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels([NAMES[m] for m in models])
    ax.set_ylim(-0.7, len(models) - 0.3)
    ax.axvline(0, color="#999999", lw=0.8, zorder=0)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)


def fig_residue():
    rs = pd.read_csv(T / "residue_sets.csv")
    rs = rs[rs.stat == "A_L"]
    g = pd.read_csv(R / "E012/summary_v1.csv")
    g = g[g.stat == "A_gen"].set_index("model")
    models = [m for m in ORDER if m in set(rs.model)]
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.3, 3.35), gridspec_kw={"width_ratios": [1.6, 1]}, sharey=True)
    for k, (s, col, lab) in enumerate((("E002", BLUE, "discovery (93 fam.)"), ("E005", ORANGE, "held-out (48 fam.)"),
                                       ("E003_christianson", AQUA, "Christianson (42 items x 4 cells)"))):
        d = rs[rs.set == s].set_index("model")
        ys = [i + (k - 1) * 0.24 for i, m in enumerate(models) if m in d.index]
        ms = [m for m in models if m in d.index]
        a.errorbar(d.loc[ms, "est"], ys, xerr=[d.loc[ms, "est"] - d.loc[ms, "lo"], d.loc[ms, "hi"] - d.loc[ms, "est"]],
                   fmt="o", ms=3, color=col, ecolor=col, elinewidth=0.9, capsize=0, label=lab)
    ylabels(a, models)
    a.set_xlabel(r"residue $A_L$ (nats)")
    a.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, fontsize=7)
    ms = [m for m in models if m in g.index]
    ys = [models.index(m) for m in ms]
    b.errorbar(g.loc[ms, "est"], ys, xerr=[g.loc[ms, "est"] - g.loc[ms, "lo"], g.loc[ms, "hi"] - g.loc[ms, "est"]],
               fmt="o", ms=3, color=BLUE, ecolor=BLUE, elinewidth=0.9)
    ylabels(b, models)
    b.set_xlabel(r"$A_{gen}$ (free generation)")
    fig.tight_layout()
    fig.savefig(OUT / "fig_residue.pdf")


def fig_patching():
    e = pd.read_csv(R / "E013/summary.csv")
    e = e[e.measure == "L"].pivot_table(index="model", columns="stat", values=["est", "lo", "hi"])
    models = [m for m in ORDER if m in e.index]
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.3, 2.0), gridspec_kw={"width_ratios": [1.3, 1]})
    for k, (st, col, lab) in enumerate((("rho_NP", BLUE, "NP states replaced"), ("rho_MC", ORANGE, "main-clause states replaced"))):
        ys = [i + (k - 0.5) * 0.3 for i in range(len(models))]
        est, lo, hi = e[("est", st)][models], e[("lo", st)][models], e[("hi", st)][models]
        a.errorbar(est, ys, xerr=[est - lo, hi - est], fmt="o", ms=3, color=col, ecolor=col, elinewidth=0.9, label=lab)
    ylabels(a, models)
    a.axvline(1, color="#999999", lw=0.8, ls=":")
    a.set_xlabel(r"retained residue $\rho = A_{patched}/A$")
    a.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=7)
    sb = pd.read_csv(R / "E013/summary_b.csv")
    sb = sb[(sb.measure == "L") & sb.run.str.endswith("__layers")]
    for (run, d), col in zip(sb.groupby("run"), (BLUE, ORANGE, AQUA)):
        d = d.set_index("stat")
        xs = [0, 0.25, 0.5, 0.75]
        ys = [d.est["rho_NP"]] + [d.est[f"rho_NPfrom{x:g}"] for x in xs[1:]]
        short = {"llama3.1-8b-instruct": "Llama-8B-I", "mistral-7b": "Mistral-7B", "qwen2.5-7b": "Qwen-7B"}
        b.plot(xs, ys, "-o", color=col, lw=2, ms=4, label=short[run.split("__")[0]])
    b.axhline(1, color="#999999", lw=0.8, ls=":")
    b.set_xticks([0, 0.25, 0.5, 0.75])
    b.set_xlabel("first patched layer / depth")
    b.set_ylabel(r"retained residue $\rho$")
    b.grid(axis="y", color=GRID, lw=0.6)
    b.set_ylim(0.0, 1.12)
    b.legend(frameon=False, fontsize=6.5, loc="lower right", handlelength=1.2)
    fig.tight_layout()
    fig.savefig(OUT / "fig_patching.pdf")


def fig_slopes():
    d = pd.read_csv(T / "item_slopes.csv")
    t = d.pivot_table(index="model", columns=["measure", "predictor"], values="t")
    models = [m for m in ORDER if m in t.index]
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 3.0), sharey=True)
    for ax, v, title in zip(axes, ("L", "S"), ("production-like $L$", "comprehension-like $S$")):
        for k, (pr, col, lab) in enumerate((("commit", BLUE, "object expectation at the verb"),
                                             ("err", ORANGE, "garden-path strength of the prime"))):
            ys = [i + (k - 0.5) * 0.3 for i in range(len(models))]
            ax.scatter(t[(v, pr)][models], ys, s=14, color=col, label=lab, zorder=3)
        ylabels(ax, models)
        for x in (-1.96, 1.96):
            ax.axvline(x, color="#bbbbbb", lw=0.6, ls=":")
        ax.set_title(title, fontsize=8, color=INK)
        ax.set_xlabel("item-level slope ($t$)")
    axes[1].tick_params(labelleft=False)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, frameon=False, loc="upper center", ncol=2, fontsize=7)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(OUT / "fig_slopes.pdf")


def fig_generation():
    g = pd.read_csv(R / "E012/summary_v1.csv").pivot_table(index="model", columns="stat", values=["est", "lo", "hi"])
    models = [m for m in ORDER if m in g.index]
    rates = {}
    for m in models:
        c = pd.read_csv(R / f"E012/{m}.coded.csv.gz", sep="\t", quoting=3, keep_default_na=False, usecols=["cond", "gp_v1"])
        rates[m] = c.groupby("cond").gp_v1.mean()
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.3, 2.05), sharey=True, gridspec_kw={"width_ratios": [1.3, 1]})
    for k, (st, col, lab) in enumerate((("A_gen", BLUE, "controlled contrast $A_{gen}$"), ("vG", ORANGE, "raw GP $-$ comma contrast"))):
        ys = [i + (k - 0.5) * 0.3 for i in range(len(models))]
        est, lo, hi = g[("est", st)][models], g[("lo", st)][models], g[("hi", st)][models]
        a.errorbar(est, ys, xerr=[est - lo, hi - est], fmt="o", ms=3, mfc=col, mec=col, ecolor=col, elinewidth=1.0, label=lab)
    ylabels(a, models)
    a.set_xlabel("difference in proportion transitive")
    a.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=7)
    for k, (cond, col, lab) in enumerate((("GP", ORANGE, "after GP prime"), ("CUE", BLUE, "after comma prime"))):
        ys = [i + (k - 0.5) * 0.3 for i in range(len(models))]
        b.scatter([rates[m][cond] for m in models], ys, s=14, color=col, label=lab, zorder=3)
    ylabels(b, models)
    b.tick_params(labelleft=False)
    b.set_xlabel("completions that are GP sentences")
    b.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "fig_generation.pdf")


if __name__ == "__main__":
    fig_patching()
    if (T / "residue_sets.csv").exists():
        fig_residue()
    fig_slopes()
    fig_generation()
    print("figures written to", OUT)
