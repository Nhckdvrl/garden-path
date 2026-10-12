"""E003 comprehension scoring: log P(Yes) - log P(No) for GP/CUE x OBS/FINAL items.

Two formats per item:
  plain: "Sentence: {s}\nQuestion: {q}\nAnswer (Yes or No):"  scored on " Yes" / " No"
  chat : tokenizer chat template (if present), user turn = same text, scored on "Yes" / "No"
Writes results/gp/E003/<tag>.comprehension.csv.
Usage: python run.py --models tag=path ...   (do NOT run without GPU authorization; see README)
"""
import argparse
import gc
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
import lmscore  # noqa: E402

ITEMS = ROOT / "data/gp_behavior/derived/e003_comprehension_items_v1.jsonl"
OUT = ROOT / "results/gp/E003"
INSTR = "Read the sentence and answer the question with Yes or No."


def prompts(tok, it):
    body = f"{INSTR}\n\nSentence: {it['sentence']}\nQuestion: {it['question']}"
    out = {"plain": (body + "\nAnswer (Yes or No):", " ")}
    if getattr(tok, "chat_template", None):
        ctx = tok.apply_chat_template([{"role": "user", "content": body}], tokenize=False,
                                      add_generation_prompt=True)
        if tok.bos_token and ctx.startswith(tok.bos_token):
            ctx = ctx[len(tok.bos_token):]  # lmscore adds BOS itself
        out["chat"] = (ctx, "")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--batch", type=int, default=64)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    items = [json.loads(l) for l in open(ITEMS)]
    for spec in a.models:
        tag, path = spec.split("=", 1)
        if (OUT / f"{tag}.comprehension.csv").exists():
            continue
        try:
            import torch
            model, tok = lmscore.load(path)
            q, keys = [], []
            for k, it in enumerate(items):
                for fmt, (ctx, sp) in prompts(tok, it).items():
                    for ans in ("Yes", "No"):
                        q.append((ctx, sp + ans))
                        keys.append((k, fmt, ans))
            res = lmscore.score(model, tok, q, batch_size=a.batch)
            acc = {}
            for (k, fmt, ans), r in zip(keys, res):
                acc.setdefault((k, fmt), {})[ans] = r["lp"]
            with open(OUT / f"{tag}.comprehension.csv", "w") as f:
                f.write("family_id,form,qtype,format,lpYes,lpNo,logodds\n")
                for (k, fmt), d in acc.items():
                    it = items[k]
                    f.write(f"{it['family_id']},{it['form']},{it['qtype']},{fmt},{d['Yes']:.5f},{d['No']:.5f},{d['Yes']-d['No']:.5f}\n")
            print(f"[{tag}] done", flush=True)
            del model
            gc.collect(); torch.cuda.empty_cache()
        except Exception as e:
            print(f"[{tag}] FAILED: {e!r}", flush=True)


if __name__ == "__main__":
    main()
