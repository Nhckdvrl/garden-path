#!/usr/bin/env python3
"""Integrity-check ONE reviewed batch returned by an external model.

Does NOT accept/promote source gold into runnable manifests. Validate exact
input IDs/hashes and conservative review vocab; unresolved is valid uncertainty.

Usage: python3 research/tools/check_model_review.py \
  --request /tmp/opencode_review/gp_review_0001.json \
  --reply /tmp/opencode_response_0001.json
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ALLOWED_ACCEPT={"VALID","MARGINAL","INVALID","UNCERTAIN"}
ALLOWED_TRUTH={"ENTAILED","CONTRADICTED","NOT_ENTAILED","UNRESOLVED"}
ALLOWED_CONSTR={"NPZ","NPS","MVRR","NPVP","OTHER","UNCERTAIN"}
def verify(request:dict,response:dict)->dict:
    if response.get("batch_id")!=request.get("batch_id"):
        raise ValueError("Reply batch_id mismatch")
    raw=request.get("input_records")
    rows=response.get("records")
    if not isinstance(raw,list) or not isinstance(rows,list):
        raise ValueError("Request/reply records must be lists")
    expected={(x["family_id"],x["candidate_id"]):x for x in raw}
    if len(expected)!=len(raw):
        raise ValueError("Duplicate request ID")
    found={}
    for rec in rows:
        if not isinstance(rec,dict):
            raise ValueError("Malformed reply record")
        key=(rec.get("family_id"),rec.get("candidate_id"))
        if key in found or key not in expected:
            raise ValueError(f"Duplicate/unexpected response ID: {key}")
        if rec.get("source_sha256")!=expected[key]["source_sha256"]:
            raise ValueError(f"Source SHA mismatch: {key}")
        if rec.get("acceptability") not in ALLOWED_ACCEPT:
            raise ValueError(f"Bad acceptability {key}")
        if rec.get("construction") not in ALLOWED_CONSTR:
            raise ValueError(f"Bad syntax label {key}")
        claims=rec.get("claims")
        if not isinstance(claims,list):
            raise ValueError(f"No claim list for {key}")
        claim_ids={c["relation_id"] for c in expected[key].get("questions",[])}
        review_ids=set()
        for c in claims:
            if not isinstance(c,dict) or c.get("label") not in ALLOWED_TRUTH:
                raise ValueError(f"Bad claim object/label for {key}")
            rid=c.get("relation_id")
            if rid in review_ids or rid not in claim_ids:
                raise ValueError(f"Unexpected/duplicate claim ID {rid} for {key}")
            review_ids.add(rid)
        if review_ids!=claim_ids:
            raise ValueError(f"Unreviewed question claim(s) for {key}")
        found[key]=rec
    if set(found)!=set(expected):
        raise ValueError(f"Missing reviewed records: {set(expected)-set(found)}")
    flags=sum(bool(x.get("needs_escalation")) or
              x.get("acceptability")!="VALID" or
              any(y.get("label")=="UNRESOLVED" for y in x["claims"])
              for x in found.values())
    return {"batch_id":request["batch_id"],"review_count":len(found),
            "needs_followup_or_uncertain":flags,
            "promoted_to_gold":0,
            "status":"STRUCTURALLY_VALID_EXTERNAL_REVIEW_NOT_GOLD"}
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--request",type=Path,required=True)
    p.add_argument("--reply",type=Path,required=True)
    a=p.parse_args()
    req=json.loads(a.request.read_text(encoding="utf-8"))
    res=json.loads(a.reply.read_text(encoding="utf-8"))
    print(json.dumps(verify(req,res),indent=2))
if __name__=="__main__":
    main()
