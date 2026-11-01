from pathlib import Path

from app.schemas import BulletOptimization
from app.services.llm import call_llm_json

PROMPT_PATH = Path(__file__).resolve().parent.parent.parent / "prompts" / "bullet_optimizer.txt"


def optimize_bullet(
    raw_text: str,
    target_role: str = "",
    target_level: str = "",
    jd_keywords: str = "",
) -> BulletOptimization:
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    user_prompt = f"""原始描述：
{raw_text}

目标岗位：{target_role}
目标级别：{target_level}
JD关键词：{jd_keywords}

请严格按 JSON 结构输出。"""

    return call_llm_json(system_prompt, user_prompt, BulletOptimization)
