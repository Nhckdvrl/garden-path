"""Gold validation of transitivity.classify on material sentences with known final structure."""
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research/tools"))
from transitivity import classify  # noqa: E402

fams = [json.loads(l) for l in open(ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl")]
intr = {json.loads(l)["family_id"]: json.loads(l) for l in open(ROOT / "data/gp_behavior/derived/npz_intransitive_controls_v1.jsonl")}
cells = [json.loads(l) for l in open(ROOT / "data/gp_behavior/derived/e003_cells_v2.jsonl")]
gold = {"GP": "INTR", "CUE": "INTR", "TB": "TRANS", "TC": "TRANS"}
res, errs = collections.Counter(), []


def check(tag, pre, sent, g):
    r = classify(pre, sent[len(pre):])
    res[(tag, r["cls"])] += 1
    if r["cls"] != g:
        errs.append((tag, sent, r["cls"]))


for f in fams:
    pre = f"{f['subord']} {f['subj_v']}"
    for c, g in gold.items():
        check("npz_" + c, pre, f["primes"][c], g)
    n = intr[f["family_id"]]
    npre = f"{f['subord']} {n['subj']} {n['intr_verb']}"
    check("npz_NB", npre, n["primes"]["NB"], "INTR")
for c in cells:  # Christianson short forms (long ones contain a relative clause -> AMBIG by design)
    if c["length"] != "S":
        continue
    gp = c["forms"]["GP"]
    pre = gp[: gp.index(" " + c["forms"]["CUE"].split(", ")[1].split()[0] + " ")] if False else None
    sv = c["forms"]["CUE"].split(",")[0]
    for form, g in (("GP", "INTR"), ("TC", "TRANS"), ("TB", "TRANS")) + ((("CTL", "TRANS"),) if "CTL" in c["forms"] else ()):
        check("chr_" + form, sv, c["forms"][form], g)
for k, v in sorted(res.items()):
    print(k, v)
print(len(errs), "errors")
for e in errs:
    print(e)
