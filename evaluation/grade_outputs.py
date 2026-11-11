"""LLM-grader score for generated dialogues (the "Grader Avg." row of Table 4).

    python evaluation/grade_outputs.py results/raw -o results/graded

GPT-4o rates each generated dialogue A-D with the dialect-specific rubric used to build the
corpus (pipeline/prompts.py), given the source paragraph. Ratings map A=4, B=3, C=2, D=1.
Re-running resumes unfinished files.
"""
import argparse
import sys
import time
from pathlib import Path

import pandas as pd
from tqdm.auto import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))
from common import grading_prompt, parse_grade  # noqa: E402
from llm_apis import MODELS, chat  # noqa: E402

CODE = {"msa": "std", "egyptian": "egy", "maghrebi": "mag"}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", help="Folder of generation CSVs (or a single CSV).")
    p.add_argument("-o", "--output", default="results/graded")
    p.add_argument("--model", default="gpt-4o", choices=sorted(MODELS))
    p.add_argument("--sleep", type=float, default=0.2)
    args = p.parse_args()

    src, dst = Path(args.input), Path(args.output)
    dst.mkdir(parents=True, exist_ok=True)
    for path in sorted(src.glob("*.csv")) if src.is_dir() else [src]:
        out = dst / path.name
        df = pd.read_csv(out if out.exists() else path)
        for col in ("grade_raw", "rating", "reason"):
            if col not in df.columns:
                df[col] = None
        for i in tqdm(df.index[df["grade_raw"].isna()], desc=path.name):
            prompt = grading_prompt(CODE[df.at[i, "dialect"]], df.at[i, "context"], df.at[i, "generation"])
            try:
                df.at[i, "grade_raw"] = chat(args.model, prompt)
            except Exception as exc:
                df.at[i, "grade_raw"] = f"ERROR: {exc}"
            df.at[i, "rating"], df.at[i, "reason"] = parse_grade(df.at[i, "grade_raw"])
            if i % 20 == 0:
                df.to_csv(out, index=False)
            time.sleep(args.sleep)
        df.to_csv(out, index=False)
        score = df["rating"].astype(str).str.strip().str.upper().map({"A": 4, "B": 3, "C": 2, "D": 1})
        print(f"{path.name}: grader average {score.mean():.3f}")


if __name__ == "__main__":
    main()
