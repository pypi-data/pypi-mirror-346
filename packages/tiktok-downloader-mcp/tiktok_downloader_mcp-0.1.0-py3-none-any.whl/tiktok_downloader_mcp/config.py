"""
Configuration for TikTok Downloader MCP
"""

import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("tiktok-downloader-mcp")

# Concurrent request limit
CONCURRENT_LIMIT = int(os.environ.get("TIKTOK_DOWNLOADER_CONCURRENT_LIMIT", 5))

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
TIKTOK_DOWNLOADER_DIR = ROOT_DIR / "TikTokDownloader"

# Default download directory
DEFAULT_DOWNLOAD_DIR = os.environ.get(
    "TIKTOK_DOWNLOADER_DIR", 
    str(Path.home() / "Downloads" / "TikTokVideos")
)

# Default settings
DEFAULT_SETTINGS = {
    "download_dir": DEFAULT_DOWNLOAD_DIR,
    "max_retries": 3,
    "timeout": 30,
    "concurrent_downloads": 3,
    "default_format": "mp4",
    "auto_rename": True,
    "skip_existing": True,
    "include_watermark": False
} 