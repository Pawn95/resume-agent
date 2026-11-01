from pathlib import Path

from app.schemas import ParsedJD
from app.services.llm import call_llm_json

PROMPT_PATH = Path(__file__).resolve().parent.parent.parent / "prompts" / "jd_parser.txt"


def parse_jd(jd_text: str) -> ParsedJD:
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    user_prompt = f"""JD 原文：
{jd_text}

请严格按 JSON 结构输出。"""

    return call_llm_json(system_prompt, user_prompt, ParsedJD)
