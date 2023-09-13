import asyncio
import aiohttp

from util import async_timed
from chapter_04 import fetch_status

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [fetch_status(session, "https://www.example.com"),
                    fetch_status(session, "https://www.example.com", 3),
                    fetch_status(session, "https://www.example.com", 1),
                    fetch_status(session, "https://www.example.com", 5)]

        # Under the hood, each coroutine is wrapped in a task and starts running concurrently
        # The routine instantly returns an iterator and starts to loop over.
        for finished_task in asyncio.as_completed(fetchers):
            # Here, we start to wait for the first result to come back
            print(await finished_task)

asyncio.run(main())
