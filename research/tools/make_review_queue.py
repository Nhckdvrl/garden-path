#!/usr/bin/env python3
"""Build a PRE-RESULT, construction-stratified, risk-prioritized review queue.

This uses published PENDING materials, not model correctness. High-risk families
and a seeded uniform sample are sent for independent source QA. This is a
review *schedule*, NOT a label audit and not acceptance of any sentence.

CLI: python3 research/tools/make_review_queue.py \
  --source data/gp_behavior/candidates --output /tmp/source_review_queue.jsonl
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import random
import re
from collections import defaultdict
from pathlib import Path

FILES = (
    "amouyal_extended_v0_pending.jsonl",
    "amouyal_nps_v0_pending.jsonl",
    "amouyal_rr_v0_pending.jsonl",
    "amouyal_npvp_v0_pending.jsonl",
)
# Only examples of observable source risks, not a proof of acceptability.
KNOWN_SUSPICIOUS = re.compile(
    r"\b(?:committe|burglers|boooks|had rode)\b", re.I
)
UNUSUAL_RELATIVE = re.compile(
    r"\b(?:who|which)\s+was\b", re.I
)

def read_pending(source: Path) -> list[dict]:
    rows=[]
    for n in FILES:
        p=source / n
        for line_no, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip(): continue
            row=json.loads(line)
            if row.get("review_status")!="PENDING" or row.get("usage_status")!="DISCOVERY_CANDIDATE_ONLY":
                raise ValueError(f"Only unreviewed source candidates may be queued: {p}:{line_no}")
            rows.append(row)
    return rows

def calculate_queue(rows: list[dict], fraction: float=.20, minimum: int=6,
                    seed: int=20261012) -> tuple[list[dict],dict]:
    if not 0 < fraction <= 1 or minimum < 0:
        raise ValueError("fraction in (0,1], minimum>=0 required")
    groups={}
    for r in rows:
        key=r["family_id"]
        d=groups.setdefault(key, {"construction":r["construction"],"rows":[]})
        if d["construction"]!=r["construction"]:
            raise ValueError(f"Mixed construction family {key}")
        d["rows"].append(r)
    strata=defaultdict(list)
    for fid,g in groups.items():
        if len(g["rows"])!=2 or {x["condition"] for x in g["rows"]}!={"GP","CUE"}:
            raise ValueError(f"Invalid GP/CUE source pair {fid}")
        strata[g["construction"]].append(fid)
    rng=random.Random(seed)
    picked=set()
    for construction in sorted(strata):
        all_f=sorted(strata[construction])
        n=min(len(all_f), max(minimum, math.ceil(len(all_f)*fraction)))
        picked.update(rng.sample(all_f, n))
    packet=[]
    for fid in sorted(groups):
        g=groups[fid]
        reasons=[]
        if fid in picked: reasons.append("STRATIFIED_RANDOM_QA")
        for r in g["rows"]:
            text=r["sentence"]
            if KNOWN_SUSPICIOUS.search(text):
                reasons.append("SUSPECT_SPELLING")
            if g["construction"]=="MVRR" and UNUSUAL_RELATIVE.search(text):
                reasons.append("RELATIVE_NATURALNESS_CHECK")
        reasons=sorted(set(reasons))
        if not reasons: continue
        conditions={r["condition"]:r for r in g["rows"]}
        packet.append({
            "family_id":fid, "construction":g["construction"],
            "selection_reasons":reasons,
            "review_status":"REQUESTED_NOT_COMPLETE",
            "original_sentences":{
                c:{"sentence":conditions[c]["sentence"],
                   "source_item_id":conditions[c]["source_item_id"],
                   "sha256":hashlib.sha256(conditions[c]["sentence"].encode("utf-8")).hexdigest(),
                   "source_question_candidates":[
                       {"relation_id":cl["relation_id"], "question":cl["question"],
                        "upstream_label":cl["upstream_correct_answer"]}
                       for cl in conditions[c]["gold_claims"]]}
                for c in ("GP","CUE")},
            "review_instructions":[
                "Check whether both printed sources are grammatical/natural",
                "Check exact parse and source-grounded truth of question",
                "Preserve authors' source label separately; not an entailment oracle",
                "No new Gold, no automatic modification or model-output-driven filtering"
            ]
        })
    summary={"seed":seed,"random_fraction":fraction,"minimum_per_construction":minimum,
             "total_families":len(groups),
             "random_families":len(picked),
             "queued_families":len(packet),
             "reason_counts":{}}
    for p in packet:
        for reason in p["selection_reasons"]:
            summary["reason_counts"][reason]=summary["reason_counts"].get(reason,0)+1
    return packet,summary

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--fraction",type=float,default=.20)
    parser.add_argument("--min-per-construction",type=int,default=6)
    parser.add_argument("--seed",type=int,default=20261012)
    args=parser.parse_args()
    rows=read_pending(args.source)
    packets,summary=calculate_queue(rows,args.fraction,args.min_per_construction,args.seed)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text("".join(json.dumps(p,ensure_ascii=False,sort_keys=True)+"\n" for p in packets),
                           encoding="utf-8")
    args.output.with_suffix(".summary.json").write_text(
        json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,sort_keys=True))
    print("Review queue only: no quality labels verified and no model evaluated.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
