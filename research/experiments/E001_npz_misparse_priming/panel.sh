#!/bin/bash
# Model panel for E001 (and reused by later experiments via RUN=...). Two GPU lanes.
cd "$(dirname "$0")/../../.."
export HF_HUB_OFFLINE=1
PY=/home/xiang/miniconda3/envs/verl-clean/bin/python
RUN=${RUN:-research/experiments/E001_npz_misparse_priming/run.py}
LOG=${LOG:-logs/gp/E001}
G0=${G0:-0}; G1=${G1:-1}
LANE0="pythia-160m=EleutherAI/pythia-160m pythia-410m-s1=EleutherAI/pythia-410m-seed1 pythia-1.4b=EleutherAI/pythia-1.4b pythia-2.8b=EleutherAI/pythia-2.8b qwen2.5-0.5b=Qwen/Qwen2.5-0.5B qwen2.5-3b=Qwen/Qwen2.5-3B qwen2.5-7b=Qwen/Qwen2.5-7B qwen2.5-32b=Qwen/Qwen2.5-32B llama-7b=huggyllama/llama-7b gemma3-1b-pt=google/gemma-3-1b-pt qwen2.5-14b-instruct=Qwen/Qwen2.5-14B-Instruct qwen3-32b=Qwen/Qwen3-32B"
LANE1="gpt2=gpt2 llama3.2-3b=unsloth/Llama-3.2-3B mistral-7b=mistralai/Mistral-7B-v0.3 gemma2-2b=google/gemma-2-2b qwen3-1.7b-base=Qwen/Qwen3-1.7B-Base qwen3-8b-base=Qwen/Qwen3-8B-Base llama2-7b=NousResearch/Llama-2-7b-hf qwen2.5-7b-instruct=Qwen/Qwen2.5-7B-Instruct llama3.1-8b-instruct=NousResearch/Meta-Llama-3.1-8B-Instruct qwen3-8b=Qwen/Qwen3-8B mistral-small-24b-instruct=mistralai/Mistral-Small-24B-Instruct-2501 gemma3-12b-it=google/gemma-3-12b-it"
CUDA_VISIBLE_DEVICES=$G0 nohup $PY $RUN --batch 128 --models $LANE0 > ${LOG}_lane0.log 2>&1 &
CUDA_VISIBLE_DEVICES=$G1 nohup $PY $RUN --batch 128 --models $LANE1 > ${LOG}_lane1.log 2>&1 &
wait
