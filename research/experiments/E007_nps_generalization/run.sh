#!/bin/bash
# E007: within-construction (NP/S targets) and cross-construction (NP/Z targets) runs. Usage: GPU=0 run.sh tag=path ...
cd "$(dirname "$0")/../../.."
export HF_HUB_OFFLINE=1 CUDA_VISIBLE_DEVICES=${GPU:-0}
PY=/home/xiang/miniconda3/envs/verl-clean/bin/python
NPS=data/gp_behavior/derived/nps_prime_families_v1.jsonl
SPEC=research/experiments/E007_nps_generalization/spec.jsonl
$PY research/tools/prime_run.py --spec $SPEC --target_fams $NPS --exp E007_within --batch 128 --models "$@"
$PY research/tools/prime_run.py --spec $SPEC --prime_fams $NPS --exp E007_cross --batch 128 --models "$@"
