# 📖 读我 — AI 私人学者代读系统

> 让大模型替你仔细读书。不只给结论，而是带着书里的血肉（案例、故事、实验）详细转述给你。

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ 特性

- 📕 **书名代读** — 输入书名，AI 根据知识生成详细代读报告
- 📤 **文件上传** — 支持 PDF / EPUB / TXT，直接解析原文
- 📝 **结构化报告** — 固定六章节结构，案例充分、有观点有故事
- 🔍 **案例加厚版** — 可选更详实的报告模式（8000-12000 字）
- 💬 **追问功能** — 对报告任意部分继续深入提问
- 📚 **历史管理** — 保存、搜索、回看所有代读报告
- 🔌 **灵活接入** — 支持 DeepSeek、GPT-4o、Claude、Moonshot、通义千问等

## 🚀 部署方式

### 方式一：Streamlit Cloud 一键部署（推荐，零成本）

适合：想让别人通过链接直接访问，不用装任何东西。

1. **Fork 本仓库** 到你的 GitHub（点右上角 Fork）

2. 打开 [Streamlit Cloud](https://share.streamlit.io)，用 GitHub 登录

3. 点 **New app**：
   - Repository: 选你 fork 的 `readme-ai`
   - Branch: `main`
   - Main file path: `app.py`

4. 点 **Advanced Settings**，填入：
   ```toml
   OPENAI_API_KEY = "sk-你的key"
   OPENAI_BASE_URL = "https://api.deepseek.com/v1"
   MODEL_NAME = "deepseek-chat"
   ```

5. 点 **Deploy** → 等待 1 分钟 → 完成！

你会得到一个 `xxx.streamlit.app` 的公网链接，分享给别人就能用。

### 方式二：本地运行

```bash
git clone https://github.com/1311523821/readme-ai.git
cd readme-ai
pip install -r requirements.txt
cp .env.example .env   # 编辑 .env 填入 API Key
streamlit run app.py
```

浏览器自动打开 `http://localhost:8501`。

### 方式三：Docker

```bash
docker build -t readme-ai .
docker run -p 8501:8501 -e OPENAI_API_KEY=sk-xxx readme-ai
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

| 服务商 | Base URL | 推荐模型 |
|--------|----------|----------|
| DeepSeek | `https://api.deepseek.com/v1` | `deepseek-chat`（便宜好用） |
| OpenAI | `https://api.openai.com/v1` | `gpt-4o` |
| Moonshot | `https://api.moonshot.cn/v1` | `moonshot-v1-128k` |
| 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-plus` |
| Anthropic | `https://api.anthropic.com/v1` | `claude-3-5-sonnet` |

> 推荐 DeepSeek：便宜、中文好、长文本能力强。

## 🏗️ 项目结构

```
readme-ai/
├── app.py                  # Streamlit 主界面
├── engine.py               # 代读引擎（提示词 + LLM 调用）
├── parsers.py              # 文件解析（PDF/EPUB/TXT）
├── storage.py              # 存储（SQLite + Markdown）
├── config.py               # 配置管理
├── requirements.txt        # 依赖
├── Dockerfile              # Docker 部署
├── .streamlit/
│   ├── config.toml         # Streamlit 主题配置
│   └── secrets.toml.example # 密钥模板
├── .env.example            # 本地环境变量模板
└── data/                   # 报告存储目录
```

## 📌 路线图

- [ ] V1.1 — 知识库沉淀：自动解析为结构化笔记（YAML + 标签）
- [ ] V1.2 — 智能问答：基于书库回答问题，引用多本书
- [ ] V2.0 — 跨书对话：让不同书的观点互相辩论
- [ ] V2.1 — 批判模式：一键生成对一本书的全盘反驳

## 📄 License

MIT License
