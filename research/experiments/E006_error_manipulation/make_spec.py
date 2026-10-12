"""E006 spec from rated variants (inclusion rule in README)."""
import hashlib, json
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
fams = {json.loads(l)["family_id"]: json.loads(l) for l in open(ROOT / "data/gp_behavior/derived/npz_prime_families_v1.jsonl")}
intr = {json.loads(l)["family_id"]: json.loads(l) for l in open(ROOT / "data/gp_behavior/derived/npz_intransitive_controls_v1.jsonl")}
V = defaultdict(list)
for l in open(ROOT / "data/gp_behavior/derived/e006_variants_v1.jsonl"):
    r = json.loads(l)
    if r["is_original"] or r["naturalness_llama31_8b"] >= 3.0:
        V[r["family_id"]].append(r)
V = {k: v for k, v in V.items() if len(v) >= 3}
targets = sorted(fams, key=lambda f: hashlib.sha256(f.encode()).hexdigest())[:45]
json.dump(targets, open(Path(__file__).with_name("targets.json"), "w"), indent=0)
n = 0
with open(Path(__file__).with_name("spec.jsonl"), "w") as fo:
    for fid, vs in V.items():
        f, nb = fams[fid], intr[fid]
        head = f"{f['subord']} {f['subj_v']}"; nhead = f"{f['subord']} {nb['subj']} {nb['intr_verb']}"
        for r in vs:
            k, rest = r["variant"], r["rest"]
            w1 = " " + rest.split()[0]
            cells = {"GP": f"{head} {f['np']} {rest}.", "CUE": f"{head}, {f['np']} {rest}.",
                     "NB": f"{nhead} {f['np']} {rest}.", "NC": f"{nhead}, {f['np']} {rest}."}
            for c, text in cells.items():
                line = {"family_id": fid, "cond": f"{c}#{k}", "prime": text, "extra_stems": [nb["intr_verb"][:5]]}
                if c == "GP":
                    line["probes"] = [[f"{head} {f['np']}", w1, f"GP_dis#{k}"], [f"{head}, {f['np']}", w1, f"CUE_dis#{k}"],
                                      [f"{head} {f['np']}", " " + rest + ".", f"GP_cont#{k}"],
                                      [f"{head}, {f['np']}", " " + rest + ".", f"CUE_cont#{k}"]]
                fo.write(json.dumps(line) + "\n"); n += 1
print(len(V), "families,", sum(len(v) for v in V.values()), "variants,", n, "spec lines")
