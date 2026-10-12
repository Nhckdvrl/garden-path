"""E002 materials: strictly intransitive-verb controls for the E001 NP/Z families.

For every E001 family, replace the subordinate verb by a verb that does not take
a direct object, keeping subject, NP and continuation:
  NB : While the man slept the deer ran into the woods.   (adjacency 'V the N', no object analysis)
  NC : While the man slept, the deer ran into the woods.
Verbs are assigned round-robin from a fixed pool (not chosen by model outcome);
inanimate subjects get a semantically compatible intransitive verb.
Output: data/gp_behavior/derived/npz_intransitive_controls_v1.jsonl
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl"
OUT = ROOT / "data/gp_behavior/derived/npz_intransitive_controls_v1.jsonl"

POOL = ["slept", "yawned", "sneezed", "laughed", "sighed", "snored", "napped",
        "shivered", "dozed", "frowned", "giggled", "rested"]
INANIMATE = {"ice cap": "glistened", "river": "glistened", "log": "smoldered",
             "match": "flickered", "wave": "receded"}
# subject = everything in subj_v except the final verb (+ particle)
PARTICLES = {"off", "up", "down"}


def split_subj(subj_v):
    w = subj_v.split()
    if w[-1] in PARTICLES:
        return " ".join(w[:-2])
    return " ".join(w[:-1])


def main():
    fams = [json.loads(l) for l in open(SRC)]
    out = []
    k = 0
    for f in fams:
        subj = split_subj(f["subj_v"])
        noun = subj.split()[-1].lower()
        key = next((n for n in INANIMATE if subj.lower().endswith(n)), None)
        if key:
            v = INANIMATE[key]
        else:
            v = POOL[k % len(POOL)]
            k += 1
        head = f"{f['subord']} {subj} {v}"
        out.append({
            "family_id": f["family_id"], "intr_verb": v, "subj": subj,
            "primes": {"NB": f"{head} {f['np']} {f['rest']}.", "NC": f"{head}, {f['np']} {f['rest']}."},
        })
    with open(OUT, "w") as fo:
        for r in out:
            fo.write(json.dumps(r) + "\n")
    print(len(out), "->", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
