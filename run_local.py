#!/usr/bin/env python3
"""
本地开发启动脚本 - 16型花名册
Local Development Startup Script
"""
import os
import subprocess
import sys


def setup_environment():
    """设置本地开发环境变量"""
    print("设置本地开发环境...")

    # Set environment variables for local development
    os.environ["DATABASE_URL"] = "sqlite:///./mbti_roster.db"
    os.environ["SECRET_KEY"] = "dev-secret-key-change-in-production-12345"
    os.environ["REDIS_URL"] = "redis://localhost:6379"
    os.environ["EMAIL_FROM"] = "noreply@mbti-roster.local"
    os.environ["DAILY_VOTE_LIMIT"] = "20"
    os.environ["DAILY_NO_REASON_LIMIT"] = "5"
    os.environ["NEW_USER_24H_LIMIT"] = "3"
    os.environ["DAILY_REGISTRATIONS_PER_IP"] = "3"

    print("环境变量设置完成")


def install_dependencies():
    """安装依赖"""
    print("正在安装Python依赖...")
    try:
        # Use virtual environment Python
        venv_python = os.path.join("venv", "Scripts", "python.exe")
        if os.path.exists(venv_python):
            subprocess.run(
                [venv_python, "-m", "pip", "install", "-r", "requirements_minimal.txt"],
                check=True,
            )
        else:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    "requirements_minimal.txt",
                ],
                check=True,
            )
        print("依赖安装完成")
    except subprocess.CalledProcessError:
        print("依赖安装失败")
        return False
    return True


def run_server():
    """启动服务器"""
    print("启动FastAPI服务器...")
    print("访问地址: http://localhost:8000")
    print("API文档: http://localhost:8000/docs")
    print("健康检查: http://localhost:8000/health")
    print("测试接口: http://localhost:8000/test")
    print("\n按 Ctrl+C 停止服务器")

    try:
        # Use virtual environment uvicorn
        venv_uvicorn = os.path.join("venv", "Scripts", "uvicorn.exe")
        if os.path.exists(venv_uvicorn):
            subprocess.run(
                [
                    venv_uvicorn,
                    "app.main:app",
                    "--host",
                    "0.0.0.0",
                    "--port",
                    "8000",
                    "--reload",
                ]
            )
        else:
            subprocess.run(
                [
                    "uvicorn",
                    "app.main:app",
                    "--host",
                    "0.0.0.0",
                    "--port",
                    "8000",
                    "--reload",
                ]
            )
    except KeyboardInterrupt:
        print("\n服务器已停止")


if __name__ == "__main__":
    print("=== 16型花名册 (MBTI Roster) - 本地开发模式 ===")

    # Check if requirements_minimal.txt exists
    if not os.path.exists("requirements_minimal.txt"):
        print("错误: requirements_minimal.txt 文件不存在")
        sys.exit(1)

    # Setup environment
    setup_environment()

    # Install dependencies
    if not install_dependencies():
        sys.exit(1)

    # Start server
    run_server()
