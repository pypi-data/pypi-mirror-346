#!/usr/bin/env python
"""
快速启动TikTok下载器MCP服务的脚本
"""

import sys
import os
from pathlib import Path

# 添加项目路径
parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(parent_dir))

from tiktok_downloader_mcp.main import run_mcp

if __name__ == "__main__":
    run_mcp() 