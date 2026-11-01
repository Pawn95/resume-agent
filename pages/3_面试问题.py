import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from app.db import init_db
from app.agents.interview_generator import generate_interview_pack
from app.services.job_service import list_jobs, get_job
from app.services.story_service import list_stories
from app.services.interview_service import create_pack, list_packs, delete_pack

st.set_page_config(page_title="面试问题", layout="wide")
init_db()

st.title("面试问题生成")
st.caption("基于 JD + 素材生成面试问题包。")

jobs = list_jobs()
stories = list_stories()

if not jobs:
    st.warning("先去「JD 解析」页保存一个岗位。")
    st.stop()

if not stories:
    st.warning("先去「经历打磨器」页保存至少一个素材。")
    st.stop()

job_options = {f"#{j.id} {j.company or '—'} / {j.title or '—'}": j.id for j in jobs}
story_options = {f"#{s.id} {s.title}": s.id for s in stories}

with st.form("interview_form"):
    job_label = st.selectbox("选择岗位", list(job_options.keys()))
    story_labels = st.multiselect("选择素材（可多选）", list(story_options.keys()))
    submitted = st.form_submit_button("生成面试问题包", type="primary")

if submitted:
    if not story_labels:
        st.error("至少选择一个素材。")
    else:
        job_id = job_options[job_label]
        job = get_job(job_id)
        selected_story_ids = [story_options[l] for l in story_labels]

        selected_stories = []
        for s in stories:
            if s.id in selected_story_ids:
                selected_stories.append({
                    "id": s.id,
                    "title": s.title,
                    "raw_text": s.raw_text,
                    "optimized_bullets_json": s.optimized_bullets_json,
                })

        with st.spinner("AI 正在生成问题..."):
            try:
                pack = generate_interview_pack(job.parsed_json, selected_stories)
                st.session_state["pack"] = pack.model_dump()
                st.session_state["pack_job_id"] = job_id
                st.session_state["pack_story_ids"] = selected_story_ids
            except Exception as e:
                st.error(f"生成失败：{e}")

if "pack" in st.session_state:
    pack = st.session_state["pack"]
    st.markdown(f"### 共 {pack.get('total_questions', 0)} 题")

    for cat in pack.get("categories", []):
        st.markdown(f"#### {cat['name']}")
        for q in cat.get("questions", []):
            with st.expander(q["question"]):
                st.write("**考察点**：", q.get("intent", ""))
                st.write("**回答框架**：", q.get("answer_framework", ""))
                st.write("**关联素材**：", q.get("related_story_ids", []))
                st.write("**追问**：")
                for f in q.get("followups", []):
                    st.markdown(f"- {f}")
                st.write("**危险信号**：")
                for r in q.get("red_flags", []):
                    st.markdown(f"- {r}")

    st.markdown("---")
    if st.button("保存面试问题包", type="primary"):
        try:
            saved = create_pack(
                job_id=st.session_state.get("pack_job_id"),
                story_ids=st.session_state.get("pack_story_ids", []),
                pack_json=pack,
            )
            st.success(f"已保存为面试包 #{saved.id}")
        except Exception as e:
            st.error(f"保存失败：{e}")

st.markdown("---")
st.markdown("### 已保存的面试包")
packs = list_packs()
if not packs:
    st.info("暂无面试包。")
for p in packs:
    with st.expander(f"#{p.id} 岗位={p.job_id} 素材={p.story_ids}"):
        st.caption(str(p.created_at))
        st.json(p.pack_json)
        if st.button(f"删除面试包 #{p.id}", key=f"del_pack_{p.id}"):
            delete_pack(p.id)
            st.rerun()
