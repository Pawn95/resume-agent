import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from app.db import init_db
from app.services.version_service import create_version, list_versions, delete_version
from app.services.job_service import list_jobs, get_job
from app.services.story_service import list_stories

st.set_page_config(page_title="版本管理", layout="wide")
init_db()

st.title("版本保存")
st.caption("把当前 JD + 素材 + 打磨结果保存成版本快照。")


def _parse_id(label: str) -> int:
    return int(label.split()[0].replace("#", ""))


jobs = list_jobs()
stories = list_stories()

with st.form("version_form"):
    name = st.text_input("版本名称", placeholder="如：2026-09-27 某公司后端岗")
    job_label = st.selectbox(
        "关联岗位（可选）",
        ["（不关联）"] + [f"#{j.id} {j.company or '—'} / {j.title or '—'}" for j in jobs],
    )
    story_labels = st.multiselect(
        "关联素材（可多选）",
        [f"#{s.id} {s.title}" for s in stories],
    )
    notes = st.text_area("备注（可选）", height=80)
    submitted = st.form_submit_button("保存版本", type="primary")

if submitted:
    if not name.strip():
        st.error("请填写版本名称。")
    else:
        job_id = None if job_label == "（不关联）" else _parse_id(job_label)
        selected_ids = [_parse_id(l) for l in story_labels]

        job = get_job(job_id) if job_id else None
        parsed_jd_json = job.parsed_json if job else {}

        bullet_opt = []
        for s in stories:
            if s.id in selected_ids:
                for v in s.optimized_bullets_json or []:
                    bullet_opt.append({
                        "story_id": s.id,
                        "tone": v.get("tone"),
                        "bullets": v.get("bullets", []),
                    })

        try:
            v = create_version(
                name=name,
                job_id=job_id,
                story_ids=selected_ids,
                bullet_optimization_json=bullet_opt,
                parsed_jd_json=parsed_jd_json,
                interview_pack_json={},
                notes=notes,
            )
            st.success(f"已保存版本 #{v.id}：{v.name}")
        except Exception as e:
            st.error(f"保存失败：{e}")

st.markdown("---")
st.markdown("### 已保存版本")
versions = list_versions()
if not versions:
    st.info("暂无版本。")

for v in versions:
    with st.expander(f"#{v.id} {v.name}  ·  {v.created_at}"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("**关联岗位**：", v.job_id or "—")
            st.write("**关联素材**：", v.story_ids or [])
            if v.notes:
                st.write("**备注**：", v.notes)
        with col2:
            if st.button("删除", key=f"del_version_{v.id}"):
                delete_version(v.id)
                st.rerun()

        st.markdown("**JD 解析快照**")
        st.json(v.parsed_jd_json)

        st.markdown("**打磨结果快照**")
        st.json(v.bullet_optimization_json)

        if st.button("加载此版本到当前会话", key=f"load_version_{v.id}"):
            st.session_state["loaded_version"] = {
                "id": v.id,
                "name": v.name,
                "parsed_jd_json": v.parsed_jd_json,
                "bullet_optimization_json": v.bullet_optimization_json,
                "story_ids": v.story_ids,
            }
            st.success(f"已加载版本 #{v.id} 到 session_state['loaded_version']")
