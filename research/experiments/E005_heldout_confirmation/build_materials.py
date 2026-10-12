"""Held-out NP/Z prime families for E005 (never used in E001/E002/E004 discovery).

Sources (immutable copies under data/gp_behavior/upstream/):
  * SyntaxGym npz_ambig (24 items; MIT): ambiguous verb vs author-chosen non-object verb x comma.
    NB/NC use the AUTHORS' unambiguous verb.
  * Ceháková & Chromý 2025 NP/Z (24 items; CC-BY-4.0): reflexive-absolute verbs, long NP
    (det N who/that was X). NB/NC use the E002 round-robin intransitive pool (new assignment).
Output: data/gp_behavior/derived/npz_heldout_v1.jsonl and the E005 spec.
"""
import importlib.util
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
UP = ROOT / "data/gp_behavior/upstream"
OUT = ROOT / "data/gp_behavior/derived/npz_heldout_v1.jsonl"
SPEC = Path(__file__).with_name("spec.jsonl")

spec = importlib.util.spec_from_file_location("b1", ROOT / "research/experiments/E001_npz_misparse_priming/build_materials.py")
b1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(b1)
b1.HUMAN |= {"woman", "doctor", "soldiers", "coach", "actor", "visitors", "nurse", "comedian", "children", "farmer",
             "teacher", "guards", "subjects", "thieves", "mother", "boy", "girl", "daughter", "nephew", "model",
             "boss", "husband", "grandmother", "queen", "businessman", "son", "child", "father", "man", "soldier",
             "uncle", "manager", "puppy", "toddler"}
b1.PLURAL |= {"soldiers", "visitors", "children", "guards", "subjects", "thieves", "waters"}
POOL = ["slept", "yawned", "sneezed", "laughed", "sighed", "snored", "napped",
        "shivered", "dozed", "frowned", "giggled", "rested"]
SUBORDS = ["As long as", "Though", "Because", "Before", "After", "While", "When", "As"]


def split_subord(s):
    for sub in SUBORDS:
        if s.startswith(sub + " "):
            return sub, s[len(sub) + 1:]
    raise ValueError(s)


def with_nb(fam, subj, intr):
    head = f"{fam['subord']} {subj} {intr}"
    fam["primes"]["NB"] = f"{head} {fam['np']} {fam['rest']}."
    fam["primes"]["NC"] = f"{head}, {fam['np']} {fam['rest']}."
    fam["intr_verb"], fam["subj"] = intr, subj
    fam["nhead"] = head
    fam["content_stems"] = sorted(set(fam["content_stems"]) | {intr[:5]})
    return fam


def syntaxgym():
    d = json.load(open(UP / "syntaxgym/npz_ambig.json"))
    out = []
    for k, it in enumerate(d["items"]):
        c = {x["condition_name"]: [r["content"].strip() for r in x["regions"]] for x in it["conditions"]}
        a, u = c["ambig_nocomma"], c["unambig_nocomma"]
        subord, subj = split_subord(a[0])
        rest = " ".join(x for x in a[4:] if x)
        f = b1.family(f"syntaxgym:npz{k+1}", "syntaxgym", subord, f"{subj} {a[1]}", a[3], rest, note="optionally_transitive")
        out.append(with_nb(f, subj, u[1]))
    return out


def cehakova():
    d = pd.read_csv(UP / "cehakova2025/exp_items.csv")
    d = d[d.condition == "NPZ-nongp-discor"]
    out = []
    for k, r in enumerate(d.itertuples()):
        s = r.sentence.rstrip(".")
        head, main = s.split(", ", 1)
        subord, sv = split_subord(head)
        w = main.split()
        np_, rest = " ".join(w[:5]), " ".join(w[5:])
        subj = " ".join(sv.split()[:-1])
        f = b1.family(f"cehakova2025:{r.item}", "cehakova2025", subord, sv, np_, rest, author_cue=r.sentence,
                      note="reflexive_absolute")
        # pronoun from the head noun (word 2), not the last word of the relative clause
        pr = b1.pronoun(" ".join(w[:2]))
        h = f"{subord} {sv}"
        f["pronoun"] = pr
        f["primes"]["TB"] = f"{h} {np_} {pr} {rest}."
        f["primes"]["TC"] = f"{h} {np_}, {pr} {rest}."
        out.append(with_nb(f, subj, POOL[k % len(POOL)]))
    return out


def main():
    fams = syntaxgym() + cehakova()
    disc = [json.loads(l) for l in open(ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl")]
    dverbs = {f["subj_v"].split()[-1].lower() for f in disc}
    with open(OUT, "w") as fo:
        for f in fams:
            f["verb_overlap_with_discovery"] = f["subj_v"].split()[-1].lower() in dverbs
            fo.write(json.dumps(f) + "\n")
    conds = ["GP", "CUE", "TB", "TC", "NB", "NC"]
    with open(SPEC, "w") as fo:
        for f in fams:
            p = f["primes"]
            head = f"{f['subord']} {f['subj_v']}"
            w1 = " " + f["rest"].split()[0]
            lines = [(c, p[c]) for c in conds] + [(f"{c}>{c}", f"{p[c]} {p[c]}") for c in ["GP", "CUE", "TB", "NB", "NC"]]
            for c, text in lines:
                line = {"family_id": f["family_id"], "cond": c, "prime": text}
                if c == "GP":
                    line["probes"] = [
                        [f"{head} {f['np']}", w1, "GP_dis"], [f"{head}, {f['np']}", w1, "CUE_dis"],
                        [f"{f['nhead']} {f['np']}", w1, "NB_dis"], [f"{f['nhead']}, {f['np']}", w1, "NC_dis"],
                        [head, " the", "V_the"], [head, ",", "V_comma"],
                        [f"{p['GP']} {head} {f['np']}", w1, "GP2_dis"], [f"{p['CUE']} {head}, {f['np']}", w1, "CUE2_dis"],
                    ]
                fo.write(json.dumps(line) + "\n")
    n_ov = sum(f["verb_overlap_with_discovery"] for f in fams)
    print(f"{len(fams)} held-out families ({n_ov} share a verb with discovery) -> {OUT.relative_to(ROOT)}")
    for f in fams[:2] + fams[24:26]:
        print(" ", f["primes"]["GP"], "|", f["primes"]["NB"], "|", f["primes"]["TC"])


if __name__ == "__main__":
    main()
