"""Generate candidate alternative main-clause continuations for each discovery family's NP.

Generator: a local instruct model (default Qwen2.5-14B-Instruct). Output is CANDIDATES only;
naturalness/role validity is checked by a different model (check_continuations.py) and by
rule filters. Raw prompts and outputs are saved for audit.
"""
import argparse, json, re, sys
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).resolve().parents[3]
FAMS = ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl"
OUT = ROOT / "data/gp_behavior/derived/e006_continuation_candidates_v1.jsonl"

PROMPT = """Here is a sentence: "{sent}"
Write 8 different natural English continuations for the phrase "{NP} ..." in which "{np}" is the grammatical SUBJECT of a new clause.
Rules:
- Each continuation starts IMMEDIATELY with the verb or auxiliary (e.g. "ran away.", "was sleeping nearby.", "had already gone.", "seemed nervous.").
- Use a variety of verbs and auxiliaries; do not start two continuations with the same word.
- Each must be plausible for {np} and fit the situation "{sub}".
- 3 to 8 words each, end with a period.
- Do NOT repeat the original continuation "{rest}".
Return only a JSON list of 8 strings."""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--model", default="Qwen/Qwen2.5-14B-Instruct"); a = ap.parse_args()
    fams = [json.loads(l) for l in open(FAMS)]
    tok = AutoTokenizer.from_pretrained(a.model); tok.padding_side = "left"
    m = AutoModelForCausalLM.from_pretrained(a.model, dtype=torch.bfloat16, device_map="cuda").eval()
    prompts = []
    for f in fams:
        msg = PROMPT.format(sent=f["primes"]["CUE"], NP=f["np"][0].upper() + f["np"][1:], np=f["np"],
                            sub=f"{f['subord'].lower()} {f['subj_v']}", rest=f["rest"])
        prompts.append(tok.apply_chat_template([{"role": "user", "content": msg}], tokenize=False, add_generation_prompt=True))
    out = []
    for i in range(0, len(prompts), 16):
        enc = tok(prompts[i:i+16], return_tensors="pt", padding=True).to("cuda")
        with torch.no_grad():
            g = m.generate(**enc, max_new_tokens=300, do_sample=False)
        out += tok.batch_decode(g[:, enc.input_ids.shape[1]:], skip_special_tokens=True)
    with open(OUT, "w") as fo:
        for f, p, o in zip(fams, prompts, out):
            try:
                cands = json.loads(re.search(r"\[.*\]", o, re.S).group(0))
            except Exception:
                cands = []
            fo.write(json.dumps({"family_id": f["family_id"], "generator": a.model, "prompt": p, "raw": o,
                                 "candidates": [c.strip() for c in cands if isinstance(c, str)]}) + "\n")
    print("wrote", OUT.relative_to(ROOT), sum(1 for o in out))

if __name__ == "__main__":
    main()
