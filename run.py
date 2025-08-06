#!/usr/bin/env python3
"""
快速启动脚本 - 16型花名册
"""
import subprocess
import sys
import os


def install_dependencies():
    """安装依赖"""
    print("正在安装Python依赖...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


def setup_database():
    """设置数据库"""
    print("正在设置数据库...")
    # TODO: Add database initialization logic
    pass


def run_server():
    """启动服务器"""
    print("启动FastAPI服务器...")
    subprocess.run(
        ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    )


if __name__ == "__main__":
    print("=== 16型花名册 (MBTI Roster) ===")

    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("错误: requirements.txt 文件不存在")
        sys.exit(1)

    # Install dependencies
    install_dependencies()

    # Setup database (placeholder)
    setup_database()

    # Start server
    run_server()
