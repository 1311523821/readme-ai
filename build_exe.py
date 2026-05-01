"""
「读我」打包脚本
使用 PyInstaller 将桌面版打包为独立 EXE
"""
import subprocess
import sys
import os


def main():
    # 确保依赖
    try:
        import PyInstaller
    except ImportError:
        print("正在安装 PyInstaller...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])

    # 打包
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name', '读我',
        '--add-data', 'docs:docs',
        '--hidden-import', 'webview',
        'desktop.py',
    ]

    if sys.platform == 'win32':
        cmd.extend(['--icon', 'docs/favicon.ico'])

    print("正在打包...")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)

    dist = os.path.join('dist', '读我' + ('.exe' if sys.platform == 'win32' else ''))
    if os.path.exists(dist):
        print(f"\n✅ 打包完成: {dist}")
        print(f"   文件大小: {os.path.getsize(dist) / 1024 / 1024:.1f} MB")
    else:
        print("\n❌ 打包失败，请检查错误信息")


if __name__ == '__main__':
    main()
