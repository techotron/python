import asyncio
import aiohttp

from chapter_04 import fetch_status
from util import async_timed




@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://www.example.com"
        status = await fetch_status(session, url)
        print(f"Status for {url} was {status}")

asyncio.run(main())
