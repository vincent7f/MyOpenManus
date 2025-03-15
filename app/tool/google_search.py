import asyncio
from typing import List

from googlesearch import search

from app.tool.base import BaseTool
from app.config import config
from loguru import logger

class GoogleSearch(BaseTool):
    name: str = "google_search"
    short_description: str = "Perform web information retrieval"
    description: str = """Perform a Google search and return a list of relevant links.
Use this tool when you need to find information on the web, get up-to-date data, or research specific topics.
The tool returns a list of URLs that match the search query.
"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "(required) The search query to submit to Google.",
            },
            "num_results": {
                "type": "integer",
                "description": "(optional) The number of search results to return. Default is 10.",
                "default": 10,
            },
        },
        "required": ["query"],
    }

    # Class variable for caching proxy settings
    _proxy_str = None
    _proxy_initialized = False
    
    @classmethod
    def _get_proxy_settings(cls) -> str:
        """
        Get proxy settings from config. This method is called only once and the result is cached.
        
        Returns:
            dict: Proxy settings dictionary or None if no proxy is configured
        """        
        if cls._proxy_initialized is True:
            logger.info("Proxy settings already initialized. Using cached proxy settings.")
            return cls._proxy_str
        
        cls._proxy_initialized = True
        if config.browser_config and config.browser_config.proxy:
            logger.info("Proxy settings found in config")
            proxy_config = config.browser_config.proxy
            # Directly access attributes instead of using get method
            cls._proxy_str = str(proxy_config.server)
            if proxy_config.username and proxy_config.password:
                proxy_auth = f"{proxy_config.username}:{proxy_config.password}@"
                cls._proxy_str = cls._proxy_str.replace("://", f"://{proxy_auth}")
        else:
            logger.info("No proxy settings found in config")
        
        return cls._proxy_str

    async def execute(self, query: str, num_results: int = 10) -> List[str]:
        """
        Execute a Google search and return a list of URLs.

        Args:
            query (str): The search query to submit to Google.
            num_results (int, optional): The number of search results to return. Default is 10.

        Returns:
            List[str]: A list of URLs matching the search query.
        """
        # Run the search in a thread pool to prevent blocking
        loop = asyncio.get_event_loop()
        
        # Determine search parameters based on proxy settings
        search_kwargs = {
            "num_results": num_results,
        }
        
        # Get proxy settings
        proxy_str = self._get_proxy_settings()
        logger.info(f"Using proxy from config.")    
            
        if proxy_str:
            search_kwargs["proxy"] = proxy_str
            
        links = await loop.run_in_executor(
            None, 
            lambda: list(search(query, **search_kwargs))
        )

        return links
