# 简历 Agent MVP（第 1 周）

范围：经历打磨器、JD 解析、面试问题生成、版本保存。

## 安装
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 配置 API Key（两种方式任选）
- **推荐：页面配置**。启动后在首页右侧「⚙️ 大模型配置」里粘贴 API 密钥，点「保存配置」，立即生效并持久化到 .env。
- 或手动编辑 `.env`，填入 `DEEPSEEK_API_KEY` / `OPENAI_API_KEY`。

## 运行
```bash
.venv/bin/streamlit run 首页.py        # Windows: .venv\Scripts\streamlit run 首页.py
```

## 页面
- 经历打磨器：口述 → 3 版 bullet → 保存 Story
- JD 解析：JD → 结构化 JSON → 保存 Job
- 面试问题：Job + Story → 面试问题包
- 版本管理：保存/查看/加载/删除版本快照
- 素材库：Story 列表、编辑、删除

## 数据
SQLite 文件位于 `data/resume.db`。
