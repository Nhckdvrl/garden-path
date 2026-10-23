"""E015: overridden statements (see README).

For every item: M = log P(" A") - log P(" B") after context + " " + probe, for CORR, CTRL, PRE, and for the
re-encoding patch: in CORR (and CTRL) the residual-stream states of the overridden statement's tokens are
replaced at every layer by those of the same tokens in PRE (and CTRL_PRE), the rest is recomputed, and the
probe reads either the re-encoded span only (CLAIM) or the whole recomputed context (FULL).
Output: results/gp/E015/<tag>.csv  (id, cond, lpA, lpB, M)
"""
import argparse
import json
import sys
import time
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
sys.path.insert(0, str(ROOT / "research/experiments/E013_stale_states"))
import lmscore  # noqa: E402
from run import mix, run_prefix, score_tails  # noqa: E402

ITEMS = ROOT / "data/gp_behavior/derived/e015_items_v1.jsonl"
OUT = ROOT / "results/gp/E015"


def enc_span(tok, text, span):
    e = tok(text, add_special_tokens=False, return_offsets_mapping=True)
    ids = [lmscore._bos(tok)] + e["input_ids"]
    offs = [(-1, -1)] + [tuple(o) for o in e["offset_mapping"]]
    a = text.index(span)
    b = a + len(span)
    pos = [k for k, (s, t) in enumerate(offs) if s >= 0 and s < b and t > a]
    return ids, pos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--dtype", default="float32")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    items = [json.loads(l) for l in open(ITEMS)]
    if a.limit:
        items = items[: a.limit]
    for m in a.models:
        tag, path = m.split("=", 1)
        dst = OUT / f"{tag}.csv"
        if dst.exists():
            print(f"[{tag}] exists, skip", flush=True)
            continue
        t0 = time.time()
        model, tok = lmscore.load(path, dtype=getattr(torch, a.dtype))
        rows, skipped = ["id,cond,lpA,lpB,M"], 0
        for it in items:
            tails = [(it["probe"], " " + it["A"]), (it["probe"], " " + it["B"])]
            jobs = {}
            for cond in ("CORR", "CTRL", "PRE"):
                ids, _ = enc_span(tok, it[cond], it["claim_A"] if cond != "CTRL" else it["claim_A_other"])
                kv, _, last = run_prefix(model, ids)
                jobs[cond] = (kv, len(ids), last)
            for rec, don, span in (("CORR", "PRE", it["claim_A"]), ("CTRL", "CTRL_PRE", it["claim_A_other"])):
                ids, pos = enc_span(tok, it[rec], span)
                dids, dpos = enc_span(tok, it[don], span)
                if len(pos) != len(dpos):
                    skipped += 1
                    continue
                _, dhs, _ = run_prefix(model, dids)
                kvB, _, lastB = run_prefix(model, ids)
                kvA, _, lastA = run_prefix(model, ids, patch=(pos, [h[dpos] for h in dhs]))
                jobs[f"{rec}|CLAIM"] = (mix(kvB, kvA, pos), len(ids), lastB)
                jobs[f"{rec}|FULL"] = (kvA, len(ids), lastA)
            for cond, (kv, plen, last) in jobs.items():
                lpA, lpB = score_tails(model, tok, kv, plen, last, tails, 8)
                rows.append(f"{it['id']},{cond},{lpA:.5f},{lpB:.5f},{lpA-lpB:.5f}")
        dst.write_text("\n".join(rows) + "\n")
        json.dump({"tag": tag, "model": path, "dtype": a.dtype, "seconds": time.time() - t0, "span_mismatch": skipped},
                  open(OUT / f"{tag}.meta.json", "w"))
        print(f"[{tag}] wrote {dst.name} ({time.time()-t0:.0f}s, span mismatches {skipped})", flush=True)
        del model
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
