"""E003 materials: Yes/No comprehension items for the 69 Amouyal NP/Z families.

Each family: sentence in GP and CUE form (CUE = E001 comma-insertion version, NOT Amouyal's
reordered control) x two author-written questions:
  Q_OBS   'Did the secretary type the memo?'  obsolete relation (NOT_ENTAILED in both forms;
          the comprehension residue is the GP-minus-CUE shift, so no absolute truth label is needed)
  Q_FINAL 'Did the memo near completion?'     final relation (entailed in both forms)
Output: data/gp_behavior/derived/e003_comprehension_items_v1.jsonl
"""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
fams = {json.loads(l)["family_id"]: json.loads(l) for l in open(ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl")}
rows = list(csv.DictReader(open(ROOT / "data/gp_behavior/upstream/amouyal/extended_gardenpath_experiments.csv")))
qs = {}
for r in rows:
    if r["sent_type"].startswith("GP"):
        qs.setdefault(r["set_id"], {})["OBS" if r["quest_type"] == "GP_question" else "FINAL"] = r["question"].strip()
out = ROOT / "data/gp_behavior/derived/e003_comprehension_items_v1.jsonl"
n = 0
with open(out, "w") as f:
    for sid, q in qs.items():
        fam = fams[f"amouyal:{sid}"]
        for form in ("GP", "CUE"):
            for qt in ("OBS", "FINAL"):
                f.write(json.dumps({"family_id": fam["family_id"], "form": form, "qtype": qt,
                                    "sentence": fam["primes"][form], "question": q[qt]}) + "\n")
                n += 1
print(n, "items ->", out.relative_to(ROOT))
