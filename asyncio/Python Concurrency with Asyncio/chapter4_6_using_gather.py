import asyncio
import  aiohttp
from aiohttp import ClientSession
from chapter_04 import fetch_status
from util import async_timed

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ["https://example.com" for _ in range(1000)]
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)

asyncio.run(main())


# The above function takes around 1 second to complete. Compare with the below which processes the requests sequentially

@async_timed()
async def main2():
    async with aiohttp.ClientSession() as session:
        urls = ["https://example.com" for _ in range(1000)]
        # awaiting for the status here will cause the list comp to wait on each iteration
        status_codes = [await fetch_status(session, url) for url in urls]
        print(status_codes)

# asyncio.run(main2())
