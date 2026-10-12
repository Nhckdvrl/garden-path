import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
fams = [json.loads(l) for l in open(ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl")]
intr = {json.loads(l)["family_id"]: json.loads(l) for l in open(ROOT / "data/gp_behavior/derived/npz_intransitive_controls_v1.jsonl")}
PART = {"off", "up", "down"}
# past != participle: passive would be ungrammatical or change the GP substring -> excluded (rule fixed before scoring)
IRREG = {"rode", "drew", "drank", "ate", "wrote", "woke", "grew", "shrank", "broke", "hid", "began"}
with open(Path(__file__).with_name("spec.jsonl"), "w") as fo:
    for f in fams:
        w = f["subj_v"].split()
        k = len(w) - (2 if w[-1] in PART else 1)
        subj, vp = " ".join(w[:k]), " ".join(w[k:])
        if w[k].lower() in IRREG:
            continue
        aux = "were" if subj.split()[-1].lower().endswith("s") and subj.split()[-1].lower() not in {"jus"} else "was"
        head = f"{f['subord']} {subj} {aux} {vp}"
        w1 = " " + f["rest"].split()[0]
        cells = {"PASS_B": f"{head} {f['np']} {f['rest']}.", "PASS_C": f"{head}, {f['np']} {f['rest']}."}
        n = intr[f["family_id"]]
        for c, text in cells.items():
            line = {"family_id": f["family_id"], "cond": c, "prime": text, "extra_stems": [n["intr_verb"][:5]]}
            if c == "PASS_B":
                line["probes"] = [[f"{head} {f['np']}", w1, "PB_dis"], [f"{head}, {f['np']}", w1, "PC_dis"]]
            fo.write(json.dumps(line) + "\n")
print("ok")
