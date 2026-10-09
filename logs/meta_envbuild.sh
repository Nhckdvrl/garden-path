#!/usr/bin/env bash
set -x
UV=/home/xiang/.local/bin/uv
VENV=/home/xiang/.venvs/vllm023-cu128
$UV venv --python 3.12 $VENV || exit 1
$UV pip install --python $VENV/bin/python \
  torch==2.11.0 torchvision==0.26.0 torchaudio==2.11.0 \
  --index-url https://download.pytorch.org/whl/cu128 || exit 1
$UV pip install --python $VENV/bin/python vllm==0.23.0 || exit 1
$VENV/bin/python -c "import vllm,torch,transformers; print(\"BUILT vllm\",vllm.__version__,\"torch\",torch.__version__,\"tf\",transformers.__version__)"
