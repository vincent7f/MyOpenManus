# Original version: by @maskkid https://github.com/maskkid
#  source from: 
#  https://github.com/mannaandpoem/OpenManus/issues/277

import asyncio
from typing import List
import logging
from app.tool.base import BaseTool
from playwright.async_api import async_playwright

class BingSearch(BaseTool):
    name: str = "bing_search"
    short_description: str = "Perform Bing search and return a list of relevant links."
    description: str = """Perform Bing search and return a list of relevant links.
Use this tool when you need to find information on the web, get the latest data, or research specific topics.
This tool returns a list of URLs that match the search query.
"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "(Required) Search query to submit to Bing.",
            },
            "num_results": {
                "type": "integer",
                "description": "(Optional) Number of search results to return. Default is 10.",
                "default": 10,
            },
        },
        "required": ["query"],
    }

    async def execute(self, query: str, num_results: int = 10) -> List[str]:
        """
        Execute Bing search and return a list of URLs.

        Args:
            query (str): Search query to submit to Bing.
            num_results (int, optional): Number of search results to return. Default is 10.

        Returns:
            List[str]: List of URLs that match the search query.
        """
        print(f"Executing Bing search, query: {query}, number of results: {num_results}")
        
        links = await self._perform_bing_search(query, num_results)
        
        print(f"Search results: Found {len(links)} links")
        if not links:
            print("Warning: No search results found")
            # Return a default message if no results are found
            return ["No search results found. Please try using different search terms or check your network connection."]
        
        return links

    async def _perform_bing_search(self, query: str, num_results: int = 10) -> List[str]:
        """
        Perform Bing search using Playwright.

        Args:
            query (str): Search query to submit to Bing.
            num_results (int): Number of search results to return.

        Returns:
            List[str]: List of URLs that match the search query.
        """
        links = []
        
        try:
            print(f"Starting Playwright for Bing search: {query}")
            async with async_playwright() as p:
                # 启动浏览器（使用无头模式）
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                
                # 创建新页面
                page = await context.new_page()
                
                # 访问bing.com国际版
                await page.goto("https://www.bing.com/?setlang=en-US&cc=US")
                print("Navigated to Bing international version")
                
                # 等待搜索框加载并输入查询
                await page.wait_for_selector("#sb_form_q")
                await page.fill("#sb_form_q", query)
                
                # 提交搜索
                await page.press("#sb_form_q", "Enter")
                print("Search query submitted")
                
                # 等待搜索结果加载
                await page.wait_for_load_state("networkidle")
                
                # 提取搜索结果链接
                # 尝试多个可能的选择器以适应Bing可能的HTML结构变化
                selectors = [
                    "li.b_algo h2 a",  # 传统选择器
                    "h2 a",            # 更通用的选择器
                    ".b_title a",      # 另一个可能的选择器
                    ".b_algo a",       # 另一个可能的选择器
                ]
                
                for selector in selectors:
                    print(f"Trying selector: {selector}")
                    elements = await page.query_selector_all(selector)
                    
                    if elements:
                        for element in elements:
                            href = await element.get_attribute("href")
                            if href and href.startswith("http") and href not in links:
                                links.append(href)
                                print(f"Found link: {href}")
                                if len(links) >= num_results:
                                    break
                    
                    if len(links) >= num_results:
                        break
                
                # 如果仍然没有找到结果，尝试获取所有链接
                if not links:
                    print("No links found with primary selectors, trying to get all links")
                    all_links = await page.query_selector_all("a[href^='http']")
                    
                    for element in all_links:
                        href = await element.get_attribute("href")
                        if href and href.startswith("http") and "bing.com" not in href and href not in links:
                            links.append(href)
                            print(f"Found potential result link: {href}")
                            if len(links) >= num_results:
                                break
                
                # 关闭浏览器
                await browser.close()
                
            return links
        except Exception as e:
            print(f"Error executing Bing search with Playwright: {e}")
            import traceback
            print(traceback.format_exc())
            return []