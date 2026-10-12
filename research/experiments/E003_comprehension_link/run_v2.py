"""E003 v2 scoring: comprehension, priming and prime-internal probes on Christianson 2001 cells.

Per model writes to results/gp/E003/:
  <tag>.comp.csv      family,verb_class,length,plaus,form,qkey,format,order,lpYes,lpNo,logodds
  <tag>.prime.csv.gz  family,verb_class,length,plaus,form,target_family,lpT,lpI,L,lpD,lpDc
  <tag>.probes.csv    family,verb_class,length,plaus,probe,lp
Targets: a fixed set of 48 E001 NP/Z families (seeded), minus any sharing a content stem with the
prime family. Target items: comma-placement pair T/I and disambiguating word in GP / comma target.
Usage: python run_v2.py --models tag=path ...
"""
import argparse
import gc
import gzip
import json
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
import lmscore  # noqa: E402

CELLS = ROOT / "data/gp_behavior/derived/e003_cells_v2.jsonl"
TGT = ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl"
OUT = ROOT / "results/gp/E003"
N_TARGETS = 48
COMP_FORMS = ["GP", "CUE", "CTL", "TB", "TC", "REORD"]
INSTR = {"YN": "Read the sentence and answer the question with Yes or No.",
         "NY": "Read the sentence and answer the question with No or Yes."}


def targets():
    fams = [json.loads(l) for l in open(TGT)]
    rng = random.Random(0)
    return rng.sample(fams, N_TARGETS)


def comp_items(tok, cells):
    items, keys = [], []
    chat = bool(getattr(tok, "chat_template", None))
    for c in cells:
        for form in COMP_FORMS:
            if form not in c["forms"]:
                continue
            for qk, q in c["q"].items():
                if not q:
                    continue
                for order, ins in INSTR.items():
                    body = f"{ins}\n\nSentence: {c['forms'][form]}\nQuestion: {q}"
                    fmts = {"plain": (body + "\nAnswer:", " ")}
                    if chat:
                        # enable_thinking=False: Qwen3 templates otherwise open a <think> block;
                        # other templates ignore the extra variable.
                        ctx = tok.apply_chat_template([{"role": "user", "content": body}], tokenize=False,
                                                      add_generation_prompt=True, enable_thinking=False)
                        if tok.bos_token and ctx.startswith(tok.bos_token):
                            ctx = ctx[len(tok.bos_token):]
                        fmts["chat"] = (ctx, "")
                    for fmt, (ctx, sp) in fmts.items():
                        for ans in ("Yes", "No"):
                            items.append((ctx, sp + ans))
                            keys.append((c, form, qk, fmt, order, ans))
    return items, keys


def prime_items(cells, tg):
    items, keys = [], []
    for c in cells:
        st = set(c["content_stems"])
        for form, s in c["forms"].items():
            for fj in tg:
                if st & set(fj["content_stems"]):
                    continue
                th = f"{fj['subord']} {fj['subj_v']}"
                w1 = " " + fj["rest"].split()[0]
                for t, (pre, cont) in {"T": ("", fj["target_T"]), "I": ("", fj["target_I"]),
                                       "D": (f"{th} {fj['np']}", w1), "Dc": (f"{th}, {fj['np']}", w1)}.items():
                    items.append((s + " " + pre, cont))
                    keys.append((c, form, fj["family_id"], t))
    return items, keys


def cid(c):
    return f"{c['family_id']},{c['verb_class']},{c['length']},{c['plaus']}"


def run_one(tag, path, cells, tg, batch):
    import torch
    t0 = time.time()
    model, tok = lmscore.load(path)
    ci, ck = comp_items(tok, cells)
    cr = lmscore.score(model, tok, ci, batch_size=batch)
    acc = {}
    for (c, form, qk, fmt, order, ans), r in zip(ck, cr):
        acc.setdefault((cid(c), form, qk, fmt, order), {})[ans] = r["lp"]
    with open(OUT / f"{tag}.comp.csv", "w") as f:
        f.write("family,verb_class,length,plaus,form,qkey,format,order,lpYes,lpNo,logodds\n")
        for (k, form, qk, fmt, order), d in acc.items():
            f.write(f"{k},{form},{qk},{fmt},{order},{d['Yes']:.5f},{d['No']:.5f},{d['Yes']-d['No']:.5f}\n")
    pi, pk = prime_items(cells, tg)
    pr = lmscore.score(model, tok, pi, batch_size=batch)
    acc = {}
    for (c, form, j, t), r in zip(pk, pr):
        acc.setdefault((cid(c), form, j), {})[t] = r["lp"]
    with gzip.open(OUT / f"{tag}.prime.csv.gz", "wt") as f:
        f.write("family,verb_class,length,plaus,form,target_family,lpT,lpI,L,lpD,lpDc\n")
        for (k, form, j), d in acc.items():
            f.write(f"{k},{form},{j},{d['T']:.5f},{d['I']:.5f},{d['T']-d['I']:.5f},{d['D']:.5f},{d['Dc']:.5f}\n")
    qi = [(c, n, ctx, w) for c in cells for n, (ctx, w) in c["probes"].items()]
    qr = lmscore.score(model, tok, [(ctx, w) for _, _, ctx, w in qi], batch_size=batch)
    with open(OUT / f"{tag}.probes.csv", "w") as f:
        f.write("family,verb_class,length,plaus,probe,lp\n")
        for (c, n, _, _), r in zip(qi, qr):
            f.write(f"{cid(c)},{n},{r['lp']:.5f}\n")
    meta = {"tag": tag, "model": path, "n_comp": len(ci), "n_prime": len(pi), "seconds": time.time() - t0}
    json.dump(meta, open(OUT / f"{tag}.meta.json", "w"))
    print(json.dumps(meta), flush=True)
    del model
    gc.collect()
    torch.cuda.empty_cache()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--batch", type=int, default=128)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    cells = [json.loads(l) for l in open(CELLS)]
    tg = targets()
    for m in a.models:
        tag, path = m.split("=", 1)
        if (OUT / f"{tag}.meta.json").exists():
            print(f"[{tag}] exists, skip", flush=True)
            continue
        try:
            run_one(tag, path, cells, tg, a.batch)
        except Exception as e:
            print(f"[{tag}] FAILED: {e!r}", flush=True)


if __name__ == "__main__":
    main()
