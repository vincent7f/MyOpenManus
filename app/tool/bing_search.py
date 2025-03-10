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
        # Run search in thread pool to prevent blocking
        loop = asyncio.get_event_loop()
        links = await loop.run_in_executor(
            None, lambda: self._perform_bing_search(query, num_results)
        )
        
        print(f"Search results: Found {len(links)} links")
        if not links:
            print("Warning: No search results found")
            # Return a default message if no results are found
            return ["No search results found. Please try using different search terms or check your network connection."]
        
        return links

    def _perform_bing_search(self, query: str, num_results: int = 10) -> List[str]:
        """
        Perform Bing search using requests and BeautifulSoup.

        Args:
            query (str): Search query to submit to Bing.
            num_results (int): Number of search results to return.

        Returns:
            List[str]: List of URLs that match the search query.
        """
        # Encode query for URL
        encoded_query = urllib.parse.quote_plus(query)
        
        # Set up search URL
        search_url = f"https://www.bing.com/search?q={encoded_query}&setlang=zh-CN"
        
        # Set headers to simulate browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
        }
        
        try:
            # Send request
            print(f"Sending request to: {search_url}")
            response = requests.get(search_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Parse HTML response
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract links from search results
            links = []
            
            # Try multiple selectors to adapt to possible HTML structure changes in Bing
            selectors = [
                "li.b_algo h2 a",  # Traditional selector
                "h2 a",            # More generic selector
                ".b_title a",      # Another possible selector
                ".b_algo a",       # Another possible selector
                "a[href^='http']", # All links starting with http
            ]
            
            for selector in selectors:
                print(f"Trying selector: {selector}")
                for link in soup.select(selector):
                    url = link.get("href")
                    if url and url.startswith("http") and url not in links:
                        links.append(url)
                        print(f"Found link: {url}")
                        if len(links) >= num_results:
                            break
                
                if len(links) >= num_results:
                    break
            
            # If still no results found, try to save HTML for debugging
            if not links:
                print("No links found, trying to analyze page structure")
                # Find all links in the page
                all_links = soup.find_all("a", href=True)
                print(f"Total links in page: {len(all_links)}")
                
                # Extract some potentially useful links
                for link in all_links:
                    url = link.get("href")
                    if url and url.startswith("http") and "bing.com" not in url and url not in links:
                        links.append(url)
                        print(f"Found potential result link: {url}")
                        if len(links) >= num_results:
                            break
            
            return links
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return []
        except Exception as e:
            print(f"Error executing Bing search: {e}")
            import traceback
            print(traceback.format_exc())
            return []