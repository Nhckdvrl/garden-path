"""E004 spec: exact-repetition primes (X>X) plus second-copy manipulation probes."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
fams = [json.loads(l) for l in open(ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl")]
intr = {json.loads(l)["family_id"]: json.loads(l) for l in open(ROOT / "data/gp_behavior/derived/npz_intransitive_controls_v1.jsonl")}
OUT = ROOT / "research/experiments/E004_repetition_history/spec.jsonl"
with open(OUT, "w") as fo:
    for f in fams:
        n = intr[f["family_id"]]
        p = dict(f["primes"]); p.update(n["primes"])
        head = f"{f['subord']} {f['subj_v']}"; nhead = f"{f['subord']} {n['subj']} {n['intr_verb']}"
        w1 = " " + f["rest"].split()[0]
        for c in ["GP", "CUE", "TB", "NB", "NC"]:
            line = {"family_id": f["family_id"], "cond": f"{c}>{c}", "prime": f"{p[c]} {p[c]}",
                    "extra_stems": [n["intr_verb"][:5]]}
            if c == "GP":
                line["probes"] = [
                    [f"{p['GP']} {head} {f['np']}", w1, "GP2_dis"],
                    [f"{p['CUE']} {head}, {f['np']}", w1, "CUE2_dis"],
                    [f"{p['NB']} {nhead} {f['np']}", w1, "NB2_dis"],
                    [f"{p['NC']} {nhead}, {f['np']}", w1, "NC2_dis"],
                    [f"{p['GP']} {head}", " the", "V_the_afterGP"], [f"{p['GP']} {head}", ",", "V_comma_afterGP"],
                ]
            fo.write(json.dumps(line) + "\n")
print("wrote", OUT.relative_to(ROOT))
