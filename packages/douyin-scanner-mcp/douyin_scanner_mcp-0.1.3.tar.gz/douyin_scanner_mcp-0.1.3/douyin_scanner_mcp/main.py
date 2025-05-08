#!/usr/bin/env python
"""
抖音扫描MCP客户端
整合了扫描逻辑，不再需要外部服务器
"""

import asyncio
import json
import os
import sys
import argparse
import logging
from typing import List, Dict, Any, Optional
import uuid
from pathlib import Path

from fastmcp import FastMCP

from .config import logger, CONCURRENT_LIMIT
from .scanner import scan_douyin_account_page, normalize_douyin_url

# 扫描结果缓存
scan_results_cache = {}

# 创建MCP服务
mcp = FastMCP("douyin-scanner")

class DouyinScannerMCP:
    def __init__(self):
        # 创建信号量用于限制并发请求
        self.concurrency_limiter = asyncio.Semaphore(CONCURRENT_LIMIT)
        
        # 最后一次扫描结果
        self.last_scan_result = None
        
        # 创建MCP服务
        self.mcp = FastMCP("douyin-scanner")
        self._register_tools()
    
    def _register_tools(self):
        # 注册所有MCP工具
        self.mcp.tool()(self.scan_douyin_account)
        self.mcp.tool()(self.scan_multiple_accounts)
        self.mcp.tool()(self.get_server_info)
        self.mcp.tool()(self.get_last_result)
    
    async def scan_douyin_account(self, account_url: str, max_videos: int = 100) -> Dict[str, Any]:
        """扫描抖音账号并获取基本信息和视频列表
        
        Args:
            account_url: 抖音账号URL
            max_videos: 要获取的最大视频数量，默认为100
            
        Returns:
            包含账号信息和视频列表的字典
        """
        try:
            # 标准化URL
            account_url = normalize_douyin_url(account_url)
            
            logger.info(f"通过MCP扫描抖音账号: {account_url}, 最大视频数: {max_videos}")
            
            # 检查缓存
            cache_key = f"{account_url}_{max_videos}"
            if cache_key in scan_results_cache:
                logger.info(f"从缓存中获取账号数据: {account_url}")
                result = scan_results_cache[cache_key]
                return result
            
            # 限制并发请求
            async with self.concurrency_limiter:
                # 直接调用扫描函数
                result = await scan_douyin_account_page(account_url, max_videos)
                
                # 更新缓存和最后结果
                scan_results_cache[cache_key] = result
                self.last_scan_result = result
                
                logger.info(f"扫描成功: {account_url}, 获取了 {len(result.get('videos_data', []))} 个视频")
                return result
                
        except Exception as e:
            error_msg = f"扫描账号时出错: {str(e)}"
            logger.error(error_msg)
            error_result = {
                "success": False,
                "error": error_msg,
                "account_url": account_url
            }
            self.last_scan_result = error_result
            return error_result
    
    async def scan_multiple_accounts(self, account_urls: List[str]) -> List[Dict[str, Any]]:
        """批量扫描多个抖音账号
        
        Args:
            account_urls: 抖音账号URL列表
            
        Returns:
            扫描结果列表
        """
        try:
            logger.info(f"通过MCP批量扫描抖音账号: {len(account_urls)}个")
            
            results = []
            total = len(account_urls)
            
            # 使用信号量限制并发扫描数量
            semaphore = asyncio.Semaphore(CONCURRENT_LIMIT)
            
            async def process_account(index, account_url):
                async with semaphore:
                    try:
                        # 标准化URL
                        normalized_url = normalize_douyin_url(account_url)
                        
                        # 扫描单个账号
                        result = await scan_douyin_account_page(normalized_url)
                        return {
                            "index": index,
                            "total": total,
                            "account_url": normalized_url,
                            "original_url": account_url,
                            "result": result
                        }
                    except Exception as e:
                        error_msg = f"扫描账号时出错: {str(e)}"
                        logger.error(error_msg)
                        return {
                            "index": index,
                            "total": total,
                            "account_url": account_url,
                            "result": {
                                "success": False,
                                "error": error_msg,
                                "account_url": account_url
                            }
                        }
            
            # 创建所有任务
            tasks = [process_account(i, url) for i, url in enumerate(account_urls)]
            
            # 使用 as_completed 按完成顺序处理任务
            for future in asyncio.as_completed(tasks):
                result = await future
                results.append(result)
                logger.info(f"完成扫描 {result['index']+1}/{result['total']}: {result['account_url']}")
            
            # 按原始顺序排序结果
            results.sort(key=lambda x: x["index"])
            
            # 更新最后结果
            if results:
                self.last_scan_result = results[-1]["result"]
            
            return results
            
        except Exception as e:
            error_msg = f"批量扫描账号时出错: {str(e)}"
            logger.error(error_msg)
            return [{
                "success": False,
                "error": error_msg,
                "account_urls": account_urls
            }]
    
    async def get_server_info(self) -> Dict[str, Any]:
        """获取服务器信息"""
        try:
            return {
                "name": "抖音账号扫描服务",
                "version": "1.0.0",
                "status": "运行中",
                "tools": {
                    "扫描单个账号": "scan_douyin_account",
                    "批量扫描多个账号": "scan_multiple_accounts",
                    "获取服务信息": "get_server_info",
                    "获取最后一次结果": "get_last_result"
                },
                "configuration": {
                    "concurrent_limit": CONCURRENT_LIMIT
                }
            }
        except Exception as e:
            return {
                "status": "错误",
                "error": f"获取服务器信息时出错: {str(e)}"
            }
    
    async def get_last_result(self) -> Dict[str, Any]:
        """获取最后一次扫描结果"""
        try:
            if self.last_scan_result:
                return self.last_scan_result
            else:
                return {
                    "success": False,
                    "error": "没有可用的扫描结果"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取最后结果时出错: {str(e)}"
            }
    
    def run(self, transport='stdio'):
        """运行MCP服务器"""
        logger.info(f"启动抖音扫描MCP服务")
        self.mcp.run(transport=transport)


def run_mcp():
    """命令行入口点，用于uvx命令"""
    parser = argparse.ArgumentParser(description="抖音扫描MCP客户端")
    parser.add_argument("--transport", choices=["stdio", "tcp", "websocket"], default="stdio",
                      help="MCP通信方式 (默认: stdio)")
    parser.add_argument("--host", type=str, help="TCP/WebSocket服务器主机 (仅当transport不是stdio时有效)")
    parser.add_argument("--port", type=int, help="TCP/WebSocket服务器端口 (仅当transport不是stdio时有效)")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")
    
    args = parser.parse_args()
    
    # 如果启用了调试模式，设置日志级别
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        logger.debug("调试模式已启用")
    
    # 创建并运行MCP客户端
    client = DouyinScannerMCP()
    client.run(transport=args.transport)


if __name__ == "__main__":
    run_mcp() 