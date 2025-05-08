#!/usr/bin/env python
"""
抖音扫描MCP客户端
作为原有HTTP服务器的MCP包装器，提供MCP接口
"""

import os
import sys
import json
import asyncio
import argparse
import logging
from typing import List, Dict, Any, Optional
import httpx
from fastmcp import FastMCP

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("douyin_mcp_client")

class DouyinScannerMCP:
    def __init__(self):
        # 获取环境变量或使用默认值
        self.server_host = os.environ.get("SERVER_HOST", "127.0.0.1")
        self.server_port = os.environ.get("SERVER_PORT", "8000")
        self.api_base_url = f"http://{self.server_host}:{self.server_port}"
        
        # 创建MCP服务
        self.mcp = FastMCP("douyin-scanner")
        self._register_tools()
    
    def _register_tools(self):
        # 注册所有MCP工具
        self.mcp.tool()(self.scan_douyin_account)
        self.mcp.tool()(self.scan_multiple_accounts)
        self.mcp.tool()(self.get_server_info)
        self.mcp.tool()(self.get_last_result)
    
    # 异步HTTP客户端
    async def get_http_client(self):
        return httpx.AsyncClient(
            base_url=self.api_base_url, 
            timeout=300.0  # 设置超时为5分钟
        )
    
    async def scan_douyin_account(self, account_url: str, max_videos: int = 100) -> Dict[str, Any]:
        """扫描抖音账号并获取基本信息和视频列表
        
        Args:
            account_url: 抖音账号URL
            max_videos: 要获取的最大视频数量，默认为100
            
        Returns:
            包含账号信息和视频列表的字典
        """
        try:
            logger.info(f"通过MCP扫描抖音账号: {account_url}, 最大视频数: {max_videos}")
            async with await self.get_http_client() as client:
                response = await client.post(
                    f"/api/scan_douyin_account?max_videos={max_videos}", 
                    json={"account_url": account_url},
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"扫描成功: {account_url}, 获取了 {len(result.get('videos_data', []))} 个视频")
                    return result
                else:
                    error_msg = f"API请求失败: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    return {
                        "success": False,
                        "error": error_msg,
                        "account_url": account_url
                    }
        except Exception as e:
            error_msg = f"扫描账号时出错: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "account_url": account_url
            }
    
    async def scan_multiple_accounts(self, account_urls: List[str]) -> List[Dict[str, Any]]:
        """批量扫描多个抖音账号
        
        Args:
            account_urls: 抖音账号URL列表
            
        Returns:
            扫描结果列表
        """
        try:
            logger.info(f"通过MCP批量扫描抖音账号: {len(account_urls)}个")
            async with await self.get_http_client() as client:
                response = await client.post(
                    "/api/scan_multiple_accounts", 
                    json={"account_urls": account_urls},
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    # 处理流式响应
                    results = []
                    async for line in response.aiter_lines():
                        if line.strip():
                            try:
                                data = json.loads(line)
                                results.append(data)
                                logger.info(f"完成扫描 {data['index']+1}/{data['total']}: {data['account_url']}")
                            except Exception as e:
                                logger.error(f"处理数据行时出错: {str(e)}")
                    
                    return results
                else:
                    error_msg = f"API请求失败: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    return [{
                        "success": False,
                        "error": error_msg,
                        "account_urls": account_urls
                    }]
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
            async with await self.get_http_client() as client:
                response = await client.get("/")
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {
                        "status": "错误",
                        "error": f"获取服务器信息失败: {response.status_code} - {response.text}"
                    }
        except Exception as e:
            return {
                "status": "错误",
                "error": f"获取服务器信息时出错: {str(e)}"
            }
    
    async def get_last_result(self) -> Dict[str, Any]:
        """获取最后一次扫描结果"""
        try:
            # 目前服务器未提供获取最后结果的端点，返回错误信息
            return {
                "success": False,
                "error": "服务器不支持获取最后结果功能"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取最后结果时出错: {str(e)}"
            }
    
    def run(self, transport='stdio'):
        """运行MCP服务器"""
        logger.info(f"启动MCP客户端，连接到服务器 {self.api_base_url}")
        self.mcp.run(transport=transport)


def run_mcp():
    """命令行入口点，用于uvx命令"""
    parser = argparse.ArgumentParser(description="抖音扫描MCP客户端")
    parser.add_argument("--transport", choices=["stdio", "tcp", "websocket"], default="stdio",
                      help="MCP通信方式 (默认: stdio)")
    parser.add_argument("--host", type=str, help="TCP/WebSocket服务器主机 (仅当transport不是stdio时有效)")
    parser.add_argument("--port", type=int, help="TCP/WebSocket服务器端口 (仅当transport不是stdio时有效)")
    
    args = parser.parse_args()
    
    # 创建并运行MCP客户端
    client = DouyinScannerMCP()
    client.run(transport=args.transport)


if __name__ == "__main__":
    run_mcp() 