#!/bin/bash
# Start E003c on GPU g once no E003/E003b scoring process (or relay) is using that GPU. No extra cards.
cd "$(dirname "$0")/../../.."
export HF_HUB_OFFLINE=1
PY=/home/xiang/miniconda3/envs/verl-clean/bin/python
R=research/experiments/E003_comprehension_link/run_history.py
L0="llama3.1-8b-instruct=NousResearch/Meta-Llama-3.1-8B-Instruct qwen2.5-7b-instruct=Qwen/Qwen2.5-7B-Instruct qwen3-32b=Qwen/Qwen3-32B mistral-7b=mistralai/Mistral-7B-v0.3"
L1="gemma3-12b-it=google/gemma-3-12b-it qwen3-8b=Qwen/Qwen3-8B qwen2.5-14b-instruct=Qwen/Qwen2.5-14B-Instruct"
busy() {  # gpu -> 0 if any of my E003/E003b python runs is on it
  for p in $(pgrep -u "$USER" -f 'research/experiments/E003_comprehension_link/run_(v2|reread).py'); do
    tr '\0' '\n' < /proc/$p/environ 2>/dev/null | grep -qx "CUDA_VISIBLE_DEVICES=$1" && return 0
  done
  pgrep -u "$USER" -f "relay(_reread)?\.sh" >/dev/null && [ "$2" = strict ] && return 0
  return 1
}
lane() {  # gpu models log
  sleep 120
  while busy "$1" strict || busy "$1"; do sleep 60; done
  echo "$(date) GPU$1 free; starting E003c" >> "$3"
  CUDA_VISIBLE_DEVICES=$1 $PY $R --batch 64 --models $2 >> "$3" 2>&1
}
mkdir -p logs/gp
lane 0 "$L0" logs/gp/E003c_lane0.log &
lane 1 "$L1" logs/gp/E003c_lane1.log &
wait
