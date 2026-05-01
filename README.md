# 📖 读我 — AI 私人学者代读系统

> 让大模型替你仔细读书。不只给结论，而是带着书里的血肉（案例、故事、实验）详细转述给你。

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![Vercel](https://img.shields.io/badge/Vercel-Ready-black.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ 特性

- 📕 **书名代读** — 输入书名，AI 生成 5000-10000 字详细报告
- 📤 **文件上传** — 支持 PDF / EPUB / TXT，解析原文后代读
- 📝 **结构化报告** — 固定六章节，案例充分、有观点有故事
- 🔍 **案例加厚版** — 可选更详实模式（8000-12000 字）
- 💬 **追问功能** — 对报告任意部分继续深入提问
- 📚 **历史管理** — 保存、搜索、回看所有代读报告
- 🔌 **多模型支持** — DeepSeek、GPT-4o、Claude、Moonshot、通义千问

## 🚀 部署方式

### 方式一：Vercel 部署（推荐，免费公网访问）

适合：分享给别人用，打开链接就能用，不用装任何东西。

```bash
cd vercel
npm i -g vercel
vercel --prod
```

或直接在 [vercel.com](https://vercel.com) 导入 GitHub 仓库，Framework 选 **Other**，Root Directory 填 `vercel`。

> ⚠️ Vercel 版前端直连 LLM API（避免 serverless 超时），用户需在页面填入自己的 API Key。

### 方式二：Streamlit Cloud 部署（免费，自带 API Key）

适合：自己用或小范围分享，API Key 配在服务端。

1. 打开 [share.streamlit.io](https://share.streamlit.io)，GitHub 登录
2. **New app** → 选 `readme-ai` 仓库 → `app.py`
3. **Advanced Settings** 填入：
   ```toml
   OPENAI_API_KEY = "sk-你的key"
   OPENAI_BASE_URL = "https://api.deepseek.com/v1"
   MODEL_NAME = "deepseek-chat"
   ```
4. Deploy → 得到 `xxx.streamlit.app` 链接

### 方式三：本地运行

```bash
git clone https://github.com/1311523821/readme-ai.git
cd readme-ai
pip install -r requirements.txt
cp .env.example .env   # 编辑填入 API Key
streamlit run app.py
```

### 方式四：Docker

```bash
docker build -t readme-ai .
docker run -p 8501:8501 -e OPENAI_API_KEY=sk-xxx readme-ai
```

### 方式五：桌面应用（exe）

```bash
pip install pywebview
python desktop.py
```

打包成 exe：
```bash
pip install pyinstaller
pyinstaller --onefile --add-data "app.py:." --add-data "engine.py:." --add-data "parsers.py:." --add-data "storage.py:." --add-data "config.py:." desktop.py
```

## 📋 代读报告结构

每份报告严格按以下六章展开：

| # | 章节 | 说明 |
|---|------|------|
| 1 | 🎯 这本书到底在解决什么问题？ | 核心问题 + 作者起心动念的事件 |
| 2 | 🔗 核心主张与论证链条 | 3-5 个主张，每个配书中案例/实验 |
| 3 | 💡 最颠覆直觉的 3 个观点 | 反常识观点 + 关键实验详细描述 |
| 4 | 📖 如果只记住一个故事 | 全书最精彩故事的微型小说式转述 |
| 5 | 🤔 我可能会质疑的地方 | 逻辑漏洞、幸存者偏差等批判分析 |
| 6 | 🛠️ 与我生活的接口 | 普通人能立刻用的行动建议 |

## 🔧 支持的模型

| 服务商 | Base URL | 推荐模型 | 说明 |
|--------|----------|----------|------|
| DeepSeek | `api.deepseek.com/v1` | `deepseek-chat` | 便宜好用，推荐 |
| OpenAI | `api.openai.com/v1` | `gpt-4o` | 效果最好 |
| Moonshot | `api.moonshot.cn/v1` | `moonshot-v1-128k` | Kimi，中文好 |
| 通义千问 | `dashscope.aliyuncs.com/...` | `qwen-plus` | 阿里云 |
| Anthropic | `api.anthropic.com/v1` | `claude-3-5-sonnet` | Claude |

## 🏗️ 项目结构

```
readme-ai/
├── app.py                  # Streamlit 主界面
├── engine.py               # 代读引擎（提示词 + LLM 调用）
├── parsers.py              # 文件解析（PDF/EPUB/TXT）
├── storage.py              # 存储（SQLite + Markdown）
├── config.py               # 配置管理
├── desktop.py              # 桌面应用入口（pywebview）
├── Dockerfile              # Docker 部署
├── requirements.txt        # Python 依赖
├── .streamlit/             # Streamlit 配置
├── .env.example            # 环境变量模板
├── vercel/                 # ← Vercel 部署版（独立）
│   ├── api/index.py        #   文件解析 API
│   ├── public/index.html   #   前端单页应用
│   ├── vercel.json         #   Vercel 配置
│   └── requirements.txt    #   Python 依赖
└── data/                   # 报告存储目录
```

## 📌 路线图

- [ ] V1.1 — 知识库沉淀：自动解析为结构化笔记（YAML + 标签）
- [ ] V1.2 — 智能问答：基于书库回答问题，引用多本书
- [ ] V2.0 — 跨书对话：让不同书的观点互相辩论
- [ ] V2.1 — 批判模式：一键生成对一本书的全盘反驳

## 📄 License

MIT License
