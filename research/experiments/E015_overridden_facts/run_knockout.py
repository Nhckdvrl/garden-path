"""E015b: attention knockout for overridden statements (see E015b_README.md).

For each item, condition (CORR, CTRL) and cell, scores log P(A) and log P(B) after context + " " + probe with a
4D attention mask that blocks the listed query->key pairs at every layer and head.
Output: results/gp/E015/<tag>__knockout.csv (id, cond, cell, lpA, lpB, M)
"""
import argparse
import json
import sys
import time
from pathlib import Path

import torch
import torch.nn.functional as F

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
import lmscore  # noqa: E402

ITEMS = ROOT / "data/gp_behavior/derived/e015_items_v1.jsonl"
OUT = ROOT / "results/gp/E015"
CELLS = ["none", "KO_ANS_CLAIM", "KO_ANS_VALUE", "KO_ALL_CLAIM", "KO_ANS_CORR"]


def positions(offs, a, b):
    return [k for k, (s, t) in enumerate(offs) if s >= 0 and s < b and t > a]


@torch.no_grad()
def score(model, tok, ctx, probe, answer, claim, value, corr, cell):
    text = f"{ctx} {probe} {answer}"
    e = tok(text, add_special_tokens=False, return_offsets_mapping=True)
    ids = [lmscore._bos(tok)] + e["input_ids"]
    offs = [(-1, -1)] + [tuple(o) for o in e["offset_mapping"]]
    ca = text.index(claim)
    cl = positions(offs, ca, ca + len(claim))
    va = ca + claim.rindex(value)
    vl = positions(offs, va, va + len(value))
    ra = text.index(corr)
    rl = positions(offs, ra, ra + len(corr))
    pa = len(ctx) + 1
    ans_q = [k for k, (s, t) in enumerate(offs) if s >= pa]       # probe and answer tokens (queries)
    tgt = [k for k, (s, t) in enumerate(offs) if s >= len(text) - len(answer) - 1 and s >= 0]  # answer tokens
    n = len(ids)
    dt = next(model.parameters()).dtype
    neg = torch.finfo(dt).min
    mask = torch.triu(torch.full((n, n), neg, dtype=dt), 1)
    if cell == "KO_ANS_CLAIM":
        for q in ans_q:
            mask[q, cl] = neg
    elif cell == "KO_ANS_VALUE":
        for q in ans_q:
            mask[q, vl] = neg
    elif cell == "KO_ALL_CLAIM":
        for q in range(max(cl) + 1, n):
            mask[q, cl] = neg
    elif cell == "KO_ANS_CORR":
        for q in ans_q:
            mask[q, rl] = neg
    x = torch.tensor([ids], device=model.device)
    lg = model(input_ids=x, attention_mask=mask[None, None].to(model.device)).logits[0].float()
    lp = F.log_softmax(lg, -1)
    return float(sum(lp[k - 1, ids[k]] for k in tgt))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--dtype", default="float32")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    items = [json.loads(l) for l in open(ITEMS)]
    if a.limit:
        items = items[: a.limit]
    for m in a.models:
        tag, path = m.split("=", 1)
        dst = OUT / f"{tag}__knockout.csv"
        if dst.exists():
            print(f"[{tag}] exists, skip", flush=True)
            continue
        t0 = time.time()
        model, tok = lmscore.load(path, dtype=getattr(torch, a.dtype))
        rows = ["id,cond,cell,lpA,lpB,M"]
        for it in items:
            for cond, claim in (("CORR", it["claim_A"]), ("CTRL", it["claim_A_other"])):
                for cell in CELLS:
                    lpA = score(model, tok, it[cond], it["probe"], it["A"], claim, it["A"], it["claim_B"], cell)
                    lpB = score(model, tok, it[cond], it["probe"], it["B"], claim, it["A"], it["claim_B"], cell)
                    rows.append(f"{it['id']},{cond},{cell},{lpA:.5f},{lpB:.5f},{lpA-lpB:.5f}")
        dst.write_text("\n".join(rows) + "\n")
        json.dump({"tag": tag, "model": path, "dtype": a.dtype, "seconds": time.time() - t0},
                  open(OUT / f"{tag}__knockout.meta.json", "w"))
        print(f"[{tag}] wrote {dst.name} ({time.time()-t0:.0f}s)", flush=True)
        del model
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
