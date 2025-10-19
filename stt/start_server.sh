#!/usr/bin/env bash
set -euo pipefail

# Usage: ./start_server.sh [cpu|cuda] [model] [compute]
# Examples:
#   ./start_server.sh cpu large-v3 int8
#   ./start_server.sh cuda large-v3 float16

DEVICE=${1:-cpu}
MODEL=${2:-large-v3}
COMPUTE=${3:-int8}

export STT_HOST=0.0.0.0
export STT_PORT=8000
export WHISPER_DEVICE="$DEVICE"
export WHISPER_MODEL="$MODEL"
export WHISPER_COMPUTE="$COMPUTE"

python3 -m pip install -r "$(dirname "$0")/requirements.txt"
python3 "$(dirname "$0")/server.py"
