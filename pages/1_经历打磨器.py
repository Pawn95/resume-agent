import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from app.db import init_db
from app.agents.bullet_optimizer import optimize_bullet
from app.services.story_service import create_story

st.set_page_config(page_title="经历打磨器", layout="wide")
init_db()

st.title("经历打磨器")
st.caption("把口述的工作内容，优化成可写入简历的表达。")

with st.form("optimize_form"):
    raw_text = st.text_area(
        "粘贴一段工作内容",
        height=200,
        placeholder="例如：我在支付项目里重构了订单服务，用了消息队列和分库分表，QPS 从 1k 提升到 5k。",
    )
    col1, col2 = st.columns(2)
    with col1:
        target_role = st.text_input("目标岗位", value="产品经理（互联网）", disabled=True)
        target_level = st.selectbox("目标级别", ["", "初级", "中级", "高级", "专家"], index=2)
    with col2:
        jd_keywords = st.text_input("JD 关键词", placeholder="如：B端产品, 数据分析, AI 产品")
    submitted = st.form_submit_button("优化为简历表达", type="primary")

if submitted:
    if not raw_text.strip():
        st.error("请先输入工作内容。")
    else:
        with st.spinner("AI 正在优化..."):
            try:
                result = optimize_bullet(
                    raw_text=raw_text,
                    target_role=target_role,
                    target_level=target_level,
                    jd_keywords=jd_keywords,
                )
                st.session_state["opt_result"] = result.model_dump()
                st.session_state["opt_raw_text"] = raw_text
                st.session_state["opt_target_role"] = target_role
                st.session_state["opt_target_level"] = target_level
                st.session_state["opt_jd_keywords"] = jd_keywords
            except Exception as e:
                st.error(f"优化失败：{e}")

if "opt_result" in st.session_state:
    result = st.session_state["opt_result"]

    # 事实抽取：以彩色标签卡片展示，替代原 JSON 树
    st.markdown("### 事实抽取")
    FACT_LABELS = [
        ("action", "行动"),
        ("object", "对象"),
        ("method", "方法"),
        ("result", "结果"),
        ("missing", "缺失（需补充）"),
    ]
    st.markdown(
        """
        <style>
        .fact-row { display: flex; align-items: flex-start; gap: 8px; margin: 8px 0; flex-wrap: wrap; }
        .fact-label { font-weight: 600; min-width: 96px; line-height: 1.9; }
        .chip {
            display: inline-block; padding: 3px 12px; margin: 3px 4px 3px 0;
            border-radius: 999px; font-size: 0.9em;
            background: rgba(99, 158, 255, 0.15);
            border: 1px solid rgba(99, 158, 255, 0.45);
        }
        .chip-missing {
            background: rgba(255, 140, 60, 0.15);
            border: 1px solid rgba(255, 140, 60, 0.5);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    facts = result.get("facts", {})
    for key, label in FACT_LABELS:
        items = facts.get(key) or []
        if not items:
            continue
        cls = "chip chip-missing" if key == "missing" else "chip"
        chips = "".join(f'<span class="{cls}">{i}</span>' for i in items)
        st.markdown(
            f'<div class="fact-row"><span class="fact-label">{label}</span>{chips}</div>',
            unsafe_allow_html=True,
        )
    if not any(facts.get(k) for k, _ in FACT_LABELS):
        st.caption("本次未抽取到事实信息。")

    st.markdown("### 可写入简历的版本")
    for v in result["versions"]:
        st.markdown(f"**{v['tone']}**")
        for b in v["bullets"]:
            st.markdown(f"- {b}")

    st.markdown("### 需要你补充的信息")
    for q in result["questions"]:
        st.markdown(f"- {q}")

    st.markdown("---")
    st.markdown("### 保存到素材库")
    default_title = st.session_state.get("opt_target_role") or "新素材"

    with st.form("save_story_form"):
        title = st.text_input("素材标题", value=default_title)
        tags = st.text_input("标签，逗号分隔", placeholder="如：支付, 高并发, 后端")
        save = st.form_submit_button("保存到素材库", type="primary")

    if save:
        try:
            story = create_story(
                title=title,
                raw_text=st.session_state.get("opt_raw_text", ""),
                target_role=st.session_state.get("opt_target_role", ""),
                target_level=st.session_state.get("opt_target_level", ""),
                jd_keywords=st.session_state.get("opt_jd_keywords", ""),
                facts_json=result["facts"],
                optimized_bullets_json=result["versions"],
                questions_json=result["questions"],
                tags=[t.strip() for t in tags.split(",") if t.strip()],
            )
            st.success(f"已保存为素材 #{story.id}：{story.title}")
        except Exception as e:
            st.error(f"保存失败：{e}")
