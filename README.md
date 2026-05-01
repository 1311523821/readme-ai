# 📖 读我 — AI 私人学者代读系统

> 让大模型替你仔细读书。不只给结论，而是带着书里的血肉（案例、故事、实验）详细转述给你。

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![GitHub Pages](https://img.shields.io/badge/GitHub_Pages-Deployed-black.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Release](https://img.shields.io/badge/Release-v1.2.0-orange.svg)

## ✨ 特性

- 📕 **书名代读** — 输入书名，AI 生成 5000-10000 字详细报告
- 📤 **文件上传** — 支持 PDF / EPUB / TXT，纯前端解析，数据不出浏览器
- 📋 **粘贴内容** — 直接粘贴书籍片段，自动提取前 30 字作为标题
- 📝 **结构化报告** — 固定六章节，案例充分、有观点有故事
- 🔍 **案例加厚版** — 可选更详实模式（8000-12000 字）
- 💬 **追问功能** — 对报告任意部分继续深入提问
- 📚 **历史管理** — 报告自动保存，左侧栏浏览、回看，生成后即时刷新
- 🔌 **多模型支持** — DeepSeek V4、GPT-4o、Moonshot、通义千问，可自定义
- 📝 **自定义提示词** — 设置中可编辑完整系统提示词，`{书名}` 自动替换
- ✕ **随时取消** — 生成中可一键中断 API 请求，不再浪费 token
- 🛡️ **隐私优先** — API Key 仅存浏览器本地，纯静态部署
- ♿ **无障碍支持** — 完整的 ARIA 标签，键盘可操作
- 📦 **桌面版** — 打包为独立 EXE，无需安装浏览器

## 🚀 使用方式

### 方式一：GitHub Pages（推荐，无需安装）

直接访问：`https://1311523821.github.io/readme-ai/`

纯前端运行，API Key 只存在浏览器本地，数据不经过任何服务器。

### 方式二：本地打开

```bash
git clone https://github.com/1311523821/readme-ai.git
cd readme-ai
# 直接用浏览器打开 docs/index.html
open docs/index.html    # macOS
xdg-open docs/index.html  # Linux
start docs/index.html   # Windows
```

### 方式三：桌面应用

```bash
# 安装依赖
pip install -r requirements.txt

# 直接运行桌面版
python desktop.py

# 或打包成独立 EXE
python build_exe.py
# 产物在 dist/读我（Windows 为 dist/读我.exe）
```

桌面版基于 pywebview，打包后的 EXE 完全离线可用（所有 JS 库已本地化），用户无需安装浏览器或 Python。

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
| DeepSeek | deepseek-v4-pro | 更强推理 |
| OpenAI | gpt-4o | 效果最好 |
| Moonshot | moonshot-v1-128k | Kimi，中文好 |
| 通义千问 | qwen-plus | 阿里云 |
| 自定义 | 任意 OpenAI 兼容 API | 填入 Base URL + Model Name 即可 |

## 🏗️ 项目结构

```
readme-ai/
├── docs/
│   ├── index.html          # GitHub Pages 前端（纯静态，单文件 SPA）
│   ├── favicon.ico         # 桌面版图标
│   ├── pdf.min.mjs         # PDF 解析（本地化）
│   ├── pdf.worker.min.js   # PDF Worker（本地化）
│   ├── marked.min.js       # Markdown 渲染（本地化）
│   ├── highlight.min.js    # 代码高亮（本地化）
│   ├── github.min.css      # 代码高亮样式（本地化）
│   └── purify.min.js       # XSS 防护（本地化）
├── desktop.py              # 桌面应用入口（pywebview）
├── build_exe.py            # PyInstaller 打包脚本（跨平台）
├── app.py                  # Streamlit 版（可选）
├── engine.py               # 代读引擎（提示词 + LLM 调用）
├── parsers.py              # 文件解析（PDF/EPUB/TXT）
├── storage.py              # 存储（SQLite + Markdown）
├── config.py               # 配置管理
├── requirements.txt        # Python 依赖
├── Dockerfile              # Docker 部署
└── data/                   # 报告存储目录
```

## 📝 版本历史

### V1.2.0 (2026-05-01)

用户体验修复：
- ✕ **随时取消** — AbortController + 取消按钮，生成中一键中断，不再浪费 token
- 📝 **自定义提示词** — 设置中可编辑完整系统提示词模板，支持 `{书名}` 变量替换
- 📋 **粘贴智能标题** — 粘贴内容自动提取前 30 字作为标题，不再显示「粘贴内容」
- 📚 **历史即时刷新** — 生成完成后左侧列表自动更新，无需手动刷新
- 🛡️ **状态保护** — 生成中点「+ 新建」或切换历史有确认提示，防止误操作
- 🔘 **按钮状态** — 生成中复制/下载按钮提示「请稍候」，无报告时提示「暂无报告」
- 🐛 **PDF 解析修复** — pdf.js worker 本地化，国内网络不再加载失败
- 🐛 **进度条竞态修复** — 快速重新生成时进度条不再消失

### V1.1.0 (2026-05-01)

前端增强：
- 内嵌 SVG favicon，浏览器标签页显示图标
- API 错误分类提示（401 密钥无效 / 403 余额不足 / 429 频率过高 / 500+ 服务器错误）
- 网络异常友好提示，不再显示裸错误信息
- 加载骨架屏，生成过程中显示 shimmer 占位动画
- EPUB 解析鲁棒性增强，单章节损坏不影响整体
- 文件大小限制（拒绝 >50MB，PDF >10MB 警告）
- localStorage 配额溢出时自动裁剪最旧记录，防止静默丢数据
- 无障碍 ARIA 标签全覆盖，键盘可操作
- CSS 过渡动画优化，focus-visible 聚焦环全局生效

EXE 打包修复：
- 跨平台 `--add-data` 分隔符适配（Windows `;` / Unix `:`）
- PyInstaller onefile 模式 `sys._MEIPASS` 路径支持
- pywebview 安装检查，打包前自动补全

CDN 本地化：
- marked.js、highlight.js、purify.js 及样式文件全部本地化
- PDF 解析组件本地化
- 桌面版完全离线可用

### V1.0.0 (2026-05-01)

- 首个版本，支持书名搜索、文件上传、报告生成与历史管理
- Streamlit + 纯静态双版本

## 📌 路线图

- [ ] V1.3 — 知识库沉淀：自动解析为结构化笔记（YAML + 标签）
- [ ] V1.4 — 智能问答：基于书库回答问题，引用多本书
- [ ] V2.0 — 跨书对话：让不同书的观点互相辩论
- [ ] V2.1 — 批判模式：一键生成对一本书的全盘反驳

## 📄 License

MIT License
