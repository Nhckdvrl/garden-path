"""E016: patching controls, role probes and a role-direction intervention (see README).

Per model writes results/gp/E016/<tag>.scores.csv.gz (same columns as E013; cond = CUE, NC, GP|cell, NB|cell)
and <tag>.probe.csv (per layer: CV accuracy, mean P(object) for NB and PASS NP states).
Cells: none, SAME (same-analysis donor, NP span), NBD (NB donor, NP span), ROLE (role direction set to the
subject mean at NP tokens, layers L/4..3L/4, full intervened cache), RAND0-2 (norm-matched random directions).
Usage: python run.py --models tag=path [--dtype float32|bfloat16] [--limit N]
"""
import argparse
import gzip
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from sklearn.linear_model import LogisticRegression

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
sys.path.insert(0, str(ROOT / "research/experiments/E013_stale_states"))
import lmscore  # noqa: E402
from run import FAMS, INTR, enc_prime, layers_of, mix, run_prefix, score_tails, targets_for  # noqa: E402

OUT = ROOT / "results/gp/E016"
PASS = {json.loads(l)["family_id"]: json.loads(l)["prime"]
        for l in open(ROOT / "research/experiments/E011_local_coherence/spec.jsonl") if '"PASS_B"' in l}
NEUTRAL = "It was a quiet morning. "


@torch.no_grad()
def run_hooked(model, ids, edit=None):
    """Forward with an optional per-layer edit(li, h) applied in place to each layer's output."""
    hooks = []
    for li, layer in enumerate(layers_of(model)):
        def hook(mod, inp, out, li=li):
            h = out[0] if isinstance(out, tuple) else out
            if edit is not None:
                edit(li, h)
            return out
        hooks.append(layer.register_forward_hook(hook))
    try:
        o = model(input_ids=torch.tensor([ids], device=model.device), use_cache=True)
    finally:
        for h in hooks:
            h.remove()
    pkv = o.past_key_values
    kv = [(k.clone(), v.clone()) for k, v in (pkv.to_legacy_cache() if hasattr(pkv, "to_legacy_cache") else pkv)]
    return kv, F.log_softmax(o.logits[0, -1].float(), -1).cpu()


def np_states(model, tok, text, np_str):
    ids, npp, _ = enc_prime(tok, text, np_str)
    _, hs, _ = run_prefix(model, ids)
    return torch.stack([h[npp[-1]].float().cpu() for h in hs])  # [L, d] at the NP's last token


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--dtype", default="float32")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--bs", type=int, default=256)
    # E016b: comma-matched probe/direction (object TB vs subject NB, both without a comma), only the
    # direction cells, written with a suffix
    ap.add_argument("--obj", default="TB,TC")
    ap.add_argument("--subj", default="CUE,NC")
    ap.add_argument("--cells", default="SAME,NBD,ROLE,RAND")
    ap.add_argument("--suffix", default="")
    a = ap.parse_args()
    OBJ, SUBJ, CELLS_ON = a.obj.split(","), a.subj.split(","), set(a.cells.split(","))
    OUT.mkdir(parents=True, exist_ok=True)
    fams = {json.loads(l)["family_id"]: json.loads(l) for l in open(FAMS)}
    intr = {json.loads(l)["family_id"]: json.loads(l) for l in open(INTR)}
    order = list(fams)[: a.limit] if a.limit else list(fams)
    for m in a.models:
        tag, path = m.split("=", 1)
        if (OUT / f"{tag}{a.suffix}.scores.csv.gz").exists():
            print(f"[{tag}] exists, skip", flush=True)
            continue
        t0 = time.time()
        model, tok = lmscore.load(path, dtype=getattr(torch, a.dtype))
        nL = len(layers_of(model))
        P = {}
        for fid in order:
            f, n = fams[fid], intr[fid]
            P[fid] = dict(f["primes"], NB=n["primes"]["NB"], NC=n["primes"]["NC"])
        # ---- (c) role probes on NP last-token states
        S = {c: {} for c in ["TB", "TC", "CUE", "NC", "NB", "PASS"]}
        for fid in order:
            for c in ["TB", "TC", "CUE", "NC", "NB"]:
                S[c][fid] = np_states(model, tok, P[fid][c], fams[fid]["np"])
            if fid in PASS:
                S["PASS"][fid] = np_states(model, tok, PASS[fid], fams[fid]["np"])
        folds = [order[0::2], order[1::2]]
        probe_rows, dirs = [], {}
        for li in range(nL):
            acc, p_nb, p_pass = [], [], []
            for k in (0, 1):
                tr, te = folds[1 - k], folds[k]
                Xtr = torch.stack([S[c][f][li] for f in tr for c in OBJ + SUBJ]).numpy()
                ytr = np.array(([1] * len(OBJ) + [0] * len(SUBJ)) * len(tr))
                mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-6
                clf = LogisticRegression(max_iter=2000, C=0.1).fit((Xtr - mu) / sd, ytr)
                held = [c for c in ["TB", "TC", "CUE", "NC"]]  # always test on all four, incl. classes not trained on
                Xte = torch.stack([S[c][f][li] for f in te for c in held]).numpy()
                acc.append(clf.score((Xte - mu) / sd, np.array([1, 1, 0, 0] * len(te))))
                p_nb += list(clf.predict_proba((torch.stack([S["NB"][f][li] for f in te]).numpy() - mu) / sd)[:, 1])
                pf = [f for f in te if f in S["PASS"]]
                if pf:
                    p_pass += list(clf.predict_proba((torch.stack([S["PASS"][f][li] for f in pf]).numpy() - mu) / sd)[:, 1])
                obj = torch.stack([S[c][f][li] for f in tr for c in OBJ]).mean(0)
                sub = torch.stack([S[c][f][li] for f in tr for c in SUBJ]).mean(0)
                u = (obj - sub) / (obj - sub).norm()
                for f in te:  # direction fit without the family itself
                    dirs[(f, li)] = (u, float(sub @ u))
            probe_rows.append(f"{li},{np.mean(acc):.4f},{np.mean(p_nb):.4f},{np.mean(p_pass) if p_pass else float('nan'):.4f}")
        with open(OUT / f"{tag}{a.suffix}.probe.csv", "w") as fo:
            fo.write("layer,cv_acc,p_obj_NB,p_obj_PASS\n" + "\n".join(probe_rows) + "\n")
        print(f"[{tag}] probes done ({time.time()-t0:.0f}s); best acc {max(float(r.split(',')[1]) for r in probe_rows):.3f}", flush=True)
        del S
        # ---- (a, b, d) scoring
        lo, hi = nL // 4, (3 * nL) // 4
        gen = torch.Generator().manual_seed(0)
        rows = []
        for fid in order:
            f = fams[fid]
            tg = targets_for(f, [intr[fid]["intr_verb"][:5]], fams)
            tails = [(pre, cont) for _, _, pre, cont in tg]
            jobs = {}
            for c in ["CUE", "NC"]:
                ids = enc_prime(tok, P[fid][c], f["np"])[0]
                kv, last = run_hooked(model, ids)
                jobs[c] = (kv, len(ids), last)
            for rec in ["GP", "NB"]:
                ids, npp, mcp = enc_prime(tok, P[fid][rec], f["np"])
                kvB, lastB = run_hooked(model, ids)
                jobs[f"{rec}|none"] = (kvB, len(ids), lastB)
                for cell, dtext in [(c, t) for c, t in [("SAME", NEUTRAL + P[fid][rec]), ("NBD", P[fid]["NB"])] if c in CELLS_ON]:
                    dids, dnp, _ = enc_prime(tok, dtext, f["np"])
                    if len(dnp) != len(npp):
                        continue
                    _, dhs, _ = run_prefix(model, dids)
                    kvA, _, _ = run_prefix(model, ids, patch=(npp, [h[dnp] for h in dhs]))
                    jobs[f"{rec}|{cell}"] = (mix(kvB, kvA, npp), len(ids), lastB)
                # role-direction edit and random controls
                rand = [torch.randn(model.config.hidden_size, generator=gen) for _ in range(3)]
                rand = [r / r.norm() for r in rand]

                def make_edit(kind):
                    def edit(li, h):
                        if not (lo <= li < hi):
                            return
                        u, m_sub = dirs[(fid, li)]
                        uu = u.to(h.device, h.dtype)
                        hh = h[0, npp]
                        shift = (m_sub - (hh.float() @ uu.float())).to(h.dtype)  # [n_np]
                        d = uu if kind is None else rand[kind].to(h.device, h.dtype)
                        h[0, npp] = hh + shift[:, None] * d[None]
                    return edit
                for cell, kind in [(c, k) for c, k in [("ROLE", None), ("RAND0", 0), ("RAND1", 1), ("RAND2", 2)] if c.rstrip("012") in CELLS_ON]:
                    kv, last = run_hooked(model, ids, edit=make_edit(kind))
                    jobs[f"{rec}|{cell}"] = (kv, len(ids), last)
            for cond, (kv, plen, last) in jobs.items():
                sc = score_tails(model, tok, kv, plen, last, tails, a.bs)
                acc = defaultdict(dict)
                for (tf, kind, _, _), s in zip(tg, sc):
                    acc[tf][kind] = s
                for tf, d in acc.items():
                    rows.append(f"{fid},{cond},{tf},{d['T']:.5f},{d['I']:.5f},{d['T']-d['I']:.5f},{d['D']:.5f},{d['Dc']:.5f}")
            print(f"[{tag}] {fid} done ({time.time()-t0:.0f}s)", flush=True)
        with gzip.open(OUT / f"{tag}{a.suffix}.scores.csv.gz", "wt") as fo:
            fo.write("prime_family,cond,target_family,lpT,lpI,L,lpD,lpDc\n" + "\n".join(rows) + "\n")
        json.dump({"tag": tag, "model": path, "dtype": a.dtype, "seconds": time.time() - t0, "layers_edited": [lo, hi]},
                  open(OUT / f"{tag}{a.suffix}.meta.json", "w"))
        print(f"[{tag}] wrote scores", flush=True)
        del model
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
