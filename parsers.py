"""文件解析模块 - 支持 PDF / EPUB / TXT"""
import os
import tempfile


def parse_pdf(file_path: str, max_chars: int = 200000) -> str:
    """解析 PDF 文件，提取文本内容"""
    import pdfplumber

    text_parts = []
    total_chars = 0
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
                total_chars += len(page_text)
                if total_chars >= max_chars:
                    break
    return "\n\n".join(text_parts)


def parse_epub(file_path: str, max_chars: int = 200000) -> str:
    """解析 EPUB 文件，提取文本内容"""
    from ebooklib import epub
    from html.parser import HTMLParser

    class HTMLTextExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.result = []
            self._skip = False

        def handle_starttag(self, tag, attrs):
            if tag in ("script", "style"):
                self._skip = True

        def handle_endtag(self, tag):
            if tag in ("script", "style"):
                self._skip = False
            if tag in ("p", "div", "br", "h1", "h2", "h3", "h4", "h5", "h6", "li"):
                self.result.append("\n")

        def handle_data(self, data):
            if not self._skip:
                self.result.append(data)

        def get_text(self):
            return "".join(self.result)

    book = epub.read_epub(file_path)
    text_parts = []
    total_chars = 0

    for item in book.get_items():
        if item.get_type() == 9:  # ITEM_DOCUMENT
            content = item.get_content().decode("utf-8", errors="ignore")
            extractor = HTMLTextExtractor()
            extractor.feed(content)
            page_text = extractor.get_text().strip()
            if page_text:
                text_parts.append(page_text)
                total_chars += len(page_text)
                if total_chars >= max_chars:
                    break

    return "\n\n".join(text_parts)


def parse_txt(file_path: str, max_chars: int = 200000) -> str:
    """解析纯文本文件"""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read(max_chars)


def parse_uploaded_file(uploaded_file, max_chars: int = 200000) -> tuple[str, str]:
    """
    解析上传的文件，返回 (文本内容, 书名)。
    uploaded_file: Streamlit UploadedFile 对象
    """
    filename = uploaded_file.name
    book_name = os.path.splitext(filename)[0]

    # 保存到临时文件
    suffix = os.path.splitext(filename)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        if suffix == ".pdf":
            text = parse_pdf(tmp_path, max_chars)
        elif suffix == ".epub":
            text = parse_epub(tmp_path, max_chars)
        elif suffix in (".txt", ".md"):
            text = parse_txt(tmp_path, max_chars)
        else:
            raise ValueError(f"不支持的文件格式: {suffix}")
    finally:
        os.unlink(tmp_path)

    return text, book_name
