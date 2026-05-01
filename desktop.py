"""
「读我」桌面版入口
使用 pywebview 创建原生窗口
"""
import threading
import time
import sys
import os
import socket

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def run_streamlit(port):
    os.system(f'streamlit run app.py --server.port={port} --server.headless=true --browser.gatherUsageStats=false')

def main():
    try:
        import webview
    except ImportError:
        print("请先安装依赖: pip install pywebview")
        sys.exit(1)

    port = find_free_port()
    url = f"http://localhost:{port}"

    # 在后台线程启动 Streamlit
    t = threading.Thread(target=run_streamlit, args=(port,), daemon=True)
    t.start()

    # 等待 Streamlit 启动
    for _ in range(30):
        try:
            import urllib.request
            urllib.request.urlopen(url, timeout=1)
            break
        except Exception:
            time.sleep(0.5)

    # 创建原生窗口
    webview.create_window(
        "📖 读我 — AI 代读系统",
        url,
        width=1200,
        height=800,
        resizable=True,
        min_size=(800, 600),
    )
    webview.start()

if __name__ == "__main__":
    main()
