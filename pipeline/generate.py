"""Step 1: Wikipedia paragraph -> one six-turn dialogue per dialect (MSA, Egyptian, Maghrebi).

    python pipeline/generate.py paragraphs.csv generated.csv --model gemini-2.5-flash

`paragraphs.csv` needs a `Text` column. Writes `<dialect>_raw` (model reply) and
`<dialect>_dialogue` (JSON with the per-turn `reference` fields removed) for std / egy / mag.
The three dialects of a row are requested in parallel. Progress is saved after every row;
re-running the command resumes. The paper used Gemini-2.5-Flash as the generator.
"""
import argparse
import concurrent.futures
import time
from pathlib import Path

import pandas as pd
from tqdm.auto import tqdm

from common import DIALECTS, GENERATION, strip_references
from llm_apis import MODELS, chat


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--model", default="gemini-2.5-flash", choices=sorted(MODELS))
    p.add_argument("--model-id", default=None)
    p.add_argument("--sleep", type=float, default=0.5)
    args = p.parse_args()

    out = Path(args.output)
    df = pd.read_csv(out if out.exists() else args.input)
    for d in DIALECTS:
        for col in (f"{d}_raw", f"{d}_dialogue"):
            if col not in df.columns:
                df[col] = None

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(DIALECTS)) as pool:
        for i in tqdm(df.index, desc="generate"):
            todo = [d for d in DIALECTS if pd.isna(df.at[i, f"{d}_raw"])]
            if not todo:
                continue
            futures = {
                d: pool.submit(chat, args.model, GENERATION[d].format(text=df.at[i, "Text"]), args.model_id)
                for d in todo
            }
            for d, fut in futures.items():
                try:
                    df.at[i, f"{d}_raw"] = fut.result()
                    df.at[i, f"{d}_dialogue"] = strip_references(df.at[i, f"{d}_raw"])
                except Exception as exc:
                    print(f"row {i} {d}: {exc}")
            df.to_csv(out, index=False)
            time.sleep(args.sleep)
    df.to_csv(out, index=False)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
