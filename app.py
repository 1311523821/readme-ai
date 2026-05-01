"""
「读我」— AI 私人学者代读系统
主界面入口
"""
import streamlit as st
import time
import config
import engine
import parsers
import storage

# ── 页面配置 ──────────────────────────────────────────────
st.set_page_config(
    page_title="读我 — AI 代读系统",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 自定义样式 ────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        text-align: center;
        padding: 1rem 0 0.5rem;
    }
    .main-title h1 {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .main-title p {
        color: #888;
        font-size: 1.1rem;
        margin-top: 0.2rem;
    }
    .report-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #667eea;
        transition: transform 0.2s;
    }
    .report-card:hover {
        transform: translateX(4px);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1rem;
    }
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ── 会话状态初始化 ────────────────────────────────────────
if "current_report" not in st.session_state:
    st.session_state.current_report = None
if "streaming" not in st.session_state:
    st.session_state.streaming = False


# ── 侧边栏 ──────────────────────────────────────────────
PRESETS = {
    "自定义": {"base_url": "", "model": ""},
    "DeepSeek V4 Flash（推荐）": {"base_url": "https://api.deepseek.com", "model": "deepseek-v4-flash"},
    "DeepSeek V4 Pro": {"base_url": "https://api.deepseek.com", "model": "deepseek-v4-pro"},
    "OpenAI GPT-4o": {"base_url": "https://api.openai.com/v1", "model": "gpt-4o"},
    "Moonshot (Kimi)": {"base_url": "https://api.moonshot.cn/v1", "model": "moonshot-v1-128k"},
    "通义千问": {"base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1", "model": "qwen-plus"},
    "Claude (Anthropic)": {"base_url": "https://api.anthropic.com/v1", "model": "claude-3-5-sonnet-20241022"},
}

with st.sidebar:
    st.markdown("## ⚙️ 配置")

    # 快捷预设
    provider = st.selectbox("🔌 模型服务商", list(PRESETS.keys()), help="选择预设或自定义")
    preset = PRESETS[provider]

    api_key = st.text_input(
        "🔑 API Key",
        value=config.OPENAI_API_KEY,
        type="password",
        help="填入你的 API Key",
    )

    default_base = preset["base_url"] or config.OPENAI_BASE_URL
    default_model = preset["model"] or config.MODEL_NAME

    base_url = st.text_input("API Base URL", value=default_base)
    model_name = st.text_input("模型名称", value=default_model)

    if api_key:
        config.OPENAI_API_KEY = api_key
    if base_url:
        config.OPENAI_BASE_URL = base_url
    if model_name:
        config.MODEL_NAME = model_name

    st.divider()
    st.markdown("## 📊 统计")
    reports = storage.list_reports()
    st.metric("已生成报告", len(reports))

    st.divider()
    st.markdown("""
    ### 💡 使用提示
    - 输入书名即可生成代读报告
    - 上传 PDF/EPUB 获得更精准的代读
    - 案例加厚版字数更多、案例更详实
    - 生成后可对报告进行追问
    """)


# ── 主标题 ────────────────────────────────────────────────
st.markdown("""
<div class="main-title">
    <h1>📖 读我</h1>
    <p>AI 私人学者代读系统 — 让大模型替你仔细读书</p>
</div>
""", unsafe_allow_html=True)

# ── 主标签页 ──────────────────────────────────────────────
tab_read, tab_history, tab_about = st.tabs(["📝 开始代读", "📚 历史报告", "ℹ️ 关于"])


# ──────────────────────────────────────────────────────────
# 代读标签页
# ──────────────────────────────────────────────────────────
with tab_read:
    col_input, col_settings = st.columns([3, 1])

    with col_settings:
        mode = st.radio(
            "详细程度",
            ["标准版", "案例加厚版"],
            help="案例加厚版：更多案例、更详实分析，字数 8000-12000",
        )
        source_type = st.radio("输入方式", ["书名搜索", "文件上传"])

    with col_input:
        if source_type == "书名搜索":
            book_title = st.text_input(
                "📕 输入书名",
                placeholder="例如：思考，快与慢",
                help="输入书名，AI 将根据其知识生成代读报告",
            )
            uploaded_file = None
        else:
            uploaded_file = st.file_uploader(
                "📤 上传书籍文件",
                type=["pdf", "epub", "txt"],
                help="支持 PDF、EPUB、TXT 格式",
            )
            book_title = ""

    # 生成按钮
    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        generate_clicked = st.button(
            "🚀 开始代读",
            type="primary",
            use_container_width=True,
            disabled=st.session_state.streaming,
        )

    # ── 生成逻辑 ──
    if generate_clicked:
        # 校验
        if source_type == "书名搜索" and not book_title.strip():
            st.error("请输入书名")
            st.stop()
        if source_type == "文件上传" and uploaded_file is None:
            st.error("请上传文件")
            st.stop()
        if not config.OPENAI_API_KEY:
            st.error("请在左侧配置中填入 API Key")
            st.stop()

        # 解析文件
        file_content = ""
        if source_type == "文件上传":
            with st.spinner("📄 正在解析文件..."):
                try:
                    file_content, book_title = parsers.parse_uploaded_file(uploaded_file)
                    st.success(f"✅ 文件解析完成，共 {len(file_content)} 字")
                except Exception as e:
                    st.error(f"文件解析失败: {e}")
                    st.stop()

        # 生成报告（流式输出）
        st.session_state.streaming = True
        st.markdown(f"### 📖 正在代读《{book_title}》...")

        report_placeholder = st.empty()
        progress_bar = st.progress(0)
        full_text = ""
        start_time = time.time()

        try:
            for chunk in engine.generate_report(
                book_title=book_title,
                book_content=file_content,
                mode=mode,
            ):
                full_text += chunk
                report_placeholder.markdown(full_text + " ▌")
                # 估算进度
                elapsed = time.time() - start_time
                est_progress = min(0.95, len(full_text) / 6000)
                progress_bar.progress(est_progress)

            report_placeholder.markdown(full_text)
            progress_bar.progress(1.0)

            # 保存报告
            report_id = storage.save_report(
                book_title=book_title,
                mode=mode,
                source_type="文件" if source_type == "文件上传" else "书名",
                content=full_text,
            )

            st.session_state.current_report = {
                "id": report_id,
                "book_title": book_title,
                "content": full_text,
                "mode": mode,
            }

            elapsed = time.time() - start_time
            st.success(f"✅ 代读完成！耗时 {elapsed:.1f} 秒，共 {len(full_text)} 字")

        except Exception as e:
            st.error(f"生成失败: {e}")
        finally:
            st.session_state.streaming = False

    # ── 追问区域 ──
    if st.session_state.current_report:
        st.divider()
        st.markdown("### 💬 追问")
        st.markdown(f"当前报告：《{st.session_state.current_report['book_title']}》")

        followup = st.text_input(
            "对报告的某个部分好奇？继续提问：",
            placeholder="例如：请再详细讲讲第三个主张的那个实验",
        )

        if st.button("💬 追问") and followup:
            if not config.OPENAI_API_KEY:
                st.error("请先配置 API Key")
            else:
                with st.spinner("思考中..."):
                    answer_placeholder = st.empty()
                    answer_text = ""
                    for chunk in engine.generate_followup(
                        book_title=st.session_state.current_report["book_title"],
                        report=st.session_state.current_report["content"],
                        question=followup,
                    ):
                        answer_text += chunk
                        answer_placeholder.markdown(answer_text + " ▌")
                    answer_placeholder.markdown(answer_text)


# ──────────────────────────────────────────────────────────
# 历史报告标签页
# ──────────────────────────────────────────────────────────
with tab_history:
    col_search, col_refresh = st.columns([3, 1])
    with col_search:
        search_keyword = st.text_input("🔍 搜索报告", placeholder="输入书名关键词...")
    with col_refresh:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 刷新"):
            st.rerun()

    if search_keyword:
        reports = storage.search_reports(search_keyword)
    else:
        reports = storage.list_reports()

    if not reports:
        st.info("📭 还没有报告，去「开始代读」生成第一份吧！")
    else:
        for report in reports:
            with st.container():
                col_main, col_action = st.columns([4, 1])
                with col_main:
                    st.markdown(f"**📖 {report['book_title']}**")
                    st.caption(
                        f"📅 {report['created_at'][:16]}　·　"
                        f"📋 {report['mode']}　·　"
                        f"📥 {report['source_type']}"
                    )
                with col_action:
                    if st.button("查看", key=f"view_{report['id']}"):
                        full = storage.get_report(report['id'])
                        if full:
                            st.session_state.current_report = {
                                "id": full["id"],
                                "book_title": full["book_title"],
                                "content": full.get("content", ""),
                                "mode": full["mode"],
                            }
                            st.rerun()
                st.divider()

    # 报告详情弹出
    if st.session_state.current_report and st.session_state.current_report.get("content"):
        with st.expander("📄 当前查看的报告详情", expanded=True):
            st.markdown(st.session_state.current_report["content"])


# ──────────────────────────────────────────────────────────
# 关于页面
# ──────────────────────────────────────────────────────────
with tab_about:
    st.markdown("""
    ## 关于「读我」

    **「读我」** 是一个 AI 代读系统，让大模型替你仔细读书。

    ### 🎯 核心理念

    不只是摘要，而是带着书里的血肉（案例、故事、实验）详细转述给你。
    一份好的代读报告应该像一个读过这本书的朋友在跟你聊天——
    有观点、有故事、有质疑，还有能立刻用上的行动建议。

    ### 📋 报告结构

    每份代读报告包含 6 个固定章节：

    1. **这本书到底在解决什么问题？** — 核心问题 + 作者的起心动念
    2. **核心主张与论证链条** — 3-5 个主张，每个配书中案例
    3. **最颠覆直觉的 3 个观点** — 反常识观点 + 关键实验
    4. **如果只记住一个故事** — 全书最精彩故事的详细转述
    5. **我可能会质疑的地方** — 逻辑漏洞与批判性分析
    6. **与我生活的接口** — 普通人能立刻用的行动建议

    ### 🛠️ 技术栈

    - **前端**: Streamlit
    - **LLM**: 兼容 OpenAI 接口的任意大模型
    - **文件解析**: pdfplumber (PDF) / ebooklib (EPUB)
    - **存储**: SQLite + Markdown 文件

    ### 📝 版本

    - **V1.0** — 当前版本，支持书名搜索、文件上传、报告生成与历史管理
    """)
