import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from app.db import init_db
from app.settings_ui import render_llm_settings

st.set_page_config(page_title="简历智能体 MVP", layout="wide", page_icon="📝")
init_db()

st.title("简历智能体 MVP")
st.caption("经历打磨器 · JD 解析 · 面试问题 · 版本保存")

col1, col2, col3, col4 = st.columns(4)
col1.metric("模块", "4")
col2.metric("存储", "SQLite")
col3.metric("大模型", "LiteLLM")
col4.metric("用户界面", "Streamlit")

st.markdown("---")
info_col, cfg_col = st.columns([3, 2])
with info_col:
    st.markdown(
        """
### 使用顺序
1. **经历打磨器**：粘贴一段工作内容 → 生成 3 版简历要点 → 保存为素材。
2. **JD 解析**：粘贴 JD → 解析出硬性要求/加分项/关键词 → 保存为岗位。
3. **面试问题**：选择岗位 + 素材 → 生成面试问题包。
4. **版本管理**：把当前 JD + 素材 + 打磨结果保存成版本快照。
5. **素材库**：管理已保存的素材。
        """
    )
with cfg_col:
    render_llm_settings(cfg_col)

st.info("API 密钥支持两种配置方式：在本页右侧「⚙️ 大模型配置」里粘贴保存（推荐），或手动编辑 .env 文件。")
