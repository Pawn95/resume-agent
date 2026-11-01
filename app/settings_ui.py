"""侧边栏 LLM 配置组件：在页面上填写并保存 API Key，无需手动编辑 .env。"""
import os
from pathlib import Path

import streamlit as st
from dotenv import set_key

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"


def _key_var_for(model: str) -> str:
    if model.startswith("openai/"):
        return "OPENAI_API_KEY"
    if model.startswith("deepseek/"):
        return "DEEPSEEK_API_KEY"
    return "DEEPSEEK_API_KEY"


def render_llm_settings(container=None) -> None:
    box = container if container is not None else st.sidebar
    with box:
        st.markdown("### ⚙️ 大模型配置")
        model = st.text_input(
            "模型",
            value=os.getenv("LLM_MODEL", "deepseek/deepseek-chat"),
            key="cfg_model",
        )
        key_var = _key_var_for(model)
        has_key = bool(os.getenv(key_var)) and os.getenv(key_var) != "your_key_here"
        api_key = st.text_input(
            f"API 密钥（{key_var}）",
            value="",
            type="password",
            key="cfg_key",
            placeholder="已配置 ✔" if has_key else "尚未配置，请粘贴 Key",
        )
        if st.button("保存配置", key="cfg_save", use_container_width=True):
            if not api_key.strip():
                st.warning("请先粘贴 API Key。")
            else:
                if not ENV_PATH.exists():
                    ENV_PATH.touch()
                set_key(str(ENV_PATH), "LLM_MODEL", model.strip())
                set_key(str(ENV_PATH), key_var, api_key.strip())
                # 立即生效，无需重启
                os.environ["LLM_MODEL"] = model.strip()
                os.environ[key_var] = api_key.strip()
                st.success("已保存到 .env，本次会话立即生效。")
