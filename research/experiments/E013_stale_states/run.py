"""E013: stale-NP-state patching (see README).

For each prime family and recipient (GP, NB) builds run B (original) and run A (residual
stream at the NP tokens replaced at every layer by the donor's NP states; donor CUE for GP,
NC for NB), mixes their KV caches by span (none / NP / MC / both), and scores all
content-disjoint E002 targets (T, I, D, Dc) against each cache. CUE and NC are scored
unpatched through the same pipeline.

Output: results/gp/E013/<tag>.scores.csv.gz with columns
prime_family,cond,target_family,lpT,lpI,L,lpD,lpDc  (cond = GP|none, GP|NP, ..., CUE, NC)
Usage: python run.py --models tag=path [--limit N]
"""
import argparse
import gzip
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import DynamicCache

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
import lmscore  # noqa: E402

FAMS = ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl"
INTR = ROOT / "data/gp_behavior/derived/npz_intransitive_controls_v1.jsonl"
OUT = ROOT / "results/gp/E013"
CELLS = ["none", "NP", "MC", "both"]


def layers_of(model):
    m = model.model if hasattr(model, "model") else model.gpt_neox
    return m.layers


def targets_for(fi, extra, fams):
    st = set(fi["content_stems"]) | set(extra)
    out = []
    for fj in fams.values():
        if fj["family_id"] == fi["family_id"] or st & set(fj["content_stems"]):
            continue
        th = f"{fj['subord']} {fj['subj_v']}"
        w1 = " " + fj["rest"].split()[0]
        out += [(fj["family_id"], "T", "", fj["target_T"]), (fj["family_id"], "I", "", fj["target_I"]),
                (fj["family_id"], "D", f"{th} {fj['np']}", w1), (fj["family_id"], "Dc", f"{th}, {fj['np']}", w1)]
    return out


def enc_prime(tok, text, np_str):
    """ids with BOS; token positions of the NP (first occurrence after the verb) and of MC."""
    e = tok(text, add_special_tokens=False, return_offsets_mapping=True)
    ids = [lmscore._bos(tok)] + e["input_ids"]
    offs = [(-1, -1)] + [tuple(o) for o in e["offset_mapping"]]
    a = text.index(" " + np_str + " ") if (" " + np_str + " ") in text else text.index(" " + np_str)
    b = a + 1 + len(np_str)
    np_pos = [k for k, (s, t) in enumerate(offs) if s >= 0 and s < b and t > a]
    mc_pos = [k for k, (s, t) in enumerate(offs) if s >= b]
    return ids, np_pos, mc_pos


@torch.no_grad()
def run_prefix(model, ids, patch=None):
    """Forward the prime once. Records every decoder layer's output (raw residual stream).
    patch: (positions, per-layer donor states [n_pos, d][, first layer]) written into every layer's
    output from the first layer on (default 0)."""
    hooks, rec = [], []
    for li, layer in enumerate(layers_of(model)):
        def hook(mod, inp, out, li=li):
            h = out[0] if isinstance(out, tuple) else out
            if patch is not None and li >= (patch[2] if len(patch) > 2 else 0):
                h[0, patch[0]] = patch[1][li].to(h.dtype)
            rec.append(h[0].detach().clone())
            return out
        hooks.append(layer.register_forward_hook(hook))
    try:
        x = torch.tensor([ids], device=model.device)
        o = model(input_ids=x, use_cache=True)
    finally:
        for h in hooks:
            h.remove()
    pkv = o.past_key_values
    kv = [(k.clone(), v.clone()) for k, v in (pkv.to_legacy_cache() if hasattr(pkv, "to_legacy_cache") else pkv)]
    last = F.log_softmax(o.logits[0, -1].float(), -1).cpu()
    return kv, rec, last


def mix(kvB, kvA, pos):
    out = []
    for (kb, vb), (ka, va) in zip(kvB, kvA):
        k, v = kb.clone(), vb.clone()
        if pos:
            k[:, :, pos], v[:, :, pos] = ka[:, :, pos], va[:, :, pos]
        out.append((k, v))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--bs", type=int, default=256)
    ap.add_argument("--suffix", default="")
    ap.add_argument("--dtype", default="float32", help="float32 (exact) or bfloat16 (large models)")
    # E013b (exploratory): NB as donor for GP (no comma imported; NB<-NB is an identity patch), and
    # NP patches applied only from a fraction of the depth onward (cells "NPfrom<frac>")
    ap.add_argument("--donor", default="CUE", choices=["CUE", "NB"])
    ap.add_argument("--from_layers", default="", help="comma-separated depth fractions, e.g. 0,0.25,0.5,0.75")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    fams = {json.loads(l)["family_id"]: json.loads(l) for l in open(FAMS)}
    intr = {json.loads(l)["family_id"]: json.loads(l) for l in open(INTR)}
    order = list(fams)[: a.limit] if a.limit else list(fams)
    for m in a.models:
        tag, path = m.split("=", 1)
        dst = OUT / f"{tag}{a.suffix}.scores.csv.gz"
        if dst.exists():
            print(f"[{tag}] exists, skip", flush=True)
            continue
        t0 = time.time()
        model, tok = lmscore.load(path, dtype=getattr(torch, a.dtype))
        rows, nfail = [], 0
        for fid in order:
            f, n = fams[fid], intr[fid]
            P = dict(f["primes"]); P["NB"], P["NC"] = n["primes"]["NB"], n["primes"]["NC"]
            tg = targets_for(f, [n["intr_verb"][:5]], fams)
            tails = [(pre, cont) for _, _, pre, cont in tg]
            jobs = {}
            enc = {c: enc_prime(tok, P[c], f["np"]) for c in ["GP", "CUE", "NB", "NC"]}
            for c in ["CUE", "NC"]:
                kv, _, last = run_prefix(model, enc[c][0])
                jobs[c] = (kv, len(enc[c][0]), last)
            pairs = [("GP", "CUE"), ("NB", "NC")] if a.donor == "CUE" else [("GP", "NB"), ("NB", "NB")]
            nL = len(layers_of(model))
            for rec, don in pairs:
                ids, npp, mcp = enc[rec]
                dids, dnp, _ = enc[don]
                if len(npp) != len(dnp):
                    nfail += 1
                    continue
                _, dhs, _ = run_prefix(model, dids)
                donor_states = [h[dnp] for h in dhs]
                kvB, _, lastB = run_prefix(model, ids)
                kvA, _, lastA = run_prefix(model, ids, patch=(npp, donor_states))
                # the prime's final token belongs to MC, so its prediction comes from the run supplying MC
                for cell, pos, last in [("none", [], lastB), ("NP", npp, lastB), ("MC", mcp, lastA),
                                        ("both", npp + mcp, lastA)]:
                    jobs[f"{rec}|{cell}"] = (mix(kvB, kvA, pos), len(ids), last)
                for frac in [float(x) for x in a.from_layers.split(",") if x]:
                    kvF, _, _ = run_prefix(model, ids, patch=(npp, donor_states, int(round(frac * nL))))
                    jobs[f"{rec}|NPfrom{frac:g}"] = (mix(kvB, kvF, npp), len(ids), lastB)
            for cond, (kv, plen, last) in jobs.items():
                sc = score_tails(model, tok, kv, plen, last, tails, a.bs)
                acc = defaultdict(dict)
                for (tf, kind, _, _), s in zip(tg, sc):
                    acc[tf][kind] = s
                for tf, d in acc.items():
                    rows.append(f"{fid},{cond},{tf},{d['T']:.5f},{d['I']:.5f},{d['T']-d['I']:.5f},{d['D']:.5f},{d['Dc']:.5f}")
            print(f"[{tag}] {fid} done ({time.time()-t0:.0f}s)", flush=True)
        with gzip.open(dst, "wt") as fo:
            fo.write("prime_family,cond,target_family,lpT,lpI,L,lpD,lpDc\n" + "\n".join(rows) + "\n")
        json.dump({"tag": tag, "model": path, "dtype": a.dtype, "seconds": time.time() - t0, "np_len_mismatch": nfail},
                  open(OUT / f"{tag}{a.suffix}.meta.json", "w"))
        print(f"[{tag}] wrote {dst.name}; np mismatches {nfail}", flush=True)
        del model
        torch.cuda.empty_cache()


@torch.no_grad()
def score_tails(model, tok, kv, plen, last_lp, tails, bs):
    """Summed log-prob of each tail continuation after the cached prime (+ ' ').
    last_lp: log-probs at the prime's final position (predicts the first tail token)."""
    enc = []
    for pre, cont in tails:
        text = " " + pre + cont if pre else " " + cont
        e = tok(text, add_special_tokens=False, return_offsets_mapping=True)
        start = len(text) - len(cont)
        mask = [o[0] >= start or o[0] < start < o[1] for o in e["offset_mapping"]]
        enc.append((e["input_ids"], mask))
    res = [None] * len(enc)
    pad = tok.pad_token_id if tok.pad_token_id is not None else lmscore._bos(tok)
    order = sorted(range(len(enc)), key=lambda i: -len(enc[i][0]))
    for b in range(0, len(order), bs):
        idx = order[b:b + bs]
        n = len(idx)
        Lm = max(len(enc[i][0]) for i in idx)
        ids = torch.full((n, Lm), pad, dtype=torch.long)
        att = torch.zeros((n, plen + Lm), dtype=torch.long)
        att[:, :plen] = 1
        for r, i in enumerate(idx):
            s = enc[i][0]
            ids[r, :len(s)] = torch.tensor(s)
            att[r, plen:plen + len(s)] = 1
        cache = DynamicCache([(k.expand(n, -1, -1, -1).contiguous(), v.expand(n, -1, -1, -1).contiguous())
                              for k, v in kv])
        pos = torch.arange(plen, plen + Lm, device=model.device)[None].expand(n, -1)
        ids = ids.to(model.device)
        lg = model(input_ids=ids, attention_mask=att.to(model.device), past_key_values=cache,
                   position_ids=pos, use_cache=False).logits.float()
        lp = F.log_softmax(lg[:, :-1], -1).gather(-1, ids[:, 1:, None])[..., 0].cpu()
        first = last_lp[ids[:, 0].cpu()]
        for r, i in enumerate(idx):
            s, m = enc[i]
            tl = torch.cat([first[r:r + 1], lp[r, :len(s) - 1]])
            res[i] = float(tl[torch.tensor(m)].sum())
    return res


if __name__ == "__main__":
    main()
