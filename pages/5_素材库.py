import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from app.db import init_db
from app.services.story_service import list_stories, delete_story, update_story

st.set_page_config(page_title="素材库", layout="wide")
init_db()

st.title("素材库")
st.caption("所有已保存的素材。")

stories = list_stories()
if not stories:
    st.info("暂无素材，先去「经历打磨器」生成并保存。")
    st.stop()

for s in stories:
    with st.expander(f"#{s.id} {s.title}  ·  {s.created_at}"):
        st.write("**原始描述**")
        st.write(s.raw_text)

        if s.target_role or s.target_level or s.jd_keywords:
            st.write(
                f"**目标**：{s.target_role or '—'} / {s.target_level or '—'} / "
                f"关键词：{s.jd_keywords or '—'}"
            )

        if s.tags:
            st.write("**标签**：", "、".join(s.tags))

        if s.facts_json:
            st.markdown("**事实抽取**")
            st.json(s.facts_json)

        if s.optimized_bullets_json:
            st.markdown("**打磨版本**")
            for v in s.optimized_bullets_json:
                st.markdown(f"*{v.get('tone', '')}*")
                for b in v.get("bullets", []):
                    st.markdown(f"- {b}")

        if s.questions_json:
            st.markdown("**待补充追问**")
            for q in s.questions_json:
                st.markdown(f"- {q}")

        with st.form(f"edit_form_{s.id}"):
            new_title = st.text_input("标题", value=s.title, key=f"title_{s.id}")
            new_tags = st.text_input("标签", value=", ".join(s.tags), key=f"tags_{s.id}")
            save = st.form_submit_button("保存修改")
        if save:
            update_story(
                s.id,
                title=new_title,
                tags=[t.strip() for t in new_tags.split(",") if t.strip()],
            )
            st.success("已更新")
            st.rerun()

        if st.button(f"删除素材 #{s.id}", key=f"del_story_{s.id}"):
            delete_story(s.id)
            st.rerun()
