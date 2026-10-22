#!/bin/bash
# Minimal GPU job queue (project budget: 4 GPUs, user instruction 2026-10-23).
# Usage: gpu_queue.sh <gpus e.g. 0 or 2,3> <log> <queue file> [more queue files, in priority order]
# Each queue line is a shell command run from the repo root with CUDA_VISIBLE_DEVICES=<gpus>.
# A line is removed from its queue (under flock) before it runs. A worker exits when every queue is empty.
cd "$(dirname "$0")/../.."
export HF_HUB_OFFLINE=1 VLLM_WORKER_MULTIPROC_METHOD=spawn CUDA_VISIBLE_DEVICES=$1
log=$2; shift 2
pop() {  # print and delete the first non-empty line of $1
  ( flock 9; l=$(grep -m1 -v '^\s*$' "$1"); [ -n "$l" ] && { printf '%s\n' "$l"; grep -vxF -- "$l" "$1" > "$1.tmp"; mv "$1.tmp" "$1"; } ) 9>"$1.lock"
}
while true; do
  job=""
  for q in "$@"; do job=$(pop "$q"); [ -n "$job" ] && break; done
  [ -z "$job" ] && { echo "$(date) GPU $CUDA_VISIBLE_DEVICES: queues empty, exit" >> $log; exit 0; }
  echo "$(date) GPU $CUDA_VISIBLE_DEVICES start: $job" >> $log
  bash -c "$job" >> $log 2>&1
  echo "$(date) GPU $CUDA_VISIBLE_DEVICES end (rc=$?): $job" >> $log
done
