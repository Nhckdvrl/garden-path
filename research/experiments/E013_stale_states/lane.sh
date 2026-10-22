#!/bin/bash
# One model per process on one GPU. Usage: lane.sh <gpu> <dtype> <log> tag=path [...]
cd "$(dirname "$0")/../../.."
export HF_HUB_OFFLINE=1
gpu=$1; dt=$2; log=$3; shift 3
for m in "$@"; do
  CUDA_VISIBLE_DEVICES=$gpu /home/xiang/miniconda3/envs/verl-clean/bin/python research/experiments/E013_stale_states/run.py --dtype $dt --models "$m" >> "$log" 2>&1
done
