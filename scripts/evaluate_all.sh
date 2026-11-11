#!/usr/bin/env bash
# Score every file in results/raw: automatic metrics, GPT-4o grader, summary table.
set -euo pipefail
cd "$(dirname "$0")/.."

python evaluation/metrics.py results/raw -o results/metrics
python evaluation/grade_outputs.py results/raw -o results/graded
python evaluation/summarize.py results/metrics results/graded -o results/summary.csv
