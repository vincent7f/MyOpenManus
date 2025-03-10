import asyncio
from app.tool.bing_search import BingSearch

async def test():
    search = BingSearch()
    results = await search.execute('OpenAI GPT-4')
    print(results)

if __name__ == "__main__":
    asyncio.run(test()) 