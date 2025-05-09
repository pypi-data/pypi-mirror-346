#!/usr/bin/env python
# coding: utf-8

"""Setup script for TikTok Downloader MCP"""

from setuptools import setup, find_packages

setup(
    name="tiktok-downloader-mcp",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastmcp>=0.1.0",
        "aiohttp>=3.8.0",
        "asyncio>=3.4.3",
        "pydantic>=2.0.0",
        "rich>=13.0.0",
        "PyYAML>=6.0",
        "python-dotenv>=1.0.0",
        "aiofiles>=23.0",
        "aiosqlite>=0.19.0",
        "emoji>=2.6.0",
        "fastapi>=0.100.0",
        "lxml>=4.9.0",
        "qrcode>=7.4.0",
        "uvicorn>=0.22.0",
        "openpyxl>=3.1.0",
        "httpx[socks]>=0.24.0"
    ],
    entry_points={
        'console_scripts': [
            'tiktok-downloader-mcp=tiktok_downloader_mcp.main:run_mcp',
        ],
    },
    python_requires='>=3.8',
) 