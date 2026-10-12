#!/bin/bash
# Per-model chain: wait for E002 -> E004 -> freeze E005 prediction -> E005 held-out scoring.
# Usage: GPU=0 chain.sh tag=path [tag=path ...]
cd "$(dirname "$0")/../../.."
export HF_HUB_OFFLINE=1 CUDA_VISIBLE_DEVICES=${GPU:-0}
PY=/home/xiang/miniconda3/envs/verl-clean/bin/python
for spec in "$@"; do
  tag=${spec%%=*}
  until [ -f results/gp/E002/$tag.meta.json ]; do sleep 60; done
  $PY research/tools/prime_run.py --spec research/experiments/E004_repetition_history/spec.jsonl --exp E004 --batch 128 --models $spec
  $PY research/experiments/E005_heldout_confirmation/analyze.py --predict_only --B 1000
  $PY research/tools/prime_run.py --spec research/experiments/E005_heldout_confirmation/spec.jsonl \
      --prime_fams data/gp_behavior/derived/npz_heldout_v1.jsonl --exp E005 --batch 128 --models $spec
done
