"""
「读我」桌面版入口
使用 pywebview 加载本地 HTML 文件
"""
import sys
import os


def get_html_path():
    """获取 docs/index.html 的绝对路径（支持 PyInstaller 打包）"""
    # PyInstaller onefile 模式：资源解压到 sys._MEIPASS
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, 'docs', 'index.html')
    if not os.path.exists(path):
        print(f"错误: 找不到 {path}")
        print("提示: 请确保 docs/index.html 存在，或使用 --add-data 打包")
        sys.exit(1)
    return path


def main():
    try:
        import webview
    except ImportError:
        print("请先安装依赖: pip install pywebview")
        sys.exit(1)

    html_path = get_html_path()

    window = webview.create_window(
        '📖 读我 — AI 代读系统',
        html_path,
        width=1200,
        height=800,
        min_size=(800, 600),
        resizable=True,
        text_select=True,
    )
    webview.start(debug='--debug' in sys.argv)


if __name__ == '__main__':
    main()
