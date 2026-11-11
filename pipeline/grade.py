"""Step 2: rate every generated dialogue A-D with the LLM grader.

    python pipeline/grade.py generated.csv graded.csv --model gpt-4o

Uses the dialect-specific rubric prompts (A = fully correct and natural ... D = poor).
Writes `<dialect>_grade_raw`, `<dialect>_rating` and `<dialect>_reason`. The paper used
GPT-4o as the grader, the model whose ratings agreed best with native speakers.
"""
import argparse
import concurrent.futures
import time
from pathlib import Path

import pandas as pd
from tqdm.auto import tqdm

from common import DIALECTS, grading_prompt, parse_grade
from llm_apis import MODELS, chat


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", help="CSV from generate.py (needs Text and <dialect>_dialogue).")
    p.add_argument("output")
    p.add_argument("--model", default="gpt-4o", choices=sorted(MODELS))
    p.add_argument("--model-id", default=None)
    p.add_argument("--sleep", type=float, default=0.5)
    args = p.parse_args()

    out = Path(args.output)
    df = pd.read_csv(out if out.exists() else args.input)
    for d in DIALECTS:
        for col in (f"{d}_grade_raw", f"{d}_rating", f"{d}_reason"):
            if col not in df.columns:
                df[col] = None

    def grade(i, d):
        return chat(args.model, grading_prompt(d, df.at[i, "Text"], df.at[i, f"{d}_dialogue"]), args.model_id)

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(DIALECTS)) as pool:
        for i in tqdm(df.index, desc="grade"):
            todo = [d for d in DIALECTS if pd.isna(df.at[i, f"{d}_grade_raw"]) and pd.notna(df.at[i, f"{d}_dialogue"])]
            if not todo:
                continue
            futures = {d: pool.submit(grade, i, d) for d in todo}
            for d, fut in futures.items():
                try:
                    raw = fut.result()
                except Exception as exc:
                    raw = f"ERROR: {exc}"
                df.at[i, f"{d}_grade_raw"] = raw
                df.at[i, f"{d}_rating"], df.at[i, f"{d}_reason"] = parse_grade(raw)
            df.to_csv(out, index=False)
            time.sleep(args.sleep)
    df.to_csv(out, index=False)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
