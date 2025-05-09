#!/usr/bin/env python
"""
TikTok Downloader MCP Server
整合TikTokDownloader的功能，提供MCP接口
"""

import asyncio
import json
import os
import sys
import argparse
import logging
from typing import List, Dict, Any, Optional, Union
import uuid
from pathlib import Path
import traceback

# 添加TikTokDownloader目录到系统路径
tiktok_downloader_path = str(Path(__file__).resolve().parent.parent.parent / "TikTokDownloader")
if tiktok_downloader_path not in sys.path:
    sys.path.insert(0, tiktok_downloader_path)

try:
    from fastmcp import Tool, app
except ImportError:
    logging.error("无法导入fastmcp，请确保已安装: pip install fastmcp")
    sys.exit(1)

from .config import logger, CONCURRENT_LIMIT, DEFAULT_SETTINGS

# 结果缓存
download_results_cache = {}

def convert_douyin_to_tiktok(url):
    """将抖音链接转换为等效的TikTok链接格式"""
    # 提取抖音视频ID
    if "douyin.com/video/" in url:
        # 抖音链接格式: https://www.douyin.com/video/7264453082866552104
        video_id = url.split("/video/")[1].split("?")[0]
        # 转换为TikTok链接格式
        logger.info(f"检测到抖音链接，转换为TikTok链接: {url} -> https://www.tiktok.com/@douyinvideo/video/{video_id}")
        return f"https://www.tiktok.com/@douyinvideo/video/{video_id}"
    return url

class TikTokDownloaderMCP:
    def __init__(self):
        # 创建信号量用于限制并发请求
        self.concurrency_limiter = asyncio.Semaphore(CONCURRENT_LIMIT)
        
        # 最后一次下载结果
        self.last_download_result = None
        
        # 创建MCP服务
        self.mcp = FastMCP("tiktok-downloader")
        
        # 初始化设置
        self.settings = DEFAULT_SETTINGS.copy()
        
        # 初始化下载器实例
        self.downloader = None
        
        # 注册工具
        self._register_tools()
    
    async def _get_downloader(self):
        """获取或创建下载器实例"""
        if self.downloader is None:
            # 动态导入以避免启动时的导入错误
            from TikTokDownloader.src.application import TikTokDownloader
            self.downloader = TikTokDownloader()
            await self.downloader.__aenter__()
        return self.downloader
    
    async def _extract_video_info(self, video_url: str):
        """提取视频信息的辅助方法"""
        # 将抖音链接转换为TikTok链接格式（如果是抖音链接）
        tiktok_url = convert_douyin_to_tiktok(video_url)
        
        # 动态导入以避免启动时的导入错误
        from TikTokDownloader.src.link import extract
        return await extract.get_video_info(tiktok_url)
    
    def _register_tools(self):
        """注册所有MCP工具"""
        # 视频下载工具
        self.mcp.tool()(self.download_video)
        self.mcp.tool()(self.download_batch)
        
        # 链接解析工具
        self.mcp.tool()(self.extract_video_info)
        
        # 服务器信息工具
        self.mcp.tool()(self.get_server_info)
        self.mcp.tool()(self.get_last_result)
        
        # 设置管理
        self.mcp.tool()(self.update_settings)
        self.mcp.tool()(self.get_settings)
    
    async def download_video(self, video_url: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """下载单个TikTok/抖音视频
        
        Args:
            video_url: TikTok/抖音视频URL
            output_dir: 输出目录，如果不指定则使用默认目录
            
        Returns:
            下载结果字典
        """
        try:
            logger.info(f"通过MCP下载视频: {video_url}")
            
            # 将抖音链接转换为TikTok链接格式（如果是抖音链接）
            tiktok_url = convert_douyin_to_tiktok(video_url)
            
            # 检查缓存
            cache_key = f"{tiktok_url}_{output_dir}"
            if cache_key in download_results_cache:
                logger.info(f"从缓存中获取下载结果: {tiktok_url}")
                result = download_results_cache[cache_key]
                return result
            
            # 设置输出目录
            if output_dir:
                download_dir = Path(output_dir)
            else:
                download_dir = Path(self.settings["download_dir"])
            
            # 确保目录存在
            download_dir.mkdir(parents=True, exist_ok=True)
            
            # 限制并发请求
            async with self.concurrency_limiter:
                # 获取下载器
                downloader = await self._get_downloader()
                
                # 提取视频信息
                video_info = await self._extract_video_info(tiktok_url)
                
                if not video_info.get("status"):
                    raise Exception(f"无法提取视频信息: {video_info.get('message', '未知错误')}")
                
                # 构建下载参数
                download_params = {
                    "video_id": video_info["video_id"],
                    "target_dir": str(download_dir),
                    "include_watermark": self.settings["include_watermark"]
                }
                
                # 执行下载
                download_result = await downloader.download_video(**download_params)
                
                # 构建结果
                result = {
                    "status": True,
                    "video_url": video_url,
                    "tiktok_url": tiktok_url,
                    "is_douyin": "douyin.com" in video_url,
                    "video_info": video_info,
                    "download_path": str(download_dir / f"{video_info['video_id']}.mp4"),
                    "download_result": download_result
                }
                
                # 更新缓存和最后结果
                download_results_cache[cache_key] = result
                self.last_download_result = result
                
                logger.info(f"下载成功: {video_url}")
                return result
                
        except Exception as e:
            error_msg = f"下载视频时出错: {str(e)}"
            logger.error(error_msg)
            error_result = {
                "status": False,
                "error": error_msg,
                "video_url": video_url
            }
            self.last_download_result = error_result
            return error_result
    
    async def download_batch(self, video_urls: List[str], output_dir: Optional[str] = None) -> List[Dict[str, Any]]:
        """批量下载多个TikTok/抖音视频
        
        Args:
            video_urls: TikTok/抖音视频URL列表
            output_dir: 输出目录，如果不指定则使用默认目录
            
        Returns:
            下载结果列表
        """
        try:
            logger.info(f"通过MCP批量下载视频: {len(video_urls)}个")
            
            results = []
            total = len(video_urls)
            
            # 设置输出目录
            if output_dir:
                download_dir = Path(output_dir)
            else:
                download_dir = Path(self.settings["download_dir"])
            
            # 确保目录存在
            download_dir.mkdir(parents=True, exist_ok=True)
            
            # 使用信号量限制并发下载数量
            semaphore = asyncio.Semaphore(self.settings["concurrent_downloads"])
            
            async def process_video(index, video_url):
                async with semaphore:
                    try:
                        # 将抖音链接转换为TikTok链接格式（如果是抖音链接）
                        tiktok_url = convert_douyin_to_tiktok(video_url)
                        
                        # 下载单个视频
                        result = await self.download_video(tiktok_url, str(download_dir))
                        return {
                            "index": index,
                            "total": total,
                            "video_url": video_url,
                            "tiktok_url": tiktok_url,
                            "is_douyin": "douyin.com" in video_url,
                            "result": result
                        }
                    except Exception as e:
                        error_msg = f"下载视频时出错: {str(e)}"
                        logger.error(error_msg)
                        return {
                            "index": index,
                            "total": total,
                            "video_url": video_url,
                            "result": {
                                "status": False,
                                "error": error_msg,
                                "video_url": video_url
                            }
                        }
            
            # 创建所有任务
            tasks = [process_video(i, url) for i, url in enumerate(video_urls)]
            
            # 使用 as_completed 按完成顺序处理任务
            for future in asyncio.as_completed(tasks):
                result = await future
                results.append(result)
                logger.info(f"完成下载 {result['index']+1}/{result['total']}: {result['video_url']}")
            
            # 按原始顺序排序结果
            results.sort(key=lambda x: x["index"])
            
            # 更新最后结果
            if results:
                self.last_download_result = results[-1]["result"]
            
            return results
            
        except Exception as e:
            error_msg = f"批量下载视频时出错: {str(e)}"
            logger.error(error_msg)
            return [{
                "status": False,
                "error": error_msg,
                "video_urls": video_urls
            }]
    
    async def extract_video_info(self, video_url: str) -> Dict[str, Any]:
        """提取TikTok/抖音视频信息
        
        Args:
            video_url: TikTok/抖音视频URL
            
        Returns:
            视频信息字典
        """
        try:
            logger.info(f"通过MCP提取视频信息: {video_url}")
            
            # 将抖音链接转换为TikTok链接格式（如果是抖音链接）
            tiktok_url = convert_douyin_to_tiktok(video_url)
            
            # 限制并发请求
            async with self.concurrency_limiter:
                # 提取视频信息
                video_info = await self._extract_video_info(tiktok_url)
                
                # 添加原始URL信息
                if video_info and video_info.get("status"):
                    video_info["original_url"] = video_url
                    video_info["tiktok_url"] = tiktok_url
                    video_info["is_douyin"] = "douyin.com" in video_url
                
                logger.info(f"成功提取视频信息: {video_url}")
                return video_info
            
        except Exception as e:
            error_msg = f"提取视频信息时出错: {str(e)}"
            logger.error(error_msg)
            return {
                "status": False,
                "error": error_msg,
                "video_url": video_url
            }
    
    async def update_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """更新TikTok下载器设置
        
        Args:
            settings: 要更新的设置字典
            
        Returns:
            更新后的设置字典
        """
        try:
            logger.info(f"通过MCP更新设置: {settings}")
            
            # 更新设置
            for key, value in settings.items():
                if key in self.settings:
                    self.settings[key] = value
            
            logger.info(f"设置已更新: {self.settings}")
            return self.settings
            
        except Exception as e:
            error_msg = f"更新设置时出错: {str(e)}"
            logger.error(error_msg)
            return {
                "status": False,
                "error": error_msg,
                "settings": self.settings
            }
    
    async def get_settings(self) -> Dict[str, Any]:
        """获取当前TikTok下载器设置
        
        Returns:
            当前设置字典
        """
        try:
            logger.info("通过MCP获取设置")
            return self.settings
            
        except Exception as e:
            error_msg = f"获取设置时出错: {str(e)}"
            logger.error(error_msg)
            return {
                "status": False,
                "error": error_msg
            }
    
    async def get_server_info(self) -> Dict[str, Any]:
        """获取服务器信息
        
        Returns:
            服务器信息字典
        """
        try:
            logger.info("通过MCP获取服务器信息")
            
            info = {
                "name": "TikTok Downloader MCP",
                "version": "1.0.0",
                "settings": self.settings,
                "capabilities": {
                    "download_video": True,
                    "download_batch": True,
                    "extract_info": True,
                    "douyin_support": True
                }
            }
            
            # 获取TikTokDownloader版本（如果可用）
            try:
                from TikTokDownloader.src.application import TikTokDownloader
                info["tiktok_downloader_version"] = getattr(TikTokDownloader, "VERSION", "未知")
            except:
                info["tiktok_downloader_version"] = "未知"
            
            return info
            
        except Exception as e:
            error_msg = f"获取服务器信息时出错: {str(e)}"
            logger.error(error_msg)
            return {
                "status": False,
                "error": error_msg
            }
    
    async def get_last_result(self) -> Dict[str, Any]:
        """获取最后一次下载结果
        
        Returns:
            最后一次下载结果
        """
        try:
            logger.info("通过MCP获取最后一次下载结果")
            
            if self.last_download_result:
                return self.last_download_result
            else:
                return {"status": False, "message": "尚无下载结果"}
            
        except Exception as e:
            error_msg = f"获取最后一次下载结果时出错: {str(e)}"
            logger.error(error_msg)
            return {
                "status": False,
                "error": error_msg
            }
    
    async def cleanup(self):
        """清理资源"""
        if self.downloader:
            await self.downloader.__aexit__(None, None, None)
    
    def run(self, transport='stdio'):
        """运行MCP服务"""
        self.mcp.run(transport=transport)

def run_mcp():
    """启动MCP服务"""
    parser = argparse.ArgumentParser(description='TikTok Downloader MCP Service')
    parser.add_argument('--transport', type=str, default='stdio', choices=['stdio', 'tcp', 'websocket'],
                      help='传输方式: stdio, tcp, websocket')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                      help='服务器地址（仅TCP/WebSocket模式有效）')
    parser.add_argument('--port', type=int, default=8080,
                      help='服务器端口（仅TCP/WebSocket模式有效）')
    parser.add_argument('--debug', action='store_true',
                      help='启用调试模式')
    
    args = parser.parse_args()
    
    # 配置日志级别
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("调试模式已启用")
    
    # 创建并运行MCP服务
    service = TikTokDownloaderMCP()
    
    if args.transport == 'stdio':
        service.run(transport='stdio')
    elif args.transport == 'tcp':
        service.run(transport='tcp', host=args.host, port=args.port)
    elif args.transport == 'websocket':
        service.run(transport='websocket', host=args.host, port=args.port)

if __name__ == "__main__":
    run_mcp() 