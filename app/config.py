import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data"
if not DATA_DIR.exists():
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
    except OSError:
        # 兼容沙箱环境：目录已存在时部分拦截器会误报 EEXIST/PermissionError
        if not DATA_DIR.exists():
            raise

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'resume.db'}")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek/deepseek-chat")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
