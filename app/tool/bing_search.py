# Original version: by @maskkid https://github.com/maskkid
#  source from: 
#  https://github.com/mannaandpoem/OpenManus/issues/277

import asyncio
from typing import List
import requests
from bs4 import BeautifulSoup
import urllib.parse
import logging
from app.tool.base import BaseTool

class BingSearch(BaseTool):
    name: str = "bing_search"
    description: str = """执行必应搜索并返回相关链接列表。
当需要查找网络信息、获取最新数据或研究特定主题时使用此工具。
该工具返回与搜索查询匹配的URL列表。
"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "(必填) 提交给必应的搜索查询。",
            },
            "num_results": {
                "type": "integer",
                "description": "(可选) 要返回的搜索结果数量。默认为10。",
                "default": 10,
            },
        },
        "required": ["query"],
    }

    async def execute(self, query: str, num_results: int = 10) -> List[str]:
        """
        执行必应搜索并返回URL列表。

        Args:
            query (str): 提交给必应的搜索查询。
            num_results (int, optional): 要返回的搜索结果数量。默认为10。

        Returns:
            List[str]: 与搜索查询匹配的URL列表。
        """
        print(f"执行必应搜索，查询词: {query}, 结果数量: {num_results}")
        # 在线程池中运行搜索以防止阻塞
        loop = asyncio.get_event_loop()
        links = await loop.run_in_executor(
            None, lambda: self._perform_bing_search(query, num_results)
        )
        
        print(f"搜索结果: 找到 {len(links)} 个链接")
        if not links:
            print("警告: 未找到任何搜索结果")
            # 如果没有找到结果，返回一个默认消息
            return ["未找到任何搜索结果，请尝试使用不同的搜索词或检查网络连接。"]
        
        return links

    def _perform_bing_search(self, query: str, num_results: int = 10) -> List[str]:
        """
        使用requests和BeautifulSoup执行必应搜索。

        Args:
            query (str): 提交给必应的搜索查询。
            num_results (int): 要返回的搜索结果数量。

        Returns:
            List[str]: 与搜索查询匹配的URL列表。
        """
        # 对URL进行查询编码
        encoded_query = urllib.parse.quote_plus(query)
        
        # 设置搜索URL
        search_url = f"https://www.bing.com/search?q={encoded_query}&setlang=zh-CN"
        
        # 设置头信息以模拟浏览器请求
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
        }
        
        try:
            # 发送请求
            print(f"发送请求到: {search_url}")
            response = requests.get(search_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # 解析HTML响应
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 从搜索结果中提取链接
            links = []
            
            # 尝试多种选择器以适应Bing可能的HTML结构变化
            selectors = [
                "li.b_algo h2 a",  # 传统选择器
                "h2 a",            # 更通用的选择器
                ".b_title a",      # 另一种可能的选择器
                ".b_algo a",       # 另一种可能的选择器
                "a[href^='http']", # 所有以http开头的链接
            ]
            
            for selector in selectors:
                print(f"尝试选择器: {selector}")
                for link in soup.select(selector):
                    url = link.get("href")
                    if url and url.startswith("http") and url not in links:
                        links.append(url)
                        print(f"找到链接: {url}")
                        if len(links) >= num_results:
                            break
                
                if len(links) >= num_results:
                    break
            
            # 如果仍然没有找到结果，尝试保存HTML以便调试
            if not links:
                print("未找到任何链接，尝试分析页面结构")
                # 查找页面中的所有链接
                all_links = soup.find_all("a", href=True)
                print(f"页面中共有 {len(all_links)} 个链接")
                
                # 提取一些可能有用的链接
                for link in all_links:
                    url = link.get("href")
                    if url and url.startswith("http") and "bing.com" not in url and url not in links:
                        links.append(url)
                        print(f"找到可能的结果链接: {url}")
                        if len(links) >= num_results:
                            break
            
            return links
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
            return []
        except Exception as e:
            print(f"执行必应搜索时出错: {e}")
            import traceback
            print(traceback.format_exc())
            return []