"""Step 3: self-repair loop for dialogues not rated A.

    python pipeline/repair.py graded.csv repaired.csv

For each dialogue rated B-D, the generator rewrites it using the grader's rating and reason
(repair prompt), and the grader rates the new version. If it is still not an A, a second
round starts from the first rewrite. Writes `<dialect>_fix{1,2}_dialogue/_rating/_reason`.
Dialogues still below A after two rounds are left for human correction (finalize.py).
"""
import argparse
import time
from pathlib import Path

import pandas as pd
from tqdm.auto import tqdm

from common import DIALECTS, REPAIR, grading_prompt, parse_grade
from llm_apis import MODELS, chat

ROUNDS = 2


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", help="CSV from grade.py.")
    p.add_argument("output")
    p.add_argument("--generator", default="gemini-2.5-flash", choices=sorted(MODELS))
    p.add_argument("--grader", default="gpt-4o", choices=sorted(MODELS))
    p.add_argument("--sleep", type=float, default=0.5)
    args = p.parse_args()

    out = Path(args.output)
    df = pd.read_csv(out if out.exists() else args.input)
    for d in DIALECTS:
        for n in range(1, ROUNDS + 1):
            for f in ("dialogue", "rating", "reason"):
                if f"{d}_fix{n}_{f}" not in df.columns:
                    df[f"{d}_fix{n}_{f}"] = None

    for i in tqdm(df.index, desc="repair"):
        for d in DIALECTS:
            rating, reason, dialogue = df.at[i, f"{d}_rating"], df.at[i, f"{d}_reason"], df.at[i, f"{d}_dialogue"]
            if pd.isna(rating) or rating == "A" or pd.notna(df.at[i, f"{d}_fix1_dialogue"]):
                continue
            try:
                for n in range(1, ROUNDS + 1):
                    prompt = REPAIR[d].format(dialogue=dialogue, text=df.at[i, "Text"], rating=rating, reason=reason)
                    dialogue = chat(args.generator, prompt)
                    rating, reason = parse_grade(chat(args.grader, grading_prompt(d, df.at[i, "Text"], dialogue)))
                    df.at[i, f"{d}_fix{n}_dialogue"] = dialogue
                    df.at[i, f"{d}_fix{n}_rating"] = rating
                    df.at[i, f"{d}_fix{n}_reason"] = reason
                    if rating == "A":
                        break
            except Exception as exc:
                print(f"row {i} {d}: {exc}")
            df.to_csv(out, index=False)
            time.sleep(args.sleep)
    df.to_csv(out, index=False)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
