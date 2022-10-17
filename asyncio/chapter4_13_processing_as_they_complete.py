# If we want to respond to a coroutine which has completed, we can't use ALL_COMPLETED or FIRST_EXCEPTION as we need to wait for them to complete (or when an exception happens)
# We can use FIRST_COMPLETED instead though. This makes wait() return when the first completed task is done.
# This approach doesn't wait for any requests which are still pending though

import asyncio
import aiohttp

from util import async_timed
from chapter_04 import fetch_status

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://www.example.com"
        fetchers = [asyncio.create_task(fetch_status(session, url)),
                    asyncio.create_task(fetch_status(session, url, delay=5)),
                    asyncio.create_task(fetch_status(session, url, delay=2))]

        # This will return when the first task returns. 
        done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_COMPLETED)

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            print(await done_task)

asyncio.run(main())
