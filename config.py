"""配置管理"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM 配置 - 优先读 Streamlit Secrets，再读环境变量，最后用默认值
def _get(key: str, default: str = "") -> str:
    """从 Streamlit secrets 或环境变量读取配置"""
    try:
        import streamlit as st
        val = st.secrets.get(key)
        if val:
            return str(val)
    except Exception:
        pass
    return os.getenv(key, default)

OPENAI_API_KEY = _get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = _get("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = _get("MODEL_NAME", "gpt-4o")

# 存储配置
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
DB_PATH = os.path.join(DATA_DIR, "reports.db")

# 确保目录存在
for d in [DATA_DIR, REPORTS_DIR, UPLOAD_DIR]:
    os.makedirs(d, exist_ok=True)
