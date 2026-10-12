"""Filter generated continuations: (1) rule filter (past-tense/past-modal first word, no
repetition of the original first word); (2) independent naturalness rating of the full CUE
sentence by a DIFFERENT model (Llama-3.1-8B-Instruct): P(rating) over 1-5, expected score.
Keeps the original continuation as variant k=0. Writes the E006 variant file."""
import json, re
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).resolve().parents[3]
FAMS = ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl"
CAND = ROOT / "data/gp_behavior/derived/e006_continuation_candidates_v1.jsonl"
OUT = ROOT / "data/gp_behavior/derived/e006_variants_v1.jsonl"
JUDGE = "NousResearch/Meta-Llama-3.1-8B-Instruct"
PAST_MODAL = {"was", "were", "had", "could", "would", "might", "began", "became", "seemed", "looked", "grew",
              "rose", "fell", "ran", "gave", "made", "took", "stood", "felt", "got", "kept", "went", "came",
              "sat", "lay", "slid", "spun", "shook", "broke", "swam", "flew", "hid", "fled", "froze", "bit",
              "stuck", "drew", "led", "left", "lost", "held", "sank", "shone", "sprang", "struck", "wore",
              "tore", "threw", "spread", "burst", "split", "slipped", "did", "should"}
Q = ('Rate how natural and grammatical this English sentence is, from 1 (very unnatural or '
     'ungrammatical) to 5 (perfectly natural).\nSentence: "{s}"\nAnswer with a single digit.')


def past_ok(c):
    w = c.split()[0].lower()
    return w.endswith("ed") or w in PAST_MODAL


def main():
    fams = {json.loads(l)["family_id"]: json.loads(l) for l in open(FAMS)}
    cands = [json.loads(l) for l in open(CAND)]
    tok = AutoTokenizer.from_pretrained(JUDGE)
    m = AutoModelForCausalLM.from_pretrained(JUDGE, dtype=torch.bfloat16, device_map="cuda").eval()
    digit_ids = [tok.encode(str(d), add_special_tokens=False)[0] for d in range(1, 6)]

    def rate(sents):
        out = []
        for i in range(0, len(sents), 32):
            ps = [tok.apply_chat_template([{"role": "user", "content": Q.format(s=s)}], tokenize=False,
                                          add_generation_prompt=True) for s in sents[i:i + 32]]
            tok.padding_side = "left"
            if tok.pad_token is None:
                tok.pad_token = tok.eos_token
            enc = tok(ps, return_tensors="pt", padding=True, add_special_tokens=False).to("cuda")
            with torch.no_grad():
                lg = m(**enc).logits[:, -1, digit_ids].float().softmax(-1).cpu()
            out += [float((lg[j] * torch.arange(1, 6)).sum()) for j in range(len(ps))]
        return out

    rows = []
    for c in cands:
        f = fams[c["family_id"]]
        orig_first = f["rest"].split()[0].lower()
        seen = {orig_first}
        keep = []
        for x in c["candidates"]:
            x = x.strip().rstrip(".")
            if not x or not past_ok(x) or x.split()[0].lower() in seen:
                continue
            seen.add(x.split()[0].lower())
            keep.append(x)
        variants = [f["rest"]] + keep
        sents = [f"{f['subord']} {f['subj_v']}, {f['np']} {v}." for v in variants]
        rows.append((f, variants, sents))
    scores = rate([s for _, _, ss in rows for s in ss])
    k = 0
    with open(OUT, "w") as fo:
        for f, variants, sents in rows:
            for j, (v, s) in enumerate(zip(variants, sents)):
                fo.write(json.dumps({"family_id": f["family_id"], "variant": j, "rest": v, "is_original": j == 0,
                                     "cue_sentence": s, "naturalness_llama31_8b": scores[k], "judge": JUDGE}) + "\n")
                k += 1
    print("wrote", OUT.relative_to(ROOT), k)


if __name__ == "__main__":
    main()
