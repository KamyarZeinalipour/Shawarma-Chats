"""Combine automatic metrics and grader ratings into one table (Table 4 and Appendix E).

    python evaluation/summarize.py results/metrics results/graded -o results/summary.csv
    python evaluation/summarize.py --paper     # print the paper's numbers from paper_results/

Output: one row per file and dialect (all, msa, egyptian, maghrebi) with ROUGE-L, BLEU,
BERTScore F1, grader average and the A-D rating counts.
"""
import argparse
from pathlib import Path

import pandas as pd

SCORE = {"A": 4, "B": 3, "C": 2, "D": 1}


def summarize(metrics_dir: Path, graded_dir: Path) -> pd.DataFrame:
    rows = []
    for path in sorted(metrics_dir.glob("*.csv")):
        if path.name == "summary_metrics.csv":
            continue
        m = pd.read_csv(path)
        g = pd.read_csv(graded_dir / path.name)
        g["rating"] = g["rating"].astype(str).str.strip().str.upper()
        for dialect in ["all", "msa", "egyptian", "maghrebi"]:
            ms = m if dialect == "all" else m[m.dialect == dialect]
            gs = g if dialect == "all" else g[g.dialect == dialect]
            rows.append({"file": path.stem, "dialect": dialect, "n": len(ms),
                         "rouge_l": ms.rouge_l.mean(), "bleu": ms.bleu.mean(), "bertscore_f1": ms.bertscore_f1.mean(),
                         "grader_avg": gs.rating.map(SCORE).mean(),
                         **{f"grader_{k}": int((gs.rating == k).sum()) for k in "ABCD"}})
    return pd.DataFrame(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("metrics", nargs="?", default="results/metrics")
    p.add_argument("graded", nargs="?", default="results/graded")
    p.add_argument("-o", "--output", default=None)
    p.add_argument("--paper", action="store_true", help="Show the paper's results from paper_results/.")
    args = p.parse_args()

    if args.paper:
        df = pd.read_csv(Path(__file__).resolve().parents[1] / "paper_results" / "results.csv")
    else:
        df = summarize(Path(args.metrics), Path(args.graded))
    with pd.option_context("display.width", 200, "display.max_columns", None):
        print(df.round(3).to_string(index=False))
    if args.output:
        df.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
