#!/usr/bin/env python3
"""Convert risk-stratified public family review queue to 3–5-record OpenCode packets.

This NEVER calls a model. It exposes published source sentences and the
authors' raw task questions, not any tested LLM responses.
Usage: python3 research/tools/make_model_review_batches.py \
  --queue /tmp/source_review_queue.jsonl --outdir /tmp/opencode_review
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

def stable_bytes(obj:dict)->bytes:
    return (json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(",",":"))+"\n").encode("utf-8")

def source_packets(queue_rows:list[dict], max_records:int=4,
                   source_queue_sha256:str="")->list[dict]:
    if not 1<=max_records<=5:
        raise ValueError("max_records must be between 1 and 5")
    flattened=[]
    family_ids=set()
    for f in queue_rows:
        fid=f.get("family_id")
        if not isinstance(fid,str) or not fid or fid in family_ids:
            raise ValueError("Queue has empty or duplicate family")
        family_ids.add(fid)
        sources=f.get("original_sentences")
        if not isinstance(sources,dict) or set(sources)!={"GP","CUE"}:
            raise ValueError(f"Queue has incomplete GP/CUE source pair for {fid}")
        for condition in ("GP","CUE"):
            src=sources[condition]
            content=src.get("sentence")
            if not isinstance(content,str) or not content:
                raise ValueError(f"Missing source for {fid}/{condition}")
            sha=hashlib.sha256(content.encode("utf-8")).hexdigest()
            if sha!=src.get("sha256"):
                raise ValueError(f"Source checksum mismatch for {fid}/{condition}")
            flattened.append({
                "family_id":fid,
                "candidate_id":f"{fid}__{condition}",
                "construction":f.get("construction"),
                "condition":condition,
                "sentence":content,
                "source_sha256":sha,
                "questions":src.get("source_question_candidates",[]),
                "selection_reasons":f.get("selection_reasons",[]),
            })
    # Do not split a GP/CUE family across different batches.
    families=[flattened[i:i+2] for i in range(0,len(flattened),2)]
    families_per_batch=max(1,max_records//2)
    packets=[]
    for n in range(0,len(families),families_per_batch):
        recs=[r for family in families[n:n+families_per_batch] for r in family]
        batch_id=f"gp_review_{n//families_per_batch+1:04d}"
        packet={
            "batch_id":batch_id,
            "source_queue_sha256":source_queue_sha256,
            "input_records":recs,
            "review_instructions_file":"research/model_assisted/REVIEW_PROMPT.md",
            "status":"SOURCE_MATERIAL_FOR_REVIEW_ONLY",
        }
        packet["packet_sha256"]=hashlib.sha256(stable_bytes(packet)).hexdigest()
        packets.append(packet)
    return packets

def make_batches(queue:Path,outdir:Path,max_records:int)->dict:
    raw=queue.read_bytes()
    rows=[json.loads(x) for x in raw.decode("utf-8").splitlines() if x.strip()]
    packets=source_packets(rows,max_records,hashlib.sha256(raw).hexdigest())
    outdir.mkdir(parents=True,exist_ok=True)
    paths=[]
    for p in packets:
        path=outdir/(p["batch_id"]+".json")
        if path.exists():
            raise FileExistsError(f"Refuse to overwrite existing frozen review batch {path}")
        path.write_bytes(stable_bytes(p))
        paths.append(str(path))
    summary={"source_queue":str(queue),"review_family_count":len(rows),
             "records":2*len(rows),"batch_count":len(paths),
             "max_records":max_records,
             "model_calls_performed":0,
             "note":"No external model called. Only review requests generated. "
                    "Confirm explicitly free model + privacy and validate responses."}
    (outdir/"BATCH_SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    return summary

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--queue",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    p.add_argument("--max-records",type=int,default=4)
    a=p.parse_args()
    print(json.dumps(make_batches(a.queue,a.outdir,a.max_records),indent=2))
    print("Manual example: opencode run --model opencode/<verified-id-ending-free> "
          "--file research/model_assisted/REVIEW_PROMPT.md "
          "--file /tmp/opencode_review/gp_review_0001.json "
          "'Review only these public materials; return strict JSON'")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
