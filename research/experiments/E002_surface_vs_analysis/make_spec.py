"""Write the E002 condition spec (see README for the logic)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
fams = [json.loads(l) for l in open(ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl")]
intr = {json.loads(l)["family_id"]: json.loads(l) for l in open(ROOT / "data/gp_behavior/derived/npz_intransitive_controls_v1.jsonl")}
OUT = ROOT / "research/experiments/E002_surface_vs_analysis/spec.jsonl"

with open(OUT, "w") as fo:
    for f in fams:
        p = dict(f["primes"])
        n = intr[f["family_id"]]
        p["NB"], p["NC"] = n["primes"]["NB"], n["primes"]["NC"]
        head = f"{f['subord']} {f['subj_v']}"
        nhead = f"{f['subord']} {n['subj']} {n['intr_verb']}"
        w1 = " " + f["rest"].split()[0]
        conds = {
            "NONE": "", "GP": p["GP"], "CUE": p["CUE"], "TB": p["TB"], "TC": p["TC"],
            "NB": p["NB"], "NC": p["NC"],
            "CUE>CUE": f"{p['CUE']} {p['CUE']}", "GP>CUE": f"{p['GP']} {p['CUE']}",
            "TB>CUE": f"{p['TB']} {p['CUE']}", "TC>CUE": f"{p['TC']} {p['CUE']}",
            "CUE>GP": f"{p['CUE']} {p['GP']}", "CUE>TB": f"{p['CUE']} {p['TB']}",
            "CUE>TC": f"{p['CUE']} {p['TC']}",
        }
        for c, text in conds.items():
            line = {"family_id": f["family_id"], "cond": c, "prime": text,
                    "extra_stems": [n["intr_verb"][:5]]}
            if c == "NONE":  # prime-internal probes stored once per family
                line["probes"] = [
                    [f"{head} {f['np']}", w1, "GP_dis"],
                    [f"{head}, {f['np']}", w1, "CUE_dis"],
                    [f"{nhead} {f['np']}", w1, "NB_dis"],
                    [f"{nhead}, {f['np']}", w1, "NC_dis"],
                    [f"{p['CUE']} {head} {f['np']}", w1, "GPafterCUE_dis"],
                    [f"{p['CUE']} {head}, {f['np']}", w1, "CUEafterCUE_dis"],
                    [head, " the", "V_the"], [head, ",", "V_comma"],
                    [f"{p['CUE']} {head}", " the", "V_the_afterCUE"], [f"{p['CUE']} {head}", ",", "V_comma_afterCUE"],
                    [nhead, " the", "NV_the"], [nhead, ",", "NV_comma"],
                ]
            fo.write(json.dumps(line) + "\n")
print("wrote", OUT.relative_to(ROOT))
