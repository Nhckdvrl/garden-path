"""E007 materials: NP/S prime families (Amouyal 40 + SAP 24) in the generic family format.

  GP : The student forgot the solution was in the back of the book.
  CUE: The student forgot that the solution was in the back of the book.
  NB : The student hoped the solution was in the back of the book.      (S-complement-only verb: no object analysis)
  NC : The student hoped that the solution was in the back of the book.
  TB : The student forgot the solution which was in the back of the book. (true object + relative clause; no 'that')
Target fields (for prime_run --target_fams): D_ctx/Dc_ctx/D_word = GP/that-version context and disambiguating word.
Probe fields: verb_ctx (subject + verb) for object expectation log P(" the") - log P(" that").
"""
import csv
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
UP = ROOT / "data/gp_behavior/upstream"
OUT = ROOT / "data/gp_behavior/derived/nps_prime_families_v1.jsonl"
S_ONLY = ["hoped", "thought", "insisted", "pretended", "wished", "boasted", "reckoned", "complained"]
HUMAN = {"player", "murderer", "visitor", "model", "suspect", "chicken", "lamb"}  # 'who' for animate-human-ish
HUMAN -= {"chicken", "lamb"}
STOP = set("a an the that this these those was were is are be been had has it its they he she his her their him them of to in on at with from for by up off down over into out about so than then".split())


def stems(*texts):
    return sorted({w[:5] for t in texts for w in re.findall(r"[A-Za-z]+", t.lower()) if w not in STOP and len(w) >= 3})


def family(fid, src, sv, np_, rest, k):
    disamb = rest.split()[0]
    head = np_.split()[-1].lower()
    rel = "who" if head in HUMAN else "which"
    subj = " ".join(sv.split()[:-1])
    nb = S_ONLY[k % len(S_ONLY)]
    return {
        "family_id": fid, "source": src, "construction": "NPS", "sv": sv, "np": np_, "rest": rest,
        "intr_verb": nb, "subj": subj,
        "primes": {"GP": f"{sv} {np_} {rest}.", "CUE": f"{sv} that {np_} {rest}.",
                   "NB": f"{subj} {nb} {np_} {rest}.", "NC": f"{subj} {nb} that {np_} {rest}.",
                   "TB": f"{sv} {np_} {rel} {rest}."},
        "D_ctx": f"{sv} {np_}", "Dc_ctx": f"{sv} that {np_}", "D_word": " " + disamb,
        "verb_ctx": sv, "nverb_ctx": f"{subj} {nb}",
        "content_stems": stems(sv, np_, rest),
    }


def amouyal():
    rows = list(csv.DictReader(open(UP / "amouyal/nps_human_base_data.csv")))
    fam = {}
    for x in rows:
        fam.setdefault(x["set_id"].split("_")[0], {})[x["sent_type"]] = (x["sentence"].strip(), x["reduced_verb"])
    out = []
    for k, (sid, v) in enumerate(fam.items()):
        gp, dis = v["nps_gp"]
        cue, _ = v["nps_nongp"]
        sv = cue.split(" that ")[0]
        rem = gp[len(sv) + 1:].rstrip(".").split()
        j = rem.index(dis)
        out.append(family(f"amouyal_nps:{sid}", "amouyal", sv, " ".join(rem[:j]), " ".join(rem[j:]), k))
    return out


def sap(k0):
    x = pd.read_excel(UP / "sap/Items_for_all_subsets.xlsx", sheet_name="NPSNPZMVRR")
    x = x[x.condition == "NPS_UAMB"]
    out = []
    for k, (_, r) in enumerate(x.iterrows()):
        amb = r["ambiguous"].strip().rstrip(".")
        cue = str(r["Unnamed: 3"]).strip()
        sv = cue.split(" that ")[0]
        w = amb.split()
        dis = int(r["disambPositionAmb"])  # 1-based index of disambiguating word
        nsv = len(sv.split())
        out.append(family(f"sap_nps:{int(r['item'])}", "sap", sv, " ".join(w[nsv:dis - 1]), " ".join(w[dis - 1:]), k0 + k))
    return out


def main():
    fams = amouyal()
    fams += sap(len(fams))
    with open(OUT, "w") as fo:
        for f in fams:
            fo.write(json.dumps(f) + "\n")
    print(len(fams), "->", OUT.relative_to(ROOT))
    for f in fams[:3] + fams[40:42]:
        print(" ", " | ".join(f["primes"][c] for c in ("GP", "NB", "TB")))


if __name__ == "__main__":
    main()
