#!/bin/bash
# E003 v2 panel (Christianson 2001 cells). Two GPU lanes; base + instruct models.
cd "$(dirname "$0")/../../.."
export HF_HUB_OFFLINE=1
PY=/home/xiang/miniconda3/envs/verl-clean/bin/python
R=research/experiments/E003_comprehension_link/run_v2.py
G0=${G0:-0}; G1=${G1:-1}
LANE0="gpt2=gpt2 pythia-410m-s1=EleutherAI/pythia-410m-seed1 pythia-1.4b=EleutherAI/pythia-1.4b pythia-2.8b=EleutherAI/pythia-2.8b qwen2.5-0.5b=Qwen/Qwen2.5-0.5B qwen2.5-3b=Qwen/Qwen2.5-3B qwen2.5-7b=Qwen/Qwen2.5-7B qwen2.5-32b=Qwen/Qwen2.5-32B llama2-7b=NousResearch/Llama-2-7b-hf qwen2.5-7b-instruct=Qwen/Qwen2.5-7B-Instruct qwen2.5-14b-instruct=Qwen/Qwen2.5-14B-Instruct qwen3-32b=Qwen/Qwen3-32B"
LANE1="pythia-160m=EleutherAI/pythia-160m llama3.2-3b=unsloth/Llama-3.2-3B mistral-7b=mistralai/Mistral-7B-v0.3 gemma2-2b=google/gemma-2-2b qwen3-8b-base=Qwen/Qwen3-8B-Base qwen3-1.7b-base=Qwen/Qwen3-1.7B-Base llama3.1-8b-instruct=NousResearch/Meta-Llama-3.1-8B-Instruct gemma3-12b-it=google/gemma-3-12b-it mistral-small-24b-instruct=mistralai/Mistral-Small-24B-Instruct-2501 qwen3-8b=Qwen/Qwen3-8B"
mkdir -p logs/gp
CUDA_VISIBLE_DEVICES=$G0 $PY $R --batch 128 --models $LANE0 > logs/gp/E003_lane0.log 2>&1 &
CUDA_VISIBLE_DEVICES=$G1 $PY $R --batch 128 --models $LANE1 > logs/gp/E003_lane1.log 2>&1 &
wait
