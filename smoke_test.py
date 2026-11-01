"""冒烟测试：验证模块导入、DB 初始化、CRUD、Prompt 加载。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

# 1. 导入所有模块
from app.db import init_db, engine
from app import models
from app.schemas import BulletOptimization, ParsedJD, InterviewPack
from app.services.llm import _extract_json
from app.services.story_service import create_story, list_stories, get_story, update_story, delete_story
from app.services.job_service import create_job, list_jobs, get_job, delete_job
from app.services.interview_service import create_pack, list_packs, delete_pack
from app.services.version_service import create_version, list_versions, delete_version
from app.agents.bullet_optimizer import PROMPT_PATH as P1, optimize_bullet  # noqa
from app.agents.jd_parser import PROMPT_PATH as P2, parse_jd  # noqa
from app.agents.interview_generator import PROMPT_PATH as P3, generate_interview_pack  # noqa
print("[1] 模块导入 OK")

# 2. 数据库初始化
init_db()
from sqlalchemy import inspect
tables = set(inspect(engine).get_table_names())
expected = {"story", "job", "interviewpack", "version"}
assert expected.issubset(tables), f"缺表: {expected - tables}"
print(f"[2] DB 初始化 OK，表：{sorted(tables)}")

# 3. Prompt 文件存在且可读
for p in (P1, P2, P3):
    assert p.exists() and len(p.read_text(encoding="utf-8")) > 50, f"prompt 缺失: {p}"
print("[3] Prompt 文件 OK")

# 4. JSON 提取函数
assert _extract_json('{"a": 1}') == {"a": 1}
assert _extract_json('```json\n{"a": 1}\n```') == {"a": 1}
assert _extract_json('前缀 {"a": 1} 后缀') == {"a": 1}
print("[4] JSON 提取 OK")

# 5. CRUD 冒烟测试
s = create_story(title="测试素材", raw_text="我做了支付重构", tags=["测试"])
assert get_story(s.id).title == "测试素材"
update_story(s.id, title="改名素材")
assert get_story(s.id).title == "改名素材"

j = create_job(jd_text="测试 JD", parsed_json={"company": "测试公司", "title": "后端"})
assert get_job(j.id).parsed_json["company"] == "测试公司"

p = create_pack(job_id=j.id, story_ids=[s.id], pack_json={"total_questions": 15})
assert list_packs()[0].pack_json["total_questions"] == 15

v = create_version(name="测试版本", job_id=j.id, story_ids=[s.id],
                   bullet_optimization_json=[{"story_id": s.id, "tone": "保守真实版", "bullets": ["x"]}],
                   parsed_jd_json={"company": "测试公司"})
assert list_versions()[0].name == "测试版本"

# schema 校验
BulletOptimization.model_validate({
    "facts": {"action": [], "object": [], "method": [], "result": [], "missing": []},
    "versions": [{"tone": "保守真实版", "bullets": ["b1"]}],
    "questions": ["q1"],
})
print("[5] CRUD + Schema 校验 OK")

# 6. 清理测试数据
delete_story(s.id); delete_job(j.id); delete_pack(p.id); delete_version(v.id)
assert list_stories() == [] and list_jobs() == []
print("[6] 清理 OK")

print("\n=== 全部冒烟测试通过 ===")
