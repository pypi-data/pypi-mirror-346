from setuptools import setup, find_packages

setup(
    name="fangcloud-mcp",
    version="0.1.2",
    author="FangCloud Developer",
    author_email="dev@example.com",
    description="FangCloud MCP 是一个 Model Context Protocol (MCP) 服务器实现，提供与 FangCloud 云存储服务的集成",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/example/fangcloud-mcp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="fangcloud, mcp, cloud storage, api",
    python_requires=">=3.12",
    install_requires=[
        "aiohttp>=3.11.18",
        "mcp[cli]>=1.7.1",
    ],
    entry_points={
        "console_scripts": [
            "fangcloud-mcp=fangcloud_mcp.fangcloud:main",
        ],
    },
    package_dir={"fangcloud_mcp": "fangcloud-mcp"},
    project_urls={
        "Bug Reports": "https://github.com/example/fangcloud-mcp/issues",
        "Source": "https://github.com/example/fangcloud-mcp",
        "Documentation": "https://github.com/example/fangcloud-mcp#readme",
    },
)
