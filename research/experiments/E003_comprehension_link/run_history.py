"""E003c: processing history vs primacy for lingering misinterpretation.

The GP (or CUE) sentence is always the labelled primary sentence; a preceding context line either
removes the garden path without asserting the obsolete relation (CTX_DIS: the main clause alone;
CTX_REORD: matrix-subordinate paraphrase) or is neutral (CTX_NEU). Plus a neutral-label order test
("Version 1/Version 2"). Yes/No scoring as in run_v2; probes give the disambiguator surprisal in
the GP sentence after each context (manipulation check).
Writes results/gp/E003c/<tag>.comp.csv, <tag>.probes.csv
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
OUT = ROOT / "results/gp/E003c"
NEUTRAL = "The weather was mild that day."
INSTR = {"YN": "Read the text and answer the question about the sentence with Yes or No.",
         "NY": "Read the text and answer the question about the sentence with No or Yes."}


def cap(s):
    return s[0].upper() + s[1:]


def contexts(c):
    """DIS = the main clause alone ("The deer ran into the woods."), recovered exactly from the
    FINAL template "Is it true that {np region} {rest}?"; it states nothing about V's object."""
    main_clause = c["q"]["FINAL_template"][len("Is it true that "):-1]
    return {"DIS": cap(main_clause) + ".", "NEU": NEUTRAL, "REORD": c["forms"]["REORD"]}


def bodies(c, q, ins):
    f = c["forms"]
    ctx = contexts(c)
    out = {}
    for cn, ct in ctx.items():
        for form in ("GP", "CUE"):
            out[f"CTX_{cn}_{form}"] = f"{ins}\n\nContext: {ct}\nSentence: {f[form]}\nQuestion: {q}"
    for a, b in (("GP", "CUE"), ("CUE", "GP"), ("GP", "GP"), ("CUE", "CUE")):
        out[f"VER_{a}_{b}"] = f"{ins}\n\nVersion 1: {f[a]}\nVersion 2: {f[b]}\nQuestion: {q}"
    return out


def items(tok, cells):
    chat = bool(getattr(tok, "chat_template", None))
    its, keys = [], []
    for c in cells:
        for qk, q in c["q"].items():
            if not q:
                continue
            for order, ins in INSTR.items():
                for cond, body in bodies(c, q, ins).items():
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


def probes(cells):
    ins = INSTR["YN"]
    its, keys = [], []
    for c in cells:
        f = c["forms"]
        pre, w1 = c["probes"]["GP_dis"]
        cpre, _ = c["probes"]["CUE_dis"]
        for cn, ct in contexts(c).items():
            its.append((f"{ins}\n\nContext: {ct}\nSentence: {pre}", w1)); keys.append((c, f"CTX_{cn}_GP"))
            its.append((f"{ins}\n\nContext: {ct}\nSentence: {cpre}", w1)); keys.append((c, f"CTX_{cn}_CUE"))
        its.append((f"{ins}\n\nVersion 1: {pre}", w1)); keys.append((c, "VER1_GP"))
        its.append((f"{ins}\n\nVersion 1: {cpre}", w1)); keys.append((c, "VER1_CUE"))
        its.append((f"{ins}\n\nVersion 1: {f['CUE']}\nVersion 2: {pre}", w1)); keys.append((c, "VER_CUE_GP_second"))
        its.append((f"{ins}\n\nVersion 1: {f['GP']}\nVersion 2: {cpre}", w1)); keys.append((c, "VER_GP_CUE_second"))
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
                acc.setdefault((c["family_id"], c["verb_class"], c["length"], c["plaus"], cond, qk, fmt, order), {})[ans] = r["lp"]
            with open(OUT / f"{tag}.comp.csv", "w") as f:
                f.write("family,verb_class,length,plaus,cond,qkey,format,order,lpYes,lpNo,logodds\n")
                for k, d in acc.items():
                    f.write(",".join(k) + f",{d['Yes']:.5f},{d['No']:.5f},{d['Yes']-d['No']:.5f}\n")
            pits, pkeys = probes(cells)
            pres = lmscore.score(model, tok, pits, batch_size=a.batch)
            with open(OUT / f"{tag}.probes.csv", "w") as f:
                f.write("family,verb_class,length,plaus,probe,lp\n")
                for (c, name), r in zip(pkeys, pres):
                    f.write(f"{c['family_id']},{c['verb_class']},{c['length']},{c['plaus']},{name},{r['lp']:.5f}\n")
            json.dump({"tag": tag, "model": path, "n": len(its), "seconds": time.time() - t0},
                      open(OUT / f"{tag}.meta.json", "w"))
            print(f"[{tag}] done {time.time()-t0:.0f}s", flush=True)
            del model
            gc.collect(); torch.cuda.empty_cache()
        except Exception as e:
            print(f"[{tag}] FAILED: {e!r}", flush=True)


if __name__ == "__main__":
    main()
