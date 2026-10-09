#!/usr/bin/env bash
# Rebuild the §14.3 run-environment reconstruction: vllm 0.23.0+cu129 wheel
# (official GitHub release asset) paired with torch 2.11.0+cu129, replacing
# the PyPI default (CUDA 13) build that cannot run on the cluster's 550/12.4
# driver. Same package VERSIONS as fgvd (vllm 0.23.0, transformers 5.12.1,
# huggingface-hub 1.20.1, tokenizers 0.22.2); only CUDA build tags differ.
set -x
UV=/home/xiang/.local/bin/uv
VENV=/home/xiang/.venvs/vllm023-cu128
$UV pip install --python $VENV/bin/python \
  "https://github.com/vllm-project/vllm/releases/download/v0.23.0/vllm-0.23.0+cu129-cp38-abi3-manylinux_2_28_x86_64.whl" \
  "torch==2.11.0+cu129" \
  --extra-index-url https://download.pytorch.org/whl/cu129 || exit 1
# re-pin the prompt-load-bearing packages in case resolution moved them
$UV pip install --python $VENV/bin/python "transformers==5.12.1" "huggingface-hub==1.20.1" || exit 1
$VENV/bin/python -c "import vllm,torch,transformers,huggingface_hub,tokenizers; print('BUILT2 vllm',vllm.__version__,'torch',torch.__version__,'tf',transformers.__version__,'hub',huggingface_hub.__version__,'tok',tokenizers.__version__)" || exit 1
ldd $VENV/lib/python3.12/site-packages/vllm/_C.abi3.so | grep -E "cudart|not found" || true
echo INSTALL_DONE
