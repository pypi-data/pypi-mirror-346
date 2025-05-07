from setuptools import setup, find_packages
import os

# 读取 README 文件作为长描述，确保使用UTF-8编码
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
try:
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "airoom"


setup(
    name="mcp-server-airoom",  # PyPI上的包名，必须唯一
    version="0.3.2",         # 版本号，每次更新时需要增加
    packages=find_packages(), # 自动查找包目录 (mcp_server_gxb)
    author="airoom",             # 您的名字或昵称
    author_email="rhythmli.scu@gmail.com", # 您的邮箱
    description="airoom", # 简短描述
    long_description=long_description,          # 详细描述（来自README）
    long_description_content_type="text/markdown", # 描述格式
    url="https://github.com/yourusername/mcp-server-gxb", # 项目主页URL（可选）
    classifiers=[ # 包的分类信息
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent", # 兼容的操作系统
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.7", # 要求的Python最低版本
    install_requires=[       # 核心依赖项
        "mcp>=1.6.0",        # 依赖MCP SDK
        # 添加其他必要的依赖，例如 "requests"
    ],
    entry_points={           # 定义命令行入口点
        "console_scripts": [
            "mcp-server-airoom=mcp_server_airoom.__main__:main", # 命令名=模块路径:函数名
        ],
    },
)