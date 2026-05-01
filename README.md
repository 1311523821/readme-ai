# 📖 读我 — AI 私人学者代读系统

> 让大模型替你仔细读书。不只给结论，而是带着书里的血肉（案例、故事、实验）详细转述给你。

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![GitHub Pages](https://img.shields.io/badge/GitHub_Pages-Ready-black.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ 特性

- 📕 **书名代读** — 输入书名，AI 生成 5000-10000 字详细报告
- 📤 **文件上传** — 支持 PDF / EPUB / TXT，解析原文后代读
- 📝 **结构化报告** — 固定六章节，案例充分、有观点有故事
- 🔍 **案例加厚版** — 可选更详实模式（8000-12000 字）
- 💬 **追问功能** — 对报告任意部分继续深入提问
- 📚 **历史管理** — 保存、搜索、回看所有代读报告
- 🔌 **多模型支持** — DeepSeek V4、GPT-4o、Moonshot、通义千问

## 🚀 使用方式

### 方式一：GitHub Pages（推荐，无需安装）

直接访问：`https://<你的用户名>.github.io/readme-ai/`

纯前端运行，API Key 只存在浏览器本地，数据不经过任何服务器。

### 方式二：本地运行

```bash
git clone https://github.com/1311523821/readme-ai.git
cd readme-ai
# 直接用浏览器打开 docs/index.html
open docs/index.html  # macOS
# 或
xdg-open docs/index.html  # Linux
```

### 方式三：桌面应用（EXE）

```bash
pip install pywebview
python desktop.py
```

打包成独立 EXE：

```bash
pip install pyinstaller pywebview
python build_exe.py
# 产物在 dist/读我.exe
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

| 服务商 | 推荐模型 | 说明 |
|--------|----------|------|
| DeepSeek | deepseek-v4-flash | 便宜好用，推荐 |
| OpenAI | gpt-4o | 效果最好 |
| Moonshot | moonshot-v1-128k | Kimi，中文好 |
| 通义千问 | qwen-plus | 阿里云 |

## 🏗️ 项目结构

```
readme-ai/
├── docs/
│   └── index.html        # GitHub Pages 前端（纯静态，单文件）
├── desktop.py             # 桌面应用入口（pywebview）
├── build_exe.py           # PyInstaller 打包脚本
├── app.py                 # Streamlit 版（可选）
├── engine.py              # 代读引擎（提示词 + LLM 调用）
├── parsers.py             # 文件解析（PDF/EPUB/TXT）
├── storage.py             # 存储（SQLite + Markdown）
├── config.py              # 配置管理
├── requirements.txt       # Python 依赖
├── Dockerfile             # Docker 部署
└── data/                  # 报告存储目录
```

## 📌 路线图

- [ ] V1.1 — 知识库沉淀：自动解析为结构化笔记（YAML + 标签）
- [ ] V1.2 — 智能问答：基于书库回答问题，引用多本书
- [ ] V2.0 — 跨书对话：让不同书的观点互相辩论
- [ ] V2.1 — 批判模式：一键生成对一本书的全盘反驳

## 📄 License

MIT License
