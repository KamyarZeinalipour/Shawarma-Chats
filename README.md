# Shawarma Chats 🥙

**A content-grounded dialogue benchmark in Modern Standard, Egyptian and Maghrebi Arabic**

[![Paper](https://img.shields.io/badge/ArabicNLP_2025-paper-b31b1b)](https://aclanthology.org/2025.arabicnlp-main.39/)
[![Dataset](https://img.shields.io/badge/%F0%9F%A4%97_Dataset-arabic__multi__dialect__dialogue-yellow)](https://huggingface.co/datasets/Kamyar-zeinalipour/arabic_multi_dialect_dialogue)
[![Models](https://img.shields.io/badge/%F0%9F%A4%97_Collection-6_LoRA_adapters-orange)](https://huggingface.co/collections/Kamyar-zeinalipour/shawarmachats-arabicnlp-2025-6af4656eda045ed7cfc001d3)
[![Code license](https://img.shields.io/badge/code-Apache_2.0-blue)](LICENSE)
[![Data license](https://img.shields.io/badge/data-CC_BY--SA_4.0-lightgrey)](data/README.md#license)

ShawarmaChats is a benchmark of **30,012 six-turn conversations** grounded in Arabic Wikipedia
paragraphs, with the same paragraph rendered as a dialogue in all three varieties. It was built with
an LLM generator–grader **self-repair loop**: one model writes the dialogue, another rates it A–D
with a dialect-specific rubric and explains why, the writer revises, and only A-rated dialogues are
kept. Native speakers corrected the last 0.5%.

This repository accompanies the paper
[*Shawarma Chats: A Benchmark Exact Dialogue & Evaluation Platter in Egyptian, Maghrebi & Modern
Standard Arabic—A Triple-Dialect Feast for Hungry Language Models*](https://aclanthology.org/2025.arabicnlp-main.39/) (ArabicNLP 2025) and
releases the dataset, prompt templates, pipeline, training and evaluation code, and LoRA adapters.

| | |
|---|---|
| Dialogues | 30,012 (train 28,500 · test 1,512), 10,004 paragraphs × 3 dialects |
| Varieties | Modern Standard Arabic · Egyptian · Maghrebi |
| Topics | 29 Wikipedia categories |
| Generator / grader | Gemini-2.5-Flash / GPT-4o, chosen by native-speaker evaluation of 5 LLMs |
| Released models | LoRA adapters for 6 open models (1B–24B) |

## Contents

- [The data](#the-data)
- [Fine-tuned adapters](#fine-tuned-adapters)
- [Repository layout](#repository-layout)
- [Setup](#setup)
- [Building dialogues with the pipeline](#building-dialogues-with-the-pipeline)
- [Reproducing the experiments](#reproducing-the-experiments)
- [Results](#results)
- [Citation](#citation)

## The data

The dataset is in [`data/`](data/) and loads without any download:

```python
import pandas as pd

test = pd.read_json("data/shawarmachats_test.jsonl.gz", lines=True)
row = test.iloc[0]
print(row.dialect, "|", row.english_title)
for turn in row.dialogue:
    print(turn["speaker"], ":", turn["text"])
```

Each row is one dialogue: `dialect`, Wikipedia `context`, the parsed `dialogue` turns, and the
`prompt` / `target` pair used for fine-tuning. Fields and statistics are in the
[data card](data/README.md). The Hugging Face version
([`arabic_multi_dialect_dialogue`](https://huggingface.co/datasets/Kamyar-zeinalipour/arabic_multi_dialect_dialogue)) also keeps every intermediate column of the pipeline
(raw generations, grades, reasons, repairs).

## Fine-tuned adapters

LoRA adapters trained on the train split, in the [ShawarmaChats collection](https://huggingface.co/collections/Kamyar-zeinalipour/shawarmachats-arabicnlp-2025-6af4656eda045ed7cfc001d3):

| Base model | Adapter | Grader score (base → fine-tuned) |
|---|---|---|
| [Llama-3.2-1B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct) | [ShawarmaChats-Llama-3.2-1B-Instruct-LoRA](https://huggingface.co/Kamyar-zeinalipour/ShawarmaChats-Llama-3.2-1B-Instruct-LoRA) | 1.003 → **1.103** |
| [Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) | [ShawarmaChats-Llama-3.2-3B-Instruct-LoRA](https://huggingface.co/Kamyar-zeinalipour/ShawarmaChats-Llama-3.2-3B-Instruct-LoRA) | 1.058 → **1.389** |
| [Mistral-7B-Instruct-v0.3](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3) | [ShawarmaChats-Mistral-7B-Instruct-v0.3-LoRA](https://huggingface.co/Kamyar-zeinalipour/ShawarmaChats-Mistral-7B-Instruct-v0.3-LoRA) | 1.186 → **3.302** |
| [Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | [ShawarmaChats-Llama-3.1-8B-Instruct-LoRA](https://huggingface.co/Kamyar-zeinalipour/ShawarmaChats-Llama-3.1-8B-Instruct-LoRA) | 1.440 → **3.172** |
| [Mistral-Nemo-Instruct-2407](https://huggingface.co/mistralai/Mistral-Nemo-Instruct-2407) | [ShawarmaChats-Mistral-Nemo-Instruct-2407-LoRA](https://huggingface.co/Kamyar-zeinalipour/ShawarmaChats-Mistral-Nemo-Instruct-2407-LoRA) | 1.313 → **3.345** |
| [Mistral-Small-24B-Instruct-2501](https://huggingface.co/mistralai/Mistral-Small-24B-Instruct-2501) | [ShawarmaChats-Mistral-Small-24B-Instruct-2501-LoRA](https://huggingface.co/Kamyar-zeinalipour/ShawarmaChats-Mistral-Small-24B-Instruct-2501-LoRA) | 1.854 → **3.607** |


```bash
python inference/generate.py --model mistralai/Mistral-7B-Instruct-v0.3 \
  --adapter Kamyar-zeinalipour/ShawarmaChats-Mistral-7B-Instruct-v0.3-LoRA --limit 5
```

## Repository layout

```
Shawarma-Chats/
├── data/                       train/test dialogues + data card
├── pipeline/                   how the corpus was built (Section 3)
│   ├── prompts.py              generation, grading and repair prompts for each dialect
│   ├── llm_apis.py             GPT-4o, Gemini, DeepSeek, Qwen, Mistral (OpenAI-compatible)
│   ├── generate.py             paragraph -> dialogue in 3 dialects
│   ├── grade.py                dialogue -> rating A–D + reason
│   ├── repair.py               rewrite non-A dialogues from the grader's reason (2 rounds)
│   └── finalize.py             keep A-rated versions, list the rest for human correction
├── training/                   LoRA fine-tuning (train.py, utils.py)
├── configs/                    training settings, DeepSpeed ZeRO-3 config
├── inference/generate.py       generate test dialogues with a base model or adapter
├── evaluation/
│   ├── metrics.py              ROUGE-L, BLEU, BERTScore
│   ├── grade_outputs.py        GPT-4o grader score (A–D -> 4–1)
│   └── summarize.py            Table 4 and per-dialect tables
├── paper_results/results.csv   every number in Table 4 and Appendix E
└── scripts/                    build_corpus.sh, train_all.sh, infer_all.sh, evaluate_all.sh
```

## Setup

```bash
git clone https://github.com/KamyarZeinalipour/Shawarma-Chats.git
cd Shawarma-Chats
conda create -n shawarma python=3.11 -y && conda activate shawarma

pip install -r requirements.txt        # training and inference (versions used in the paper)
pip install -r requirements-eval.txt   # automatic metrics
pip install -r requirements-api.txt    # pipeline and LLM grader
cp .env.example .env                   # add API keys for the pipeline / grader
```

The Llama and Mistral models are gated on the Hugging Face Hub: accept their terms on each model
page and run `huggingface-cli login`.

## Building dialogues with the pipeline

Give it a CSV with a `Text` column of Arabic paragraphs:

```bash
scripts/build_corpus.sh paragraphs.csv work/
```

This runs the four steps in `pipeline/` (generate → grade → repair → finalize). Each step saves
after every row and resumes if interrupted. Rows marked `source = human` in
`work/4_final.csv` still need a native speaker. Applied to the released corpus, the selection rule
in `finalize.py` reproduces the published dialogue for 99.96% of automatically resolved items.

## Reproducing the experiments

```bash
scripts/train_all.sh      # LoRA fine-tuning of the six models (DeepSpeed ZeRO-3)
scripts/infer_all.sh      # base and fine-tuned generations on the test split -> results/raw/
scripts/evaluate_all.sh   # metrics + GPT-4o grader + summary table
```

Training settings (`configs/train_lora.json`, as stored with the released adapters):
LoRA r = 64, α = 128, dropout 0.1 on all attention and MLP projections plus `embed_tokens` and
`lm_head`; 3 epochs; AdamW, learning rate 1e-4, cosine schedule, no warm-up, weight decay 1e-4;
2 sequences per GPU, 2 gradient-accumulation steps, packing to 3,500 tokens; bf16, Flash
Attention 2, seed 100. Decoding: temperature 0.8, top-p 0.95, top-k 50, repetition penalty 1.1,
up to 1,024 new tokens.

To see the paper's numbers without a GPU:

```bash
python evaluation/summarize.py --paper
```

## Results

Test split (1,512 dialogues), base instruction-tuned model vs. the same model after LoRA
fine-tuning (Table 4). Grader: GPT-4o rating mapped A = 4 … D = 1.

| Model | ROUGE-L | | BLEU | | BERTScore F1 | | Grader (1–4) | |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| | Base | FT | Base | FT | Base | FT | Base | FT |
| Llama-3.2-1B-Instruct | 0.220 | **0.318** | 0.088 | **0.198** | 0.763 | **0.767** | 1.003 | **1.103** |
| Llama-3.2-3B-Instruct | 0.298 | **0.310** | 0.101 | **0.194** | 0.797 | 0.745 | 1.058 | **1.389** |
| Mistral-7B-Instruct-v0.3 | 0.304 | **0.443** | 0.182 | **0.286** | 0.767 | **0.856** | 1.186 | **3.302** |
| Llama-3.1-8B-Instruct | 0.337 | **0.433** | 0.152 | **0.279** | 0.821 | **0.856** | 1.440 | **3.172** |
| Mistral-Nemo-Instruct-2407 | 0.246 | **0.439** | 0.141 | **0.284** | 0.772 | **0.857** | 1.313 | **3.345** |
| Mistral-Small-24B-Instruct-2501 | 0.413 | **0.443** | 0.257 | **0.287** | 0.838 | **0.857** | 1.854 | **3.607** |

Per-dialect results (Appendix E) and rating counts are in
[`paper_results/results.csv`](paper_results/results.csv).

## Citation

```bibtex
@inproceedings{zeinalipour-etal-2025-shawarma,
    title = "Shawarma Chats: A Benchmark Exact Dialogue {\&} Evaluation Platter in {E}gyptian, {M}aghrebi {\&} {M}odern {S}tandard {A}rabic{---}{A} Triple-Dialect Feast for Hungry Language Models",
    author = "Zeinalipour, Kamyar  and
      Saad, Mohamed Zaky  and
      Attafi, Oumaima  and
      Maggini, Marco  and
      Gori, Marco",
    editor = "Darwish, Kareem  and
      Ali, Ahmed  and
      Abu Farha, Ibrahim  and
      Touileb, Samia  and
      Zitouni, Imed  and
      Abdelali, Ahmed  and
      Al-Ghamdi, Sharefah  and
      Alkhereyf, Sakhar  and
      Zaghouani, Wajdi  and
      Khalifa, Salam  and
      AlKhamissi, Badr  and
      Almatham, Rawan  and
      Hamed, Injy  and
      Alyafeai, Zaid  and
      Alowisheq, Areeb  and
      Inoue, Go  and
      Mrini, Khalil  and
      Alshammari, Waad",
    booktitle = "Proceedings of The Third {A}rabic Natural Language Processing Conference",
    month = nov,
    year = "2025",
    address = "Suzhou, China",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.arabicnlp-main.39/",
    doi = "10.18653/v1/2025.arabicnlp-main.39",
    pages = "472--524",
    ISBN = "979-8-89176-352-4"
}
```

## License

Code: [Apache License 2.0](LICENSE). Data: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/),
as it is derived from Wikipedia. Adapters follow the license of their base model.

Questions or problems: please [open an issue](https://github.com/KamyarZeinalipour/Shawarma-Chats/issues).
