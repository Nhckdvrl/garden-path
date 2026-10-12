"""E003b: does rereading / processing history change lingering misinterpretation?

Same Christianson cells and Yes/No scoring as run_v2 (comprehension only). The sentence slot
of the prompt is replaced by a presentation condition:
  GP1      Sentence: GP
  GP2      Sentence: GP / Sentence (read again): GP          (second copy not garden-pathed; E004)
  CUE1     Sentence: CUE
  CUE2     Sentence: CUE / Sentence (read again): CUE         (repetition control)
  GP_CUE   Sentence: GP / Same sentence with punctuation: CUE (explicit disambiguation after GP)
  CUE_GP   Sentence: CUE / Same sentence without punctuation: GP
  QFIRST_GP / QFIRST_CUE   question shown before the sentence
  TC1      Sentence: TC  (transitive reference)
Writes results/gp/E003b/<tag>.comp.csv
"""
import argparse
import gc
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/tools"))
import lmscore  # noqa: E402

CELLS = ROOT / "data/gp_behavior/derived/e003_cells_v2.jsonl"
OUT = ROOT / "results/gp/E003b"
INSTR = {"YN": "Read the text and answer the question with Yes or No.",
         "NY": "Read the text and answer the question with No or Yes."}


def bodies(f, q, ins):
    gp, cue, tc = f["GP"], f["CUE"], f["TC"]
    return {
        "GP1": f"{ins}\n\nSentence: {gp}\nQuestion: {q}",
        "GP2": f"{ins}\n\nSentence: {gp}\nSentence (read again): {gp}\nQuestion: {q}",
        "CUE1": f"{ins}\n\nSentence: {cue}\nQuestion: {q}",
        "CUE2": f"{ins}\n\nSentence: {cue}\nSentence (read again): {cue}\nQuestion: {q}",
        "GP_CUE": f"{ins}\n\nSentence: {gp}\nSame sentence with punctuation: {cue}\nQuestion: {q}",
        "CUE_GP": f"{ins}\n\nSentence: {cue}\nSame sentence without punctuation: {gp}\nQuestion: {q}",
        "QFIRST_GP": f"{ins}\n\nQuestion: {q}\nSentence: {gp}\nQuestion (repeated): {q}",
        "QFIRST_CUE": f"{ins}\n\nQuestion: {q}\nSentence: {cue}\nQuestion (repeated): {q}",
        "TC1": f"{ins}\n\nSentence: {tc}\nQuestion: {q}",
    }


def items(tok, cells):
    chat = bool(getattr(tok, "chat_template", None))
    its, keys = [], []
    for c in cells:
        for qk, q in c["q"].items():
            if not q:
                continue
            for order, ins in INSTR.items():
                for cond, body in bodies(c["forms"], q, ins).items():
                    fmts = {"plain": (body + "\nAnswer:", " ")}
                    if chat:
                        ctx = tok.apply_chat_template([{"role": "user", "content": body}], tokenize=False,
                                                      add_generation_prompt=True, enable_thinking=False)
                        if tok.bos_token and ctx.startswith(tok.bos_token):
                            ctx = ctx[len(tok.bos_token):]
                        fmts["chat"] = (ctx, "")
                    for fmt, (ctx, sp) in fmts.items():
                        for ans in ("Yes", "No"):
                            its.append((ctx, sp + ans))
                            keys.append((c, cond, qk, fmt, order, ans))
    return its, keys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--batch", type=int, default=64)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    cells = [json.loads(l) for l in open(CELLS)]
    for m in a.models:
        tag, path = m.split("=", 1)
        if (OUT / f"{tag}.meta.json").exists():
            continue
        try:
            import torch
            t0 = time.time()
            model, tok = lmscore.load(path)
            its, keys = items(tok, cells)
            res = lmscore.score(model, tok, its, batch_size=a.batch)
            acc = {}
            for (c, cond, qk, fmt, order, ans), r in zip(keys, res):
                k = (c["family_id"], c["verb_class"], c["length"], c["plaus"], cond, qk, fmt, order)
                acc.setdefault(k, {})[ans] = r["lp"]
            with open(OUT / f"{tag}.comp.csv", "w") as f:
                f.write("family,verb_class,length,plaus,cond,qkey,format,order,lpYes,lpNo,logodds\n")
                for k, d in acc.items():
                    f.write(",".join(k) + f",{d['Yes']:.5f},{d['No']:.5f},{d['Yes']-d['No']:.5f}\n")
            json.dump({"tag": tag, "model": path, "n": len(its), "seconds": time.time() - t0},
                      open(OUT / f"{tag}.meta.json", "w"))
            print(f"[{tag}] done {time.time()-t0:.0f}s", flush=True)
            del model
            gc.collect(); torch.cuda.empty_cache()
        except Exception as e:
            print(f"[{tag}] FAILED: {e!r}", flush=True)


if __name__ == "__main__":
    main()
