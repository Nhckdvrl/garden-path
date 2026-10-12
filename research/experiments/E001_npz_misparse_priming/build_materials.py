"""Build NP/Z prime families for E001 from pinned published sources.

Sources (immutable bytes under data/gp_behavior/upstream/):
  * Amouyal et al. NP/Z (69 families; 'While SUBJ V NP VP.')
  * SAP benchmark NP/Z (Huang et al. 2024; 24 families, author comma controls)

Every family is decomposed into  SUBORD | SUBJ_V | NP | REST  so that the
four prime conditions differ only by a comma and (for transitive-final
primes) a resumptive pronoun:

  GP  : While the man hunted the deer ran into the woods.          (final: V intransitive; temporarily transitive)
  CUE : While the man hunted, the deer ran into the woods.         (final: V intransitive; comma blocks object reading)
  TB  : While the man hunted the deer it ran into the woods.       (final: V transitive; no comma)
  TC  : While the man hunted the deer, it ran into the woods.      (final: V transitive; comma)
  MAIN: The deer ran into the woods.                               (no subordinate clause; neutral baseline)

Targets for family j are two prefixes with identical words that differ only in
comma placement:
  T_j : While the man hunted the deer,     (NP attached as object  -> transitive)
  I_j : While the man hunted, the deer     (NP starts main clause -> intransitive)

Output: data/gp_behavior/derived/npz_prime_families_v1.jsonl
"""
import csv
import json
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
UP = ROOT / "data/gp_behavior/upstream"
OUT = ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl"

# Multi-word NP heads the determiner+1-word heuristic gets wrong.
NP_FIX = {"amouyal:set_13": "the hot dog"}
PLURAL = {"children", "students", "tomatoes", "balls", "baboons", "athletes"}
HUMAN = {"challenger", "dancer", "opponent", "enemy", "child", "neighbor", "baby",
         "patient", "team"}
STOP = set("""a an the while when after before because although once as and of to in on
at with from for by up off down over into toward is was were be been it its they he she
his her their him them that this there out about so than then""".split())


def pronoun(np: str) -> str:
    head = np.split()[-1].lower()
    if head in PLURAL or head in HUMAN:
        return "they"
    return "it"


def stems(*texts):
    out = set()
    for t in texts:
        for w in re.findall(r"[A-Za-z]+", t.lower()):
            if w in STOP or len(w) < 3:
                continue
            out.add(w[:5])
    return out


def family(fid, source, subord, subj_v, np, rest, author_cue=None, note=""):
    lc = lambda s: s[0].lower() + s[1:]
    np = lc(np)
    pr = pronoun(np)
    head = f"{subord} {subj_v}"
    cond = {
        "GP": f"{head} {np} {rest}.",
        "CUE": f"{head}, {np} {rest}.",
        "TB": f"{head} {np} {pr} {rest}.",
        "TC": f"{head} {np}, {pr} {rest}.",
        "MAIN": f"{np[0].upper() + np[1:]} {rest}.",
    }
    return {
        "family_id": fid, "source": source, "subord": subord, "subj_v": subj_v,
        "np": np, "rest": rest, "pronoun": pr, "primes": cond,
        "target_T": f"{head} {np},", "target_I": f"{head}, {np}",
        "content_stems": sorted(stems(subj_v, np, rest)),
        "author_cue": author_cue, "author_cue_matches": (author_cue == cond["CUE"]) if author_cue else None,
        "note": note,
    }


def amouyal():
    rows = list(csv.DictReader(open(UP / "amouyal/extended_gardenpath_experiments.csv")))
    fam = {}
    for x in rows:
        fam.setdefault(x["set_id"], {})[x["sent_type"]] = x["sentence"].strip()
    out = []
    for sid, v in fam.items():
        gp = next(s for t, s in v.items() if t.startswith("GP"))
        ng = next(s for t, s in v.items() if t.startswith("nonGP"))
        main, sub = re.split(r" while ", ng.rstrip("."), maxsplit=1)
        assert gp.startswith("While "), gp
        body = gp[len("While "):].rstrip(".")
        subj_v = body[: len(sub)]
        assert subj_v.lower() == sub.lower(), (sid, subj_v, sub)
        fid = f"amouyal:{sid}"
        w = main.split()
        np = NP_FIX.get(fid) or (" ".join(w[:2]) if w[0].lower() in ("the", "a") else w[0])
        rest = main[len(np):].strip()
        assert main.lower().startswith(np.lower())
        kind = "reflexive_absolute" if "hyp5" in sid else "optionally_transitive"
        out.append(family(fid, "amouyal", "While", subj_v, np, rest, note=kind))
    return out


def sap():
    x = pd.read_excel(UP / "sap/Items_for_all_subsets.xlsx", sheet_name="NPSNPZMVRR")
    x = x[x.condition.astype(str).str.contains("NPZ")]
    out = []
    for _, r in x.iterrows():
        amb, cue = r["ambiguous"].strip(), str(r["Unnamed: 3"]).strip()
        words = amb.rstrip(".").split()
        dis = int(r["disambPositionAmb"])  # 1-based index of disambiguating verb
        # comma position from author cue
        cw = cue.split()
        k = next(i for i, w in enumerate(cw) if w.endswith(","))
        subord = words[0]
        subj_v = " ".join(words[1 : k + 1])
        np = " ".join(words[k + 1 : dis - 1])
        rest = " ".join(words[dis - 1 :])
        assert f"{subord} {subj_v} {np} {rest}." == amb, (amb,)
        out.append(family(f"sap:npz{int(r['item'])}", "sap", subord, subj_v, np, rest,
                          author_cue=cue, note="optionally_transitive"))
    return out


def main():
    fams = amouyal() + sap()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        for r in fams:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{len(fams)} families -> {OUT.relative_to(ROOT)}", file=sys.stderr)
    for r in fams:
        if r["author_cue_matches"] is False:
            print("author cue differs:", r["family_id"], "|", r["author_cue"], file=sys.stderr)


if __name__ == "__main__":
    main()
