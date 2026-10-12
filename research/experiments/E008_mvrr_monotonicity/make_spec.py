import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
with open(Path(__file__).with_name("spec.jsonl"), "w") as fo:
    for l in open(ROOT / "data/gp_behavior/derived/mvrr_prime_families_v1.jsonl"):
        f = json.loads(l)
        for c in ("GP", "CUE", "NB", "NC"):
            line = {"family_id": f["family_id"], "cond": c, "prime": f["primes"][c], "extra_stems": [f["intr_verb"][:5]]}
            if c == "GP":
                line["probes"] = [[f["D_ctx"], f["D_word"], "GP_dis"], [f["Dc_ctx"], f["D_word"], "CUE_dis"],
                                  [f["verb_ctx"], " the", "V_the"], [f["verb_ctx"], " a", "V_a"], [f["verb_ctx"], " by", "V_by"]]
            fo.write(json.dumps(line) + "\n")
print("ok")
