from setuptools import setup, find_packages
import os

readme_path = os.path.join(os.path.dirname(__file__), "README.md")
try:
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Smart MCP Server"


setup(
    name="smart-meeting-agent",                     # PyPI上的包名，必须唯一
    version="0.2.3",                                # 版本号，每次更新时需要增加
    packages=find_packages(),                       # 自动查找包目录 (mcp_server_gxb)
    author="rhythmli",                              # 您的名字或昵称
    author_email="rhythmli.scu@gmail.com",          # 您的邮箱
    description=" ",
    long_description=long_description,              # 详细描述（来自README）
    long_description_content_type="text/markdown",  # 描述格式
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.7", # 要求的Python最低版本
    install_requires=[       # 核心依赖项
        "mcp>=1.6.0",        # 依赖MCP SDK
        "requests"           # 添加其他必要的依赖，例如 "requests"
    ],
    entry_points={           # 定义命令行入口点
        "console_scripts": [
            "smart-meeting-agent=smart_meeting_agent.__main__:main", # 命令名=模块路径:函数名
        ],
    },
)