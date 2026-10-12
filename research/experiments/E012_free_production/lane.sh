#!/bin/bash
# Run E012 models one process per model on one GPU. Usage: lane.sh <gpu> <log> tag=path [...]
cd "$(dirname "$0")/../../.."
export HF_HUB_OFFLINE=1
gpu=$1; log=$2; shift 2
for m in "$@"; do
  CUDA_VISIBLE_DEVICES=$gpu /home/xiang/miniconda3/envs/verl-clean/bin/python research/experiments/E012_free_production/run.py --models "$m" >> "$log" 2>&1
done
