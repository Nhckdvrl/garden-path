#!/bin/bash
# Start each E012 lane on fvcrc20 only after the given process on that GPU exits (no extra cards).
# Usage: relay.sh <pid_on_gpu0> <pid_on_gpu1>
cd "$(dirname "$0")/../../.."
export HF_HUB_OFFLINE=1
PY=/home/xiang/miniconda3/envs/verl-clean/bin/python
R=research/experiments/E012_free_production/run.py
L0="llama3.2-3b=unsloth/Llama-3.2-3B mistral-7b=mistralai/Mistral-7B-v0.3 qwen2.5-7b=Qwen/Qwen2.5-7B llama3.1-8b-instruct=NousResearch/Meta-Llama-3.1-8B-Instruct"
L1="qwen3-8b-base=Qwen/Qwen3-8B-Base qwen2.5-7b-instruct=Qwen/Qwen2.5-7B-Instruct gemma2-2b=google/gemma-2-2b pythia-1.4b=EleutherAI/pythia-1.4b"
lane() {  # gpu pid models log
  while kill -0 "$2" 2>/dev/null; do sleep 60; done
  echo "$(date) GPU$1 free (pid $2 exited); starting E012" >> "$4"
  CUDA_VISIBLE_DEVICES=$1 $PY $R --models $3 >> "$4" 2>&1
}
mkdir -p logs/gp
lane 0 "$1" "$L0" logs/gp/E012_lane0.log &
lane 1 "$2" "$L1" logs/gp/E012_lane1.log &
wait
