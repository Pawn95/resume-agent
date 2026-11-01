import json
import os
import re
from typing import Type, TypeVar

import litellm
from pydantic import BaseModel

from app.config import LLM_MODEL, LLM_TEMPERATURE

T = TypeVar("T", bound=BaseModel)


def _extract_json(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            return json.loads(text[start:end + 1])
        raise ValueError(f"无法从 LLM 输出中解析 JSON：\n{text[:500]}")


def call_llm_json(
    system_prompt: str,
    user_prompt: str,
    schema: Type[T],
    model: str | None = None,
) -> T:
    # 每次调用时读取，便于页面上保存的配置立即生效
    model = model or os.getenv("LLM_MODEL", LLM_MODEL)

    resp = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=LLM_TEMPERATURE,
    )

    content = resp.choices[0].message.content
    data = _extract_json(content)
    return schema.model_validate(data)
