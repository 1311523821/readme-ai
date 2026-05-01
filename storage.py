"""存储模块 - SQLite + Markdown 文件"""
import sqlite3
import os
from datetime import datetime
import config


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_title TEXT NOT NULL,
            mode TEXT DEFAULT '标准版',
            source_type TEXT DEFAULT '书名',
            md_path TEXT NOT NULL,
            created_at TEXT NOT NULL,
            summary TEXT
        )
    """)
    conn.commit()
    return conn


def save_report(book_title: str, mode: str, source_type: str, content: str) -> int:
    """
    保存一份代读报告。
    返回报告 ID。
    """
    now = datetime.now()
    date_str = now.strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(c for c in book_title if c.isalnum() or c in " _-").strip()[:50]
    filename = f"{safe_title}_{date_str}.md"
    md_path = os.path.join(config.REPORTS_DIR, filename)

    # 写 Markdown 文件
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 代读报告：《{book_title}》\n\n")
        f.write(f"- **生成时间**: {now.strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"- **详细程度**: {mode}\n")
        f.write(f"- **来源**: {source_type}\n\n")
        f.write("---\n\n")
        f.write(content)

    # 取前 200 字作为摘要
    summary = content[:200].replace("\n", " ")

    conn = _get_conn()
    cursor = conn.execute(
        "INSERT INTO reports (book_title, mode, source_type, md_path, created_at, summary) VALUES (?, ?, ?, ?, ?, ?)",
        (book_title, mode, source_type, md_path, now.isoformat(), summary),
    )
    report_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return report_id


def list_reports(limit: int = 50) -> list[dict]:
    """获取报告列表，按时间倒序"""
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM reports ORDER BY created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_report(report_id: int) -> dict | None:
    """获取单份报告"""
    conn = _get_conn()
    row = conn.execute("SELECT * FROM reports WHERE id = ?", (report_id,)).fetchone()
    conn.close()
    if row is None:
        return None
    report = dict(row)
    if os.path.exists(report["md_path"]):
        with open(report["md_path"], "r", encoding="utf-8") as f:
            report["content"] = f.read()
    return report


def search_reports(keyword: str) -> list[dict]:
    """搜索报告（按书名或摘要）"""
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM reports WHERE book_title LIKE ? OR summary LIKE ? ORDER BY created_at DESC",
        (f"%{keyword}%", f"%{keyword}%"),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_report(report_id: int) -> bool:
    """删除报告"""
    conn = _get_conn()
    row = conn.execute("SELECT md_path FROM reports WHERE id = ?", (report_id,)).fetchone()
    if row is None:
        conn.close()
        return False
    if os.path.exists(row["md_path"]):
        os.remove(row["md_path"])
    conn.execute("DELETE FROM reports WHERE id = ?", (report_id,))
    conn.commit()
    conn.close()
    return True
