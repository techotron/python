# This approach is similar to the previous one exception we're looping over the pending tasks until it's empty

import asyncio
import aiohttp

from chapter_04 import fetch_status
from util import async_timed

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://example.com"
        pending = [asyncio.create_task(fetch_status(session, url)),
                    asyncio.create_task(fetch_status(session, url, delay=5)),
                    asyncio.create_task(fetch_status(session, url, delay=2))]

        # This gives us similar behaviour to as_completed except we have better insight into which tasks are done and which tasks are still running
        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            print(f"Done task count: {len(done)}")
            print(f"Pending task count: {len(pending)}")

            for done_task in done:
                print(await done_task)

asyncio.run(main())
