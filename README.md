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
- 🔌 **灵活接入** — 兼容 OpenAI 接口的任意大模型（GPT-4o、Claude、Gemini 等）

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/1311523821/readme-ai.git
cd readme-ai
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API

复制环境变量模板并填入你的 API Key：

```bash
cp .env.example .env
```

编辑 `.env`：

```env
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4o
```

> 💡 支持任何兼容 OpenAI 接口的服务，如 DeepSeek、Moonshot、通义千问等。

### 4. 启动

```bash
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`。

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

## 🏗️ 项目结构

```
readme-ai/
├── app.py              # Streamlit 主界面
├── engine.py           # 代读引擎（LLM 调用 + 提示词模板）
├── parsers.py          # 文件解析（PDF / EPUB / TXT）
├── storage.py          # 存储模块（SQLite + Markdown）
├── config.py           # 配置管理
├── requirements.txt    # Python 依赖
├── .env.example        # 环境变量模板
├── data/               # 数据目录
│   ├── reports.db      # SQLite 数据库
│   └── reports/        # Markdown 报告文件
└── uploads/            # 临时上传文件
```

## 🔧 支持的模型

| 模型 | Base URL | 说明 |
|------|----------|------|
| GPT-4o | `https://api.openai.com/v1` | OpenAI 官方 |
| Claude 3.5 | `https://api.anthropic.com/v1` | Anthropic |
| DeepSeek | `https://api.deepseek.com/v1` | DeepSeek |
| Moonshot | `https://api.moonshot.cn/v1` | Kimi |
| 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 阿里云 |

## 📌 路线图

- [ ] V1.1 — 知识库沉淀：自动解析为结构化笔记（YAML + 标签）
- [ ] V1.2 — 智能问答：基于书库回答问题，引用多本书
- [ ] V2.0 — 跨书对话：让不同书的观点互相辩论
- [ ] V2.1 — 批判模式：一键生成对一本书的全盘反驳

## 📄 License

MIT License
