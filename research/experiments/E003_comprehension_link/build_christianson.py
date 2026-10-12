"""Parse Christianson et al. (2001) appendices into structured families.

OT (optionally transitive, Appendix 1, 42 items):
  subord, subj_v, alt_obj, np, rc, rest_plaus, rest_implaus, q_obs, q_final (Exp.2; items 1-40)
RAT (reflexive absolute transitive, Appendix 2, 12 items): subord, subj_v, np, rc, rest, q_obs
Output: data/gp_behavior/derived/christianson2001_families_v1.jsonl
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "data/gp_behavior/upstream/christianson2001/appendix_pdftotext.txt"
OUT = ROOT / "data/gp_behavior/derived/christianson2001_families_v1.jsonl"


def blocks(text):
    text = re.sub(r"(\w)- \n\s*(\w)", r"\1\2", text)  # line-final hyphenation
    lines = [l.strip() for l in text.splitlines()]
    out, cur = [], None
    for l in lines:
        m = re.match(r"^(\d+)\.\s+(.*)$", l)
        if m:
            if cur:
                out.append(cur)
            cur = [int(m.group(1)), m.group(2)]
        elif cur and l:
            cur[1] += " " + l
    if cur:
        out.append(cur)
    return [(n, re.sub(r"(\w)- (\w)", r"\1\2", re.sub(r"\s+", " ", t)).strip()) for n, t in out]


def main():
    raw = SRC.read_text()
    a1, rest = raw.split("Matrix clause questions for Experiment 2")
    a1q, a2 = rest.split("APPENDIX 2")
    fams = []
    finals = {n: t for n, t in blocks(a1q)}
    pat = re.compile(r"^(While|As) (.+?) \((.+?)\) (.+?) \((that (?:was|were) .+?)\) (.+?)/(.+?) (Did .+?\??)$")
    for n, t in blocks(a1.split("Experimental sentences for Experiments 1a and 1b")[1]):
        m = pat.match(t)
        assert m, (n, t)
        sub, sv, alt, np, rc, rp, ri, q = m.groups()
        fams.append({"family_id": f"chr2001:ot{n}", "verb_class": "OT", "subord": sub, "subj_v": sv,
                     "alt_obj": alt, "np": np, "rc": rc, "rest_plaus": rp.strip(), "rest_implaus": ri.strip(),
                     "q_obs": q if q.endswith("?") else q + "?", "q_final": finals.get(n)})
    items = blocks(a2[a2.index("1. While Jim"):])
    for n, t in items:
        # "While Jim bathed the child that was blond and pudgy giggled with delight <reordered> Did Jim bathe the child?"
        gp, q = re.match(r"^(While .+?) The .+? (Did .+\?)$", t).groups()
        m = re.match(r"^While (.+?) (the \w+) (that (?:was|were) \w+ and \w+) (.+)$", gp)
        assert m, (n, gp)
        sv, np, rc, rest = m.groups()
        fams.append({"family_id": f"chr2001:rat{n}", "verb_class": "RAT", "subord": "While", "subj_v": sv,
                     "alt_obj": None, "np": np, "rc": rc, "rest_plaus": rest.strip(), "rest_implaus": None,
                     "q_obs": q, "q_final": None})
    with open(OUT, "w") as f:
        for r in fams:
            f.write(json.dumps(r) + "\n")
    print(len(fams), "->", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
