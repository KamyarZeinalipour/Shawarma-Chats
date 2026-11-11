"""Step 4: keep the A-rated version of every dialogue and list what needs a human.

    python pipeline/finalize.py repaired.csv final.csv

For each paragraph and dialect the final dialogue is the original if rated A, otherwise the
first repair rated A. Dialogues with no A version get `<dialect>_source = human` and an empty
`<dialect>_final`; in the paper these 0.5% were corrected by native speakers.
On the released corpus this rule reproduces the published dialogue for 99.96% of the
29,851 automatically resolved items.
"""
import argparse

import pandas as pd

from common import DIALECTS, strip_fence


def pick(row, d):
    if row.get(f"{d}_rating") == "A":
        return row[f"{d}_dialogue"], "original"
    for n in (1, 2):
        if row.get(f"{d}_fix{n}_rating") == "A":
            return strip_fence(row[f"{d}_fix{n}_dialogue"]), f"repair{n}"
    return None, "human"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", help="CSV from repair.py.")
    p.add_argument("output")
    args = p.parse_args()

    df = pd.read_csv(args.input)
    for d in DIALECTS:
        picked = df.apply(lambda r: pick(r, d), axis=1)
        df[f"{d}_final"] = [x[0] for x in picked]
        df[f"{d}_source"] = [x[1] for x in picked]
        counts = df[f"{d}_source"].value_counts().to_dict()
        print(d, counts)
    df.to_csv(args.output, index=False)
    print(f"Saved {args.output}. Rows with source == human need manual correction.")


if __name__ == "__main__":
    main()
