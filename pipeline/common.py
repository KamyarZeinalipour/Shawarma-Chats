"""Shared helpers: dialect names, prompt lookup, JSON clean-up and grade parsing."""
from __future__ import annotations

import json
import re

import pandas as pd

import prompts as P

DIALECTS = ["std", "egy", "mag"]  # Modern Standard, Egyptian, Maghrebi
DIALECT_NAMES = {"std": "msa", "egy": "egyptian", "mag": "maghrebi"}

GENERATION = {"std": P.standard_prompt, "egy": P.egyptian_prompt, "mag": P.maghrebi_prompt}
GRADING = {"std": P.standard_evaluation_prompt, "egy": P.egy_evaluation_prompt, "mag": P.mag_evaluation_prompt}
REPAIR = {"std": P.std_fix_prompt, "egy": P.egy_fix_prompt, "mag": P.mag_fix_prompt}

_FENCE = re.compile(r"^\s*```(?:json)?\s*|\s*```\s*$")
_REFERENCE_LINE = re.compile(r'^\s*"reference"\s*:.*$\n?', re.MULTILINE)
_JSON_BLOCK = re.compile(r"(?:```(?:json)?\s*)?(\{[\s\S]*\})(?:\s*```)?", re.IGNORECASE)


def strip_fence(text) -> str:
    return _FENCE.sub("", str(text)).strip()


def strip_references(text) -> str:
    """Remove the per-turn `reference` fields the generator adds (the source sentence of each turn)."""
    raw = strip_fence(text)
    try:
        data = json.loads(raw)
        for turn in data.get("dialogue", []):
            turn.pop("reference", None)
        return json.dumps(data, ensure_ascii=False, indent=2)
    except (json.JSONDecodeError, AttributeError):
        # Malformed JSON: drop the reference lines and the trailing comma they leave behind.
        cleaned = _REFERENCE_LINE.sub("", raw)
        return re.sub(r',(\s*\n\s*\})', r"\1", cleaned)


def grading_prompt(dialect: str, text: str, dialogue: str) -> str:
    return GRADING[dialect].replace("{text}", str(text)).replace("{dialogue}", str(dialogue))


def parse_grade(raw):
    """(rating, reason) from the grader's JSON reply, or (None, None)."""
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return None, None
    match = _JSON_BLOCK.search(str(raw))
    if not match:
        return None, None
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError:
        return None, None
    if isinstance(data, dict) and "annotation" in data:
        first = (data["annotation"] or [{}])[0]
        return first.get("rating"), first.get("reason")
    return data.get("rating"), data.get("reason")
