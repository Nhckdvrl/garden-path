#!/usr/bin/env python3
"""Illustrative power/sensitivity for *independent lexical family* contrasts.

Assumption: family-level paired effects are approximately normal and exchangeable.
This is a planning approximation, NOT an empirical power claim or study guarantee.
Use a variance estimate from an independent or strictly designated discovery set.

Examples:
 python3 research/tools/sample_size_sensitivity.py --sd 0.25 --min-effect 0.08
 python3 research/tools/sample_size_sensitivity.py --sd 0.25 --min-effect 0.05 \
   --available-families 69
"""
from __future__ import annotations
import argparse
import json
import math
from statistics import NormalDist

def required_families(sd:float, effect:float, alpha:float=.05, power:float=.80)->int:
    if not (sd>0 and effect>0 and 0<alpha<1 and 0<power<1):
        raise ValueError("sd/effect > 0; alpha and power must be in (0,1)")
    z1=NormalDist().inv_cdf(1-alpha/2)
    z2=NormalDist().inv_cdf(power)
    return math.ceil(((z1+z2)*sd/effect)**2)

def minimum_effect_detectable(sd:float, n:int, alpha:float=.05, power:float=.80)->float:
    if n<2 or sd<=0 or not (0<alpha<1 and 0<power<1):
        raise ValueError("n>=2 and valid parameters required")
    return (NormalDist().inv_cdf(1-alpha/2)+NormalDist().inv_cdf(power))*sd/math.sqrt(n)

def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--sd",type=float,required=True,
                   help="Discovery data's standard deviation of one estimate per family, NOT per question")
    p.add_argument("--min-effect",type=float,required=True,help="Minimum meaningful family-average effect")
    p.add_argument("--alpha",type=float,default=.05)
    p.add_argument("--power",type=float,default=.80)
    p.add_argument("--available-families",type=int)
    a=p.parse_args()
    n=required_families(a.sd,a.min_effect,a.alpha,a.power)
    d={"assumptions":"paired approximately normal independent family effects; preliminary power only",
       "sd":a.sd,"min_meaningful_effect":a.min_effect,"alpha":a.alpha,"power":a.power,
       "approx_required_independent_families":n}
    if a.available_families is not None:
        d["available_independent_families"]=a.available_families
        d["approx_detectable_effect_at_available_n"]=minimum_effect_detectable(
            a.sd,a.available_families,a.alpha,a.power)
        d["approx_family_shortfall"]=max(0,n-a.available_families)
    print(json.dumps(d,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
