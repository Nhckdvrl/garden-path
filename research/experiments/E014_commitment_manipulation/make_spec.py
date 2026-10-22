"""E014 spec: each context (OBJ1, OBJ2, INT1, INT2, NEU) x prime (GP, CUE, NB, NC); cond = "<ctx>:<prime>".
Families with a missing context are dropped entirely (count printed). Context content words are
added to the family's stems so that no target shares a content word with the context.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
D = ROOT / "data/gp_behavior/derived"
OUT = ROOT / "research/experiments/E014_commitment_manipulation/spec.jsonl"
CTX = ["OBJ1", "OBJ2", "INT1", "INT2", "NEU"]
STOP = set("the a an and of to in on at by for with from that this was were is are had has have be been "
           "into onto over under while as his her their its it they he she".split())

fams = {json.loads(l)["family_id"]: json.loads(l) for l in open(D / "npz_prime_families_v1.jsonl")}
intr = {json.loads(l)["family_id"]: json.loads(l) for l in open(D / "npz_intransitive_controls_v1.jsonl")}
ctxs = {json.loads(l)["family_id"]: json.loads(l) for l in open(D / "e014_contexts_v1.jsonl")}

n_drop, n_out = 0, 0
with open(OUT, "w") as fo:
    for fid, f in fams.items():
        cx = ctxs[fid]["contexts"]
        if any(cx.get(c) is None for c in CTX):
            n_drop += 1
            continue
        n = intr[fid]
        P = dict(f["primes"]); P["NB"], P["NC"] = n["primes"]["NB"], n["primes"]["NC"]
        head = f"{f['subord']} {f['subj_v']}"
        nhead = f"{f['subord']} {n['subj']} {n['intr_verb']}"
        w1 = " " + f["rest"].split()[0]
        cstems = sorted({w[:5] for c in CTX for w in re.findall(r"[a-z]+", cx[c].lower())
                         if len(w) >= 4 and w not in STOP})
        for c in CTX:
            for p in ["GP", "CUE", "NB", "NC"]:
                line = {"family_id": fid, "cond": f"{c}:{p}", "prime": f"{cx[c]} {P[p]}",
                        "extra_stems": [n["intr_verb"][:5]] + cstems}
                if p == "GP":
                    k = cx[c] + " "
                    line["probes"] = [[k + head, " the", "V_the"], [k + head, ",", "V_comma"],
                                      [k + f"{head} {f['np']}", w1, "GP_dis"], [k + f"{head}, {f['np']}", w1, "CUE_dis"],
                                      [k + nhead, " the", "NV_the"], [k + nhead, ",", "NV_comma"]]
                fo.write(json.dumps(line) + "\n")
                n_out += 1
print(f"wrote {OUT.relative_to(ROOT)}: {n_out} lines, dropped families {n_drop}")
