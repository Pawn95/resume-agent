import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from app.db import init_db
from app.agents.jd_parser import parse_jd
from app.services.job_service import create_job, list_jobs, delete_job

st.set_page_config(page_title="JD 解析", layout="wide")
init_db()

st.title("JD 解析")
st.caption("粘贴 JD，解析成结构化字段。")

with st.form("jd_form"):
    jd_text = st.text_area("粘贴 JD 原文", height=280)
    submitted = st.form_submit_button("解析 JD", type="primary")

if submitted:
    if not jd_text.strip():
        st.error("请先粘贴 JD。")
    else:
        with st.spinner("AI 正在解析..."):
            try:
                parsed = parse_jd(jd_text)
                st.session_state["jd_parsed"] = parsed.model_dump()
                st.session_state["jd_text"] = jd_text
            except Exception as e:
                st.error(f"解析失败：{e}")

if "jd_parsed" in st.session_state:
    parsed = st.session_state["jd_parsed"]

    st.markdown("### 解析结果")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**公司**：", parsed.get("company") or "—")
        st.write("**岗位**：", parsed.get("title") or "—")
        st.write("**级别**：", parsed.get("seniority") or "—")
        st.write("**领域**：", parsed.get("domain") or "—")
    with col2:
        st.write("**语气**：", parsed.get("tone") or "—")

    st.markdown("**硬性要求**")
    for x in parsed.get("must_have", []):
        st.markdown(f"- {x}")

    st.markdown("**加分项**")
    for x in parsed.get("nice_to_have", []):
        st.markdown(f"- {x}")

    st.markdown("**职责**")
    for x in parsed.get("responsibilities", []):
        st.markdown(f"- {x}")

    st.markdown("**关键词**")
    st.write("、".join(parsed.get("keywords", [])))

    st.markdown("---")
    if st.button("保存为岗位", type="primary"):
        try:
            job = create_job(
                jd_text=st.session_state.get("jd_text", ""),
                parsed_json=parsed,
            )
            st.success(f"已保存为岗位 #{job.id}：{job.company or '未填公司'} / {job.title or '未填岗位'}")
        except Exception as e:
            st.error(f"保存失败：{e}")

st.markdown("---")
st.markdown("### 已保存的岗位")
jobs = list_jobs()
if not jobs:
    st.info("暂无岗位。")
for j in jobs:
    with st.expander(f"#{j.id} {j.company or '—'} / {j.title or '—'}"):
        st.caption(str(j.created_at))
        st.json(j.parsed_json)
        if st.button(f"删除岗位 #{j.id}", key=f"del_job_{j.id}"):
            delete_job(j.id)
            st.rerun()
