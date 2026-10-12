"""E008 materials: MV/RR prime families (Amouyal 40 + SAP 24).

  GP : The chef hired last month worked overtime.            (reduced relative; initial main-verb analysis destroyed)
  CUE: The chef which was hired last month worked overtime.  (author's unreduced control, verbatim relativizer)
  NB : The chef chosen last month worked overtime.           (irregular participle: no main-verb analysis)
  NC : The chef which was chosen last month worked overtime.
Participle assignment is by verb meaning class, fixed before any scoring:
  ditransitive SAP verbs -> given; selection verbs -> chosen; all others -> seen.
"""
import csv
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
UP = ROOT / "data/gp_behavior/upstream"
OUT = ROOT / "data/gp_behavior/derived/mvrr_prime_families_v1.jsonl"
SELECT = {"hired", "selected", "appointed", "nominated", "promoted", "elected", "commissioned", "dispatched",
          "recruited", "chosen", "drafted", "assigned", "named", "picked", "enlisted", "employed", "sponsored",
          "admitted", "accepted", "invited", "awarded"}
STOP = set("a an the that which who was were is are be been had has it its they he she his her their him them of to in on at with from for by up off down over into out about so than then this last".split())


def stems(*texts):
    return sorted({w[:5] for t in texts for w in re.findall(r"[A-Za-z]+", t.lower()) if w not in STOP and len(w) >= 3})


def family(fid, src, np_, verb, amb_rest, rel, main, ditrans):
    part = "given" if ditrans else ("chosen" if verb.lower() in SELECT else "seen")
    tail = f" {amb_rest}" if amb_rest else ""
    dis = main.split()[0]
    return {
        "family_id": fid, "source": src, "construction": "MVRR", "np": np_, "verb": verb, "amb_rest": amb_rest,
        "rel": rel, "main": main, "intr_verb": part,
        "primes": {"GP": f"{np_} {verb}{tail} {main}.", "CUE": f"{np_} {rel} {verb}{tail} {main}.",
                   "NB": f"{np_} {part}{tail} {main}.", "NC": f"{np_} {rel} {part}{tail} {main}."},
        "D_ctx": f"{np_} {verb}{tail}", "Dc_ctx": f"{np_} {rel} {verb}{tail}", "D_word": " " + dis,
        "verb_ctx": f"{np_} {verb}",
        "content_stems": stems(np_, verb, amb_rest, main),
    }


def amouyal():
    rows = list(csv.DictReader(open(UP / "amouyal/reduced_relative_human_base_data.csv")))
    fam = {}
    for x in rows:
        fam.setdefault(x["set_id"].split("_")[0], {})[x["sent_type"]] = x
    out = []
    for sid, v in fam.items():
        gp = next(x for t, x in v.items() if "non" not in t)
        cue = next(x for t, x in v.items() if "non" in t)["sentence"].strip().rstrip(".")
        # derive structure from GP/control word alignment (upstream gp_verb has typos, e.g. 'instrcuted')
        s = gp["sentence"].strip().rstrip(".")
        gw, cw = s.split(), cue.split()
        i = next(k for k in range(len(gw)) if gw[k] != cw[k])      # first divergence = start of relativizer
        np_, verb = " ".join(gw[:i]), gw[i]
        rel = " ".join(cw[i: cw.index(verb, i)])
        rest = gw[i + 1:]
        dis = gp["reduced_verb"].split()[0]
        if sid == "s37":  # upstream marks 'pleased'; the disambiguating word is 'was' (ditransitive RR)
            dis = "was"
        j = next(k for k, w in enumerate(rest) if w.lower().startswith(dis.lower()))
        amb_rest, main = " ".join(rest[:j]), " ".join(rest[j:])
        out.append(family(f"amouyal_rr:{sid}", "amouyal", np_, verb, amb_rest, rel, main, ditrans=(sid == "s37")))
    return out


def sap():
    x = pd.read_excel(UP / "sap/Items_for_all_subsets.xlsx", sheet_name="NPSNPZMVRR")
    x = x[x.condition == "MVRR_UAMB"]
    out = []
    for _, r in x.iterrows():
        amb, cue = r["ambiguous"].strip().rstrip("."), str(r["Unnamed: 3"]).strip().rstrip(".")
        w = amb.split()
        dis = int(r["disambPositionAmb"])
        rel = "who was"
        np_ = cue[: cue.index(" who was ")]
        nnp = len(np_.split())
        verb = w[nnp]
        amb_rest = " ".join(w[nnp + 1: dis - 1])
        main = " ".join(w[dis - 1:])
        out.append(family(f"sap_rr:{int(r['item'])}", "sap", np_, verb, amb_rest, rel, main, ditrans=True))
    return out


def main():
    fams = amouyal() + sap()
    with open(OUT, "w") as fo:
        for f in fams:
            fo.write(json.dumps(f) + "\n")
    print(len(fams), "->", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
