#!/usr/bin/env python3
"""Offline analysis for completed, independently audited Garden Path model outputs.

Pilot A consumes source-entailment judgments and reports per-role GP/CUE paired
accuracy and bounds from invalid responses. Pilot B consumes teacher-forced
target log probabilities and reports the lexical-family bootstrap of
(GP-CUE)-(NONAMB_BARE-NONAMB_CUE) contrasts.

NO weights/API/GPU. NO raw outcome inference is performed here. Runs on
already-qualified, preregistered response records; unreviewed materials do not
become valid by being analyzed.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

CONDITIONS_B = ("GP", "CUE", "NONAMB_BARE", "NONAMB_CUE")
PROBES_A = ("OBSOLETE", "FINAL", "INDEPENDENT", "BRIDGE")
TRUTH = ("ENTAILED", "CONTRADICTED", "NOT_ENTAILED")
VALIDITY = ("VALID", "INVALID", "CAPPED", "UNKNOWN")

def load_jsonl(path: Path) -> list[dict]:
    arr = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
            if not isinstance(obj, dict):
                raise ValueError("expected an object")
            arr.append(obj)
        except (ValueError, json.JSONDecodeError) as err:
            raise ValueError(f"JSONL {path} line {n}: {err}") from err
    if not arr:
        raise ValueError("Empty input")
    return arr

def _quantile(xs: list[float], p: float) -> float:
    xs = sorted(xs)
    x = (len(xs) - 1) * p
    a, b = math.floor(x), math.ceil(x)
    return xs[a] * (b - x) + xs[b] * (x - a) if a != b else xs[a]

def family_bootstrap(values: dict[str, float], nboot: int=5000, seed: int=2718) -> dict:
    """One mean per independent lexical family, resampling families only."""
    if not values:
        raise ValueError("No independent families")
    fs = sorted(values)
    xs = [float(values[x]) for x in fs]
    if not all(math.isfinite(x) for x in xs):
        raise ValueError("non-finite family effect")
    stats: dict[str, Any] = {
        "n_families": len(xs),
        "mean": statistics.fmean(xs),
        "median_family_effect": statistics.median(xs),
        "families_positive": sum(x > 0 for x in xs),
        "families_negative": sum(x < 0 for x in xs),
        "families_zero": sum(x == 0 for x in xs)
    }
    if len(xs) < 2:
        stats["ci95"] = None
        stats["warning"] = "n<2: cannot estimate between-family uncertainty"
        return stats
    rng = random.Random(seed)
    draws = [statistics.fmean(xs[rng.randrange(len(xs))] for _ in xs)
             for _ in range(nboot)]
    stats["ci95"] = [_quantile(draws, 0.025), _quantile(draws, 0.975)]
    return stats

def _need_string(row: dict, field: str) -> str:
    v = row.get(field)
    if not isinstance(v, str) or not v:
        raise ValueError(f"Missing required string {field} in {row.get('item_id', row)}")
    return v

def analyze_a(rows: list[dict], nboot: int=5000) -> dict:
    """Preserves missing/capped answers as upper/lower outcome bounds."""
    index: dict[tuple, dict] = {}
    groups: dict[tuple, set] = defaultdict(set)
    for row in rows:
        model, fam, probe, cond = (_need_string(row, x) for x in
                                    ("model_id","family_id","probe_type","condition"))
        if probe not in PROBES_A or cond not in ("GP","CUE"):
            raise ValueError(f"Unexpected A probe/condition: {probe}/{cond}")
        if row.get("gold_review") != "PASSED":
            raise ValueError(f"Unaudited model-response gold for {model}/{fam}/{probe}")
        gold = row.get("gold_status")
        status = row.get("response_status")
        if gold not in TRUTH or status not in VALIDITY:
            raise ValueError(f"Invalid gold/response validity: {gold}/{status}")
        pred = row.get("predicted_status")
        if status == "VALID" and pred not in TRUTH:
            raise ValueError("VALID output requires tri-valued predicted_status")
        if status != "VALID" and pred not in (None, "UNRESOLVED"):
            raise ValueError("Missing/capped answers must not have a forced answer label")
        key=(model,fam,probe,cond)
        if key in index:
            raise ValueError(f"Duplicate A cell {key}; aggregate replicates prospectively")
        index[key]=row
        groups[(model,fam)].add((probe,cond))

    models=sorted({x[0] for x in index})
    out={"pilot":"A","n_input_rows":len(rows),"model_results":{},
         "interpretation":"Harm = accuracy(CUE)-accuracy(GP); positive means GP harms that probe. "
         "Unknown/capped outputs yield lower and upper harm bounds."}
    for model in models:
        families=sorted({f for (m,f,_,_) in index if m==model})
        for f in families:
            need={(p,c) for p in PROBES_A for c in ("GP","CUE")}
            if groups[(model,f)]!=need:
                raise ValueError(f"Incomplete A 4-probe×2-condition family: {model}/{f}")
            for p in PROBES_A:
                a,b=(index[(model,f,p,c)] for c in ("GP","CUE"))
                if a["gold_status"]!=b["gold_status"]:
                    raise ValueError(f"A GP/CUE gold disagreement {model}/{f}/{p}")
        panels={}
        for probe in PROBES_A:
            lows, highs={},{}
            invalid=0
            for fam in families:
                gp=index[(model,fam,probe,"GP")];cue=index[(model,fam,probe,"CUE")]
                def accuracy_bounds(x:dict) -> tuple[float,float]:
                    if x["response_status"]!="VALID":
                        return 0.0,1.0
                    y=float(x["predicted_status"]==x["gold_status"])
                    return y,y
                gp_low,gp_hi=accuracy_bounds(gp); cue_low,cue_hi=accuracy_bounds(cue)
                lows[fam]=cue_low-gp_hi
                highs[fam]=cue_hi-gp_low
                invalid+=int(gp["response_status"]!="VALID")+int(cue["response_status"]!="VALID")
            panels[probe]={"harm_lower":family_bootstrap(lows,nboot=nboot),
                            "harm_upper":family_bootstrap(highs,nboot=nboot),
                            "invalid_cells":invalid,"total_cells":2*len(families)}
        # Descriptive interaction: bridge impairment beyond final impairment.
        # This is NOT a causal test of global incoherence.
        out["model_results"][model]={
            "n_families":len(families),"probes":panels,
            "warning":"Probe differences are behavioral; errors in downstream BRIDGE "
                      "may inherit FINAL mistakes. New dependency counterfactuals required."
        }
    return out

def analyze_b(rows: list[dict], nboot: int=5000) -> dict:
    index: dict[tuple,dict]={}
    for row in rows:
        model,fam,target,cond=(_need_string(row,k) for k in
                              ("model_id","family_id","target_id","condition"))
        if cond not in CONDITIONS_B:
            raise ValueError(f"Unexpected priming condition {cond}")
        if row.get("material_review")!="PASSED":
            raise ValueError(f"Unaudited prime/target {model}/{fam}/{target}")
        trans,intrans=row.get("logp_transitive"),row.get("logp_intransitive")
        if isinstance(trans,bool) or isinstance(intrans,bool) or not all(
            isinstance(x,(int,float)) and math.isfinite(x) for x in (trans,intrans)
        ):
            raise ValueError("Pilot B requires finite numeric continuation log probabilities")
        if not row.get("target_sha") or not row.get("prompt_sha"):
            raise ValueError("Pilot B target/prompt hash missing")
        key=model,fam,target,cond
        if key in index:
            raise ValueError(f"Duplicate Pilot B cell {key}")
        index[key]=row
    models=sorted({x[0] for x in index})
    out={"pilot":"B","n_input_rows":len(rows),"model_results":{},
         "estimand":"delta_path = (L_GP-L_CUE)-(L_NONAMB_BARE-L_NONAMB_CUE), "
         "L=logp_transitive-logp_intransitive, average over targets THEN families"}
    for m in models:
        groups:dict[tuple,set]=defaultdict(set)
        for mm,fam,t,cond in index:
            if mm==m: groups[fam,t].add(cond)
        family_vals:dict[str,list[float]]=defaultdict(list)
        for (fam,target),present in groups.items():
            if present!=set(CONDITIONS_B):
                raise ValueError(f"Incomplete four-condition B unit: {m}/{fam}/{target}")
            q=[index[(m,fam,target,c)] for c in CONDITIONS_B]
            if len({r["target_sha"] for r in q})!=1:
                raise ValueError(f"Target candidates differ across conditions for {m}/{fam}/{target}")
            if len({r.get("source_revision") for r in q})!=1:
                raise ValueError(f"Source revision mismatch {m}/{fam}/{target}")
            L={c:q[i]["logp_transitive"]-q[i]["logp_intransitive"]
               for i,c in enumerate(CONDITIONS_B)}
            family_vals[fam].append((L["GP"]-L["CUE"])-
                                    (L["NONAMB_BARE"]-L["NONAMB_CUE"]))
        effects={fam:statistics.fmean(v) for fam,v in family_vals.items()}
        out["model_results"][m]={
            "primary_path_interaction":family_bootstrap(effects,nboot=nboot),
            "n_targets":sum(len(x) for x in family_vals.values()),
            "warning":"Positive interaction is a context-conditioned syntactic "
                      "choice effect; not proof of an internal stored parse. "
                      "Punctuation/lexical/semantic controls must be examined."
        }
    return out

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pilot",required=True,choices=("A","B"))
    p.add_argument("--input",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    p.add_argument("--boot",type=int,default=5000)
    args=p.parse_args()
    if args.boot<200:
        raise ValueError("Require at least 200 resamples for exploratory CI")
    data=load_jsonl(args.input)
    result=analyze_a(data,args.boot) if args.pilot=="A" else analyze_b(data,args.boot)
    result["source_input_path"]=str(args.input)
    result["bootstrap_resamples"]=args.boot
    result["status"]="OFFLINE_ANALYSIS_OF_SUPPLIED_MODEL_RESPONSES"
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"Wrote {args.output}, n={len(data)}, models={len(result['model_results'])}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
