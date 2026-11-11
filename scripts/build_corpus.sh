#!/usr/bin/env bash
# Build dialogues for new paragraphs with the paper's pipeline (needs API keys in .env).
#   usage: scripts/build_corpus.sh paragraphs.csv work_dir
set -euo pipefail
cd "$(dirname "$0")/.."
IN=$1; W=${2:-work}; mkdir -p "$W"

python pipeline/generate.py "$IN" "$W/1_generated.csv" --model gemini-2.5-flash
python pipeline/grade.py    "$W/1_generated.csv" "$W/2_graded.csv" --model gpt-4o
python pipeline/repair.py   "$W/2_graded.csv" "$W/3_repaired.csv"
python pipeline/finalize.py "$W/3_repaired.csv" "$W/4_final.csv"
