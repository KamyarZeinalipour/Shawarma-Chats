# ShawarmaChats data

| File | Paragraphs | Dialogues |
|---|---:|---:|
| `shawarmachats_train.jsonl.gz` | 9,500 | 28,500 |
| `shawarmachats_test.jsonl.gz` | 504 | 1,512 |

Every Arabic Wikipedia paragraph has one six-turn dialogue in each of the three varieties:
**Modern Standard Arabic** (`msa`), **Egyptian** (`egyptian`) and **Maghrebi** (`maghrebi`),
so each split is balanced across dialects (train 9,500 × 3, test 504 × 3). This is the split
used for all results in the paper. The same data, with all intermediate pipeline columns, is on the Hugging Face Hub as
[`Kamyar-zeinalipour/arabic_multi_dialect_dialogue`](https://huggingface.co/datasets/Kamyar-zeinalipour/arabic_multi_dialect_dialogue).

## Loading

```python
import pandas as pd

test = pd.read_json("data/shawarmachats_test.jsonl.gz", lines=True)
row = test.iloc[0]
print(row.dialect, row.english_title)
for turn in row.dialogue:
    print(turn["speaker"], turn["text"])
```

## Fields

| Field | Description |
|---|---|
| `id` | `train-00000` … / `test-00000` … |
| `split` | `train` or `test` |
| `dialect` | `msa`, `egyptian` or `maghrebi` |
| `page_id`, `url` | Arabic Wikipedia page id and link |
| `arabic_title`, `english_title` | Article titles |
| `category` | One of 29 topic categories (Entertainment, History, Geography, Science, …) |
| `context` | The Wikipedia paragraph the dialogue is grounded in (median 185 words) |
| `dialogue` | List of turns `{"speaker": "A" or "B", "text": ...}`; 6 turns in 99.7% of dialogues |
| `prompt` | The generation prompt for this paragraph and dialect (model input in fine-tuning) |
| `target` | The gold dialogue as the JSON string the prompt asks for (model output in fine-tuning) |

## How the dialogues were made

1. Gemini-2.5-Flash wrote one dialogue per paragraph and dialect (`pipeline/generate.py`).
2. GPT-4o rated each dialogue A–D with a dialect-specific rubric (`pipeline/grade.py`).
3. Dialogues below A were rewritten using the grader's reason and re-rated, up to two rounds
   (`pipeline/repair.py`).
4. Only A-rated dialogues were kept; the remaining 161 (0.5%) were corrected by native speakers.

Of the final dialogues, 25,771 passed on the first attempt, 3,567 after one repair, 513 after two,
and 161 were corrected by hand.

## License

The data is derived from Arabic Wikipedia and released under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
