"""Vercel API - 文件解析 + 报告存储"""
import json
import os
import tempfile
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import base64

# ── 提示词模板 ──────────────────────────────────────────────
SYSTEM_PROMPT = """你将扮演一位私人学者，替我仔细阅读用户提供的书籍内容，然后按照下面的结构为我呈现内容。

**重要原则**：
- 不要只给结论，必须保留书中最有说服力的具体案例、实验、故事作为证据。
- 回答应当是一篇详细的深度转述，不少于 5000 字。
- 如果你不确定某个细节，请标注"此处信息不确定"，不要编造。
- 使用中文回答。

请严格按照以下六部分展开，每部分用二级标题（##）标记：

## 一、这本书到底在解决什么问题？
- 用一句话概括核心问题。
- 附上书中导致作者想写这本书的那个核心事件或现象，尽量详细。

## 二、核心主张与论证链条
- 列出本书最主要的 3-5 个主张。
- 每个主张之下，必须配上书中至少一个具体的例子/实验/人物故事来详细说明。
- 如果书中某个主张没有提供实证，请标注"作者在此处未给出实例"，不要自己编造。

## 三、最颠覆或最反直觉的 3 个点
- 摘出书中与大众常识截然相反的观点。
- 每个点都要附上它用来颠覆读者的那个关键实验或真实案例的详细描述。

## 四、如果只记住一个故事
- 选出全书最精彩、最适合以后讲给别人听的一个完整故事。
- 请像写一篇微型小说一样，详细转述其背景、人物、经过、结果和作者的分析。
- 不少于 800 字。

## 五、我可能会质疑的地方
- 客观分析书中的论证是否存在逻辑跳跃、以偏概全、幸存者偏差等问题。
- 如果有，请用书中具体内容举例说明。

## 六、这本书与我生活最直接的一个接口
- 假设我是一个普通上班族/学生，不创业也不做研究。
- 从书中挑一个能立刻用上的具体行动建议，并补充原文中的操作细节。
- 写清楚具体怎么做、什么场景下做、预期什么效果。"""


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """健康检查"""
        if self.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        """处理文件上传解析"""
        if self.path == "/api/parse":
            self._handle_parse()
        elif self.path == "/api/prompt":
            self._handle_prompt()
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        """CORS 预检"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _handle_prompt(self):
        """返回系统提示词"""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"prompt": SYSTEM_PROMPT}).encode())

    def _handle_parse(self):
        """解析上传的文件"""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 50 * 1024 * 1024:  # 50MB limit
                self._json_error(413, "文件太大，最大支持 50MB")
                return

            body = self.rfile.read(content_length)
            data = json.loads(body)

            filename = data.get("filename", "unknown")
            file_b64 = data.get("content", "")
            file_bytes = base64.b64decode(file_b64)

            suffix = os.path.splitext(filename)[1].lower()
            book_name = os.path.splitext(filename)[0]

            # 写临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name

            try:
                if suffix == ".pdf":
                    text = self._parse_pdf(tmp_path)
                elif suffix == ".epub":
                    text = self._parse_epub(tmp_path)
                elif suffix in (".txt", ".md"):
                    text = file_bytes.decode("utf-8", errors="ignore")
                else:
                    self._json_error(400, f"不支持的格式: {suffix}")
                    return
            finally:
                os.unlink(tmp_path)

            # 截断到合理长度
            max_chars = 200000
            if len(text) > max_chars:
                text = text[:max_chars] + "\n\n[...内容已截断...]"

            self._json_response({
                "text": text,
                "book_name": book_name,
                "chars": len(text),
            })

        except Exception as e:
            self._json_error(500, str(e))

    def _parse_pdf(self, path: str) -> str:
        try:
            import pdfplumber
            parts = []
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        parts.append(t)
            return "\n\n".join(parts)
        except ImportError:
            return "[需要安装 pdfplumber 才能解析 PDF]"

    def _parse_epub(self, path: str) -> str:
        try:
            from ebooklib import epub
            from html.parser import HTMLParser

            class TextExtractor(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.result = []
                    self._skip = False
                def handle_starttag(self, tag, attrs):
                    if tag in ("script", "style"): self._skip = True
                def handle_endtag(self, tag):
                    if tag in ("script", "style"): self._skip = False
                    if tag in ("p", "div", "br", "h1", "h2", "h3"): self.result.append("\n")
                def handle_data(self, data):
                    if not self._skip: self.result.append(data)
                def get_text(self): return "".join(self.result)

            book = epub.read_epub(path)
            parts = []
            for item in book.get_items():
                if item.get_type() == 9:
                    content = item.get_content().decode("utf-8", errors="ignore")
                    ext = TextExtractor()
                    ext.feed(content)
                    t = ext.get_text().strip()
                    if t: parts.append(t)
            return "\n\n".join(parts)
        except ImportError:
            return "[需要安装 ebooklib 才能解析 EPUB]"

    def _json_response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def _json_error(self, status, msg):
        self._json_response({"error": msg}, status)
