"""Automatic metrics for generated dialogues: ROUGE-L F, BLEU and BERTScore F1 (Section 4.1).

    python evaluation/metrics.py results/raw -o results/metrics

Compares `generation` with the gold dialogue (`target`) for every CSV written by
inference/generate.py and adds per-row columns plus a `summary_metrics.csv` (overall and per
dialect). Texts are normalised (diacritics, tatweel, alif and alif maqsura variants),
tokenised with CAMeL Tools when installed (whitespace otherwise) and truncated to 2,000
characters, as in the paper's runs.
"""
import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
from tqdm.auto import tqdm

BERT_MODEL = "microsoft/deberta-xlarge-mnli"
MAX_CHARS = 2000
_DIACRITICS = re.compile(r"[ؗ-ًؚ-ٟۖ-ۭ]")
_SMOOTH = SmoothingFunction().method1

try:
    from camel_tools.tokenizers.word import simple_word_tokenize

    def tokenize(text):
        return [t for t in simple_word_tokenize(text) if t.strip()]
except ModuleNotFoundError:
    def tokenize(text):
        return text.split()


def normalize(text: str) -> str:
    text = _DIACRITICS.sub("", text).replace("ـ", "")
    text = re.sub(r"[إأٱآ]", "ا", text).replace("ى", "ي")
    return text.strip()


def _lcs(xs, ys):
    dp = [0] * (len(ys) + 1)
    for i in range(len(xs) - 1, -1, -1):
        prev = 0
        for j in range(len(ys) - 1, -1, -1):
            cur = dp[j]
            if xs[i] == ys[j]:
                dp[j] = 1 + prev
            elif dp[j] < dp[j + 1]:
                dp[j] = dp[j + 1]
            prev = cur
    return dp[0]


def rouge_l(ref: str, hyp: str, eps=1e-12) -> float:
    r, h = tokenize(normalize(ref)), tokenize(normalize(hyp))
    if not r or not h:
        return 0.0
    lcs = _lcs(h, r)
    prec, rec = lcs / len(h), lcs / len(r)
    if prec == 0 or rec == 0:
        return 0.0
    beta2 = prec / (rec + eps)
    return (1 + beta2**2) * prec * rec / (rec + beta2**2 * prec + eps)


def bleu(ref: str, hyp: str) -> float:
    return sentence_bleu([tokenize(normalize(ref))], tokenize(normalize(hyp)), smoothing_function=_SMOOTH)


def bertscore_f1(refs, hyps):
    from bert_score import score

    _, _, f1 = score(hyps, refs, model_type=BERT_MODEL)
    return [float(x) for x in f1]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", help="Folder of generation CSVs (or a single CSV).")
    p.add_argument("-o", "--output", default="results/metrics")
    args = p.parse_args()

    src, dst = Path(args.input), Path(args.output)
    dst.mkdir(parents=True, exist_ok=True)
    rows = []
    for path in sorted(src.glob("*.csv")) if src.is_dir() else [src]:
        df = pd.read_csv(path)
        refs = [str(x)[:MAX_CHARS] for x in df["target"]]
        hyps = [str(x)[:MAX_CHARS] for x in df["generation"].fillna("")]
        df["rouge_l"] = [rouge_l(r, h) for r, h in tqdm(zip(refs, hyps), total=len(df), desc=path.name)]
        df["bleu"] = [bleu(r, h) for r, h in zip(refs, hyps)]
        df["bertscore_f1"] = bertscore_f1(refs, hyps)
        df.to_csv(dst / path.name, index=False)
        for dialect, g in [("all", df)] + list(df.groupby("dialect")):
            rows.append({"file": path.name, "dialect": dialect, "n": len(g),
                         **{m: float(np.mean(g[m])) for m in ("rouge_l", "bleu", "bertscore_f1")}})
    pd.DataFrame(rows).to_csv(dst / "summary_metrics.csv", index=False)
    print(pd.DataFrame(rows).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
