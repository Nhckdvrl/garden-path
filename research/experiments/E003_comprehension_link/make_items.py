"""E003 v2: build sentence cells, comprehension prompts and priming primes from Christianson 2001.

Writes
  data/gp_behavior/derived/e003_cells_v2.jsonl   one line per family x form x length x plausibility
                                                 (sentence text + probe strings)
Comprehension prompt construction and priming target pairing happen in run_v2.py.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FAM = ROOT / "data/gp_behavior/derived/christianson2001_families_v1.jsonl"
OUT = ROOT / "data/gp_behavior/derived/e003_cells_v2.jsonl"

PLURAL = {"notes", "balls", "drapes", "children", "baboons", "students"}
HUMAN = {"child", "challenger", "model", "actor", "opponent", "enemy", "baby", "neighbor", "patient"}
PARTICLES = {"off", "up", "down"}
POOL = ["slept", "yawned", "sneezed", "laughed", "sighed", "snored", "napped",
        "shivered", "dozed", "frowned", "giggled", "rested"]
STOP = set("""a an the while when after before because although once as and of to in on at with from
for by up off down over into toward is was were be been it its they he she his her their him them
that this there out about so than then did""".split())


def stems(*texts):
    return sorted({w[:5] for t in texts for w in re.findall(r"[a-z]+", t.lower()) if w not in STOP and len(w) >= 3})


def pron(np):
    h = np.split()[-1].lower()
    return "they" if h in PLURAL or h in HUMAN else "it"


def subj_of(sv):
    w = sv.split()
    return " ".join(w[:-2] if w[-1] in PARTICLES else w[:-1])


def cap(s):
    return s[0].upper() + s[1:]


def main():
    fams = [json.loads(l) for l in open(FAM)]
    out = []
    k = 0
    for f in fams:
        intr = POOL[k % len(POOL)]
        k += 1
        sub, sv, np, pr = f["subord"], f["subj_v"], f["np"], pron(f["np"])
        subj = subj_of(sv)
        verb = sv[len(subj):].strip()
        for L in ("S", "L"):
            npx = np if L == "S" else f"{np} {f['rc']}"
            for P in (("P", "I") if f["rest_implaus"] else ("P",)):
                rest = f["rest_plaus"] if P == "P" else f["rest_implaus"]
                forms = {
                    "GP": f"{sub} {sv} {npx} {rest}.",
                    "CUE": f"{sub} {sv}, {npx} {rest}.",
                    "TB": f"{sub} {sv} {npx} {pr} {rest}.",
                    "TC": f"{sub} {sv} {npx}, {pr} {rest}.",
                    "NB": f"{sub} {subj} {intr} {npx} {rest}.",
                    "NC": f"{sub} {subj} {intr}, {npx} {rest}.",
                    "REORD": f"{cap(npx)} {rest} {sub.lower()} {sv}.",
                }
                if f["alt_obj"]:
                    forms["CTL"] = f"{sub} {sv} {f['alt_obj']} {npx} {rest}."
                w1 = " " + rest.split()[0]
                # prime-internal probes: disambiguating word after the ambiguous NP region
                probes = {"GP_dis": [f"{sub} {sv} {npx}", w1], "CUE_dis": [f"{sub} {sv}, {npx}", w1],
                          "NB_dis": [f"{sub} {subj} {intr} {npx}", w1], "NC_dis": [f"{sub} {subj} {intr}, {npx}", w1],
                          "V_the": [f"{sub} {sv}", " " + np.split()[0]], "V_comma": [f"{sub} {sv}", ","]}
                if f["alt_obj"]:
                    probes["CTL_dis"] = [f"{sub} {sv} {f['alt_obj']} {npx}", w1]
                out.append({
                    "family_id": f["family_id"], "verb_class": f["verb_class"], "length": L, "plaus": P,
                    "forms": forms, "probes": probes,
                    "q": {"OBS_author": f["q_obs"], "FINAL_author": f["q_final"] if P == "P" else None,
                          "OBS_template": f"Is it true that {sv} {np}?",
                          "FINAL_template": f"Is it true that {npx} {rest}?"},
                    "intr_verb": intr,
                    "content_stems": stems(sv, np, f["rc"], f["rest_plaus"], f["rest_implaus"] or "", f["alt_obj"] or "", intr),
                })
    with open(OUT, "w") as fo:
        for r in out:
            fo.write(json.dumps(r) + "\n")
    print(len(out), "cells ->", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
