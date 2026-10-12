import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
fams = [json.loads(l) for l in open(ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl")]
intr = {json.loads(l)["family_id"]: json.loads(l) for l in open(ROOT / "data/gp_behavior/derived/npz_intransitive_controls_v1.jsonl")}
with open(Path(__file__).with_name("spec.jsonl"), "w") as fo:
    for f in fams:
        n = intr[f["family_id"]]
        head = f"{f['subord']} {f['subj_v']}"; nhead = f"{f['subord']} {n['subj']} {n['intr_verb']}"
        cells = {"GP": f"{head} {f['np']} {f['rest']}.", "NOM": f"{head} they {f['rest']}.",
                 "NB": f"{nhead} {f['np']} {f['rest']}.", "NBNOM": f"{nhead} they {f['rest']}."}
        w1 = " " + f["rest"].split()[0]
        for c, text in cells.items():
            line = {"family_id": f["family_id"], "cond": c, "prime": text, "extra_stems": [n["intr_verb"][:5]]}
            if c == "GP":
                line["probes"] = [[f"{head} {f['np']}", w1, "GP_dis"], [f"{head}, {f['np']}", w1, "CUE_dis"],
                                  [head, " the", "V_the"], [head, ",", "V_comma"], [head, " they", "V_they"]]
            fo.write(json.dumps(line) + "\n")
print("ok")
