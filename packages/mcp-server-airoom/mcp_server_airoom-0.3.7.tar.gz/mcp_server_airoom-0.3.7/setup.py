from setuptools import setup, find_packages
import os

readme_path = os.path.join(os.path.dirname(__file__), "README.md")
try:
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "AIROOM MCP时间服务器 - 详细描述请参见项目主页。"

setup(
    name="mcp-server-airoom",
    version="0.3.7",
    packages=find_packages(),
    author="AIROOM",
    author_email="your.email@example.com",
    description="一个实现MCP协议的时间服务器示例",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mcp-server-airoom",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.7",
    install_requires=[
        "mcp>=1.6.0",
        "request"
    ],
    entry_points={
        "console_scripts": [
            "mcp-server-airoom=mcp_server_airoom.__main__:main",
        ],
    }
)
