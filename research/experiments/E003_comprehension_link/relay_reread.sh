#!/bin/bash
# Run E003b on each GPU after the E003 process on that GPU exits (no extra cards).
# Usage (on fvcrc11): relay_reread.sh <E003_pid_gpu0> <E003_pid_gpu1>
cd "$(dirname "$0")/../../.."
export HF_HUB_OFFLINE=1
PY=/home/xiang/miniconda3/envs/verl-clean/bin/python
R=research/experiments/E003_comprehension_link/run_reread.py
L0="mistral-7b=mistralai/Mistral-7B-v0.3 qwen2.5-7b-instruct=Qwen/Qwen2.5-7B-Instruct qwen2.5-14b-instruct=Qwen/Qwen2.5-14B-Instruct qwen2.5-7b=Qwen/Qwen2.5-7B qwen3-32b=Qwen/Qwen3-32B qwen2.5-32b=Qwen/Qwen2.5-32B"
L1="llama3.1-8b-instruct=NousResearch/Meta-Llama-3.1-8B-Instruct gemma3-12b-it=google/gemma-3-12b-it qwen3-8b=Qwen/Qwen3-8B llama2-7b=NousResearch/Llama-2-7b-hf"
lane() {  # gpu pid models log
  while kill -0 "$2" 2>/dev/null; do sleep 60; done
  echo "$(date) GPU$1 free (E003 pid $2 exited); starting E003b" >> "$4"
  CUDA_VISIBLE_DEVICES=$1 $PY $R --batch 64 --models $3 >> "$4" 2>&1
}
mkdir -p logs/gp
lane 0 "$1" "$L0" logs/gp/E003b_lane0.log &
lane 1 "$2" "$L1" logs/gp/E003b_lane1.log &
wait
