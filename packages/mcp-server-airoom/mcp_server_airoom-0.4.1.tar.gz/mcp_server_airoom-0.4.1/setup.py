from setuptools import setup, find_packages
import os

readme_path = os.path.join(os.path.dirname(__file__), "README.md")
try:
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "AIROOM MCP"

setup(
    name="mcp-server-airoom",
    version="0.4.1",
    packages=find_packages(),
    author="rhythmli",
    author_email="rhythmli.scu@gmail.com",
    description="MCP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.7",
    install_requires=[
        "mcp>=1.6.0",
        "requests>=2.26.0"
    ],
    entry_points={
        "console_scripts": [
            "mcp-server-airoom=mcp_server_airoom.__main__:main",
        ],
    },
    license="MIT",
    license_files=[],
    include_package_data=True,
)
