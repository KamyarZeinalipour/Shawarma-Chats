"""One `chat()` call for the five API models compared in the paper.

All five are reached through OpenAI-compatible endpoints, so only the `openai` package is needed.
Keys are read from the environment or a `.env` file in the repository root:
OPENAI_API_KEY, GEMINI_API_KEY, DEEPSEEK_API_KEY, QWEN_API_KEY, MISTRAL_API_KEY.
"""
from __future__ import annotations

import os

from openai import OpenAI

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

SYSTEM_PROMPT = "You are a linguistics expert with over 20 years of experience in Arabic dialectology."

# short name -> (base_url, key variable, default model id)
MODELS = {
    "gpt-4o": (None, "OPENAI_API_KEY", "gpt-4o"),
    "gemini-2.5-flash": ("https://generativelanguage.googleapis.com/v1beta/openai/", "GEMINI_API_KEY", "gemini-2.5-flash"),
    "deepseek-chat": ("https://api.deepseek.com", "DEEPSEEK_API_KEY", "deepseek-chat"),
    "qwen-plus": ("https://dashscope-intl.aliyuncs.com/compatible-mode/v1", "QWEN_API_KEY", "qwen-plus"),
    "mistral-large": ("https://api.mistral.ai/v1", "MISTRAL_API_KEY", "mistral-large-latest"),
}


def chat(model: str, prompt: str, model_id: str | None = None) -> str:
    base_url, key_name, default_id = MODELS[model]
    key = os.getenv(key_name)
    if not key:
        raise RuntimeError(f"Set {key_name} in your environment or in .env (see .env.example).")
    client = OpenAI(api_key=key, base_url=base_url)
    response = client.chat.completions.create(
        model=model_id or default_id,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
