#!/bin/bash
# Start each E003 lane only after the E002 process on the same GPU has exited (no extra cards).
# Usage (on fvcrc11): relay.sh <E002_pid_gpu0> <E002_pid_gpu1>
cd "$(dirname "$0")/../../.."
export HF_HUB_OFFLINE=1
PY=/home/xiang/miniconda3/envs/verl-clean/bin/python
R=research/experiments/E003_comprehension_link/run_v2.py
source <(grep -E '^LANE[01]=' research/experiments/E003_comprehension_link/panel.sh)
lane() {  # gpu pid lanemodels log
  while kill -0 "$2" 2>/dev/null; do sleep 60; done
  echo "$(date) GPU$1 free (E002 pid $2 exited); starting E003" >> "$4"
  CUDA_VISIBLE_DEVICES=$1 $PY $R --batch 128 --models $3 >> "$4" 2>&1
}
mkdir -p logs/gp
lane 0 "$1" "$LANE0" logs/gp/E003_lane0.log &
lane 1 "$2" "$LANE1" logs/gp/E003_lane1.log &
wait
