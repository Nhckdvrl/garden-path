"""Write the E014 contexts with a local instruction model (vLLM, Qwen3-32B, no thinking).

Greedy first; if a greedy output breaks a constraint, seeded samples (seed 0, n=8) are tried
in order. Nothing here looks at any scored model output.
Output: data/gp_behavior/derived/e014_contexts_v1.jsonl
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FAMS = ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl"
INTR = ROOT / "data/gp_behavior/derived/npz_intransitive_controls_v1.jsonl"
OUT = ROOT / "data/gp_behavior/derived/e014_contexts_v1.jsonl"

TYPES = {
    "OBJ": ("Write ONE short, natural English sentence (at most 14 words) that makes it very likely that "
            "{subj} is about to act on {np} as the thing being {verb}: {np} should be {subj}'s target or goal. "
            "Mention both {subj} and {np}."),
    "INT": ("Write ONE short, natural English sentence (at most 14 words) that describes {subj} and {np} as "
            "doing separate, unrelated things: {subj} is busy on their own, and {np} is acting on its own. "
            "It must not suggest that {subj} will do anything to {np}. Mention both {subj} and {np}."),
    "NEU": ("Write ONE short, natural English sentence (at most 14 words) that simply mentions {subj} and "
            "{np} as being in the same place, without saying what either is doing or how they relate."),
}
RULES = (" Rules: do not use the words {ban}; do not use any form of the verb '{verb}'; no commas; "
         "end with a period. Output only the sentence.")
STOP = set("the a an and of to in on at by for with from that this was were is are had has have be been "
           "into onto over under while as his her their its it they he she".split())


def stems(text):
    return {w[:5] for w in re.findall(r"[a-z]+", text.lower()) if len(w) >= 4 and w not in STOP}


def check(s, subj_head, np_head, banned):
    s = s.strip().strip('"')
    words = re.findall(r"[A-Za-z']+", s)
    low = [w.lower() for w in words]
    ok = (s.endswith(".") and s.count(".") == 1 and "," not in s and len(words) <= 16
          and subj_head in low and np_head in low
          and not any(w[:4] == b[:4] and len(w) >= 4 for w in low for b in banned))
    return ok, s


def main():
    from vllm import LLM, SamplingParams
    fams = [json.loads(l) for l in open(FAMS)]
    intr = {json.loads(l)["family_id"]: json.loads(l) for l in open(INTR)}
    llm = LLM(model=sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen3-32B", dtype="bfloat16",
              max_model_len=1024, max_num_seqs=256, gpu_memory_utilization=0.85, seed=0)
    tok = llm.get_tokenizer()
    jobs = []
    for f in fams:
        n = intr[f["family_id"]]
        subj = n["subj"]
        verb = f["subj_v"][len(subj):].strip()
        rest_words = [w for w in re.findall(r"[a-z]+", f["rest"].lower()) if w not in STOP and len(w) >= 4]
        banned = [verb.lower(), n["intr_verb"].lower()] + rest_words
        meta = dict(family_id=f["family_id"], subj=subj, verb=verb, np=f["np"], banned=banned,
                    subj_head=subj.split()[-1].lower(), np_head=f["np"].split()[-1].lower())
        for t, tmpl in TYPES.items():
            ask = (tmpl + RULES).format(subj=subj, np=f["np"], verb=verb, ban=", ".join(f"'{b}'" for b in banned))
            prompt = tok.apply_chat_template([{"role": "user", "content": ask}], tokenize=False,
                                             add_generation_prompt=True, enable_thinking=False)
            jobs.append((meta, t, prompt))
    greedy = llm.generate([p for _, _, p in jobs], SamplingParams(temperature=0, max_tokens=48))
    samp = llm.generate([p for _, _, p in jobs], SamplingParams(temperature=0.8, top_p=0.95, n=8, seed=0, max_tokens=48))
    out = {}
    for (meta, t, _), g, s in zip(jobs, greedy, samp):
        cands = [g.outputs[0].text] + [o.text for o in s.outputs]
        passing = []
        for c in cands:
            ok, c = check(c, meta["subj_head"], meta["np_head"], meta["banned"])
            if ok and c not in passing:
                passing.append(c)
        rec = out.setdefault(meta["family_id"], dict(meta, contexts={}))
        need = 1 if t == "NEU" else 2
        for k in range(need):
            name = t if t == "NEU" else f"{t}{k+1}"
            rec["contexts"][name] = passing[k] if len(passing) > k else None
    with open(OUT, "w") as fo:
        for r in out.values():
            fo.write(json.dumps(r) + "\n")
    miss = sum(v is None for r in out.values() for v in r["contexts"].values())
    print(f"wrote {OUT.name}: {len(out)} families, missing contexts {miss}")


if __name__ == "__main__":
    os.environ.setdefault("VLLM_WORKER_MULTIPROC_METHOD", "spawn")
    main()
