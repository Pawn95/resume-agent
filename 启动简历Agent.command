#!/bin/bash
# 简历 Agent 一键启动脚本：双击即可运行
cd "$(dirname "$0")"

# 首次运行自动装环境
if [ ! -d .venv ]; then
  echo "首次运行：正在创建虚拟环境并安装依赖（约 2-5 分钟）..."
  /Users/sunchao/.workbuddy/binaries/python/versions/3.13.12/bin/python3 -m venv .venv
  .venv/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
fi

echo "正在启动简历 Agent..."
.venv/bin/streamlit run 首页.py
