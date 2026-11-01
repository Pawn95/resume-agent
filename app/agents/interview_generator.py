from pathlib import Path
from typing import List, Dict, Any

from app.schemas import InterviewPack
from app.services.llm import call_llm_json

PROMPT_PATH = Path(__file__).resolve().parent.parent.parent / "prompts" / "interview_generator.txt"


def generate_interview_pack(
    parsed_jd: dict,
    stories: List[Dict[str, Any]],
) -> InterviewPack:
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    story_blocks = []
    for s in stories:
        bullets = []
        for v in s.get("optimized_bullets_json") or []:
            bullets.extend(v.get("bullets", []))
        story_blocks.append(
            f"[story_id={s['id']}] {s['title']}\n"
            f"原始描述：{s['raw_text']}\n"
            f"简历 bullet：{bullets}"
        )
    stories_text = "\n\n".join(story_blocks) if story_blocks else "（无可用 Story）"

    user_prompt = f"""JD 解析结果：
{parsed_jd}

候选人 Story：
{stories_text}

请严格按 JSON 结构输出。问题必须引用具体 story_id 或 JD 的具体要求。"""

    return call_llm_json(system_prompt, user_prompt, InterviewPack)
