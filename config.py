"""配置管理"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM 配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")

# 存储配置
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
DB_PATH = os.path.join(DATA_DIR, "reports.db")

# 确保目录存在
for d in [DATA_DIR, REPORTS_DIR, UPLOAD_DIR]:
    os.makedirs(d, exist_ok=True)
