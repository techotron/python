# Default behaviour for wait is to wait for all tasks to complete
# This is closest to using gather but with some differences

# How to handle exceptions in this paradigm:
#  - Use await and let the exceptions throw
#  - Use await and wrap it in a try/except block
#  - Use task.result() and task.exception() (these can be safely called because with ALL_COMPLETED we're guaranteed that they're completed)

import asyncio
import aiohttp

from util import async_timed
from chapter_04 import fetch_status

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [asyncio.create_task(fetch_status(session, "https://example.com")),
                    asyncio.create_task(fetch_status(session, "https://example.com"))]
        
        # Wait returns a set of tasks which are finished and a set of tasks still pending
        done, pending = await asyncio.wait(fetchers)

        print(f"Done task count: {len(done)}")

        # Pending will always be 0 because the default option for asyncio.wait() is ALL_COMPLETED, meaning it won't return until everything is complete.
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            # If any of the tasks returned an exception, we don't see it until we await the future here
            result = await done_task
            print(result)

asyncio.run(main())
