#!/bin/bash
# Scale extension (2026-10-23): run the core scored experiments for one or more models on given GPUs.
# E002 -> E004 -> E005 (frozen per-model prediction, then held-out scoring) -> E009 -> E011 -> E003.
# Usage: GPUS=0,1 [LMSCORE_DEVICE_MAP=auto] scale_lane.sh <log> tag=path [...]
cd "$(dirname "$0")/../.."
export HF_HUB_OFFLINE=1 CUDA_VISIBLE_DEVICES=${GPUS:-${CUDA_VISIBLE_DEVICES:-0}}
PY=/home/xiang/miniconda3/envs/verl-clean/bin/python
E=research/experiments
log=$1; shift
for m in "$@"; do
  echo "$(date) start $m" >> $log
  $PY research/tools/prime_run.py --spec $E/E002_surface_vs_analysis/spec.jsonl --exp E002 --batch 64 --models $m >> $log 2>&1
  $PY research/tools/prime_run.py --spec $E/E004_repetition_history/spec.jsonl --exp E004 --batch 64 --models $m >> $log 2>&1
  flock results/gp/E005/.predict.lock $PY $E/E005_heldout_confirmation/analyze.py --predict_only --B 1000 >> $log 2>&1
  $PY research/tools/prime_run.py --spec $E/E005_heldout_confirmation/spec.jsonl \
      --prime_fams data/gp_behavior/derived/npz_heldout_v1.jsonl --exp E005 --batch 64 --models $m >> $log 2>&1
  $PY research/tools/prime_run.py --spec $E/E009_case_disambiguation/spec.jsonl --exp E009 --batch 64 --models $m >> $log 2>&1
  $PY research/tools/prime_run.py --spec $E/E011_local_coherence/spec.jsonl --exp E011 --batch 64 --models $m >> $log 2>&1
  $PY $E/E003_comprehension_link/run_v2.py --batch 64 --models $m >> $log 2>&1
  echo "$(date) done $m" >> $log
done
