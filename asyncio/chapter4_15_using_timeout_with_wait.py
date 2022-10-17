# When wait's timeout parameter is exceeded, wait will return both the done and pending task sets.
# Timeouts in wait are handled differently as to wait_for and as_completed
#  - Coroutines are not cancelled. Behaves closer to gather and as_completed. If we want to cancel pending tasks, we'd have to loop over them and cancel
#  - Timeout errors are not raised. Wait will return all done and pending tasks up to the point of the timeout value.

import asyncio
import aiohttp

from chapter_04 import fetch_status
from util import async_timed

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://www.example.com"
        fetchers = [asyncio.create_task(fetch_status(session, url)),
                    asyncio.create_task(fetch_status(session, url)),
                    asyncio.create_task(fetch_status(session, url, delay=3))]

        # Use the default return_when value of ALL_COMPLETED for this demonstration
        done, pending = await asyncio.wait(fetchers, timeout=1)

        print(f"Done task count: {len(done)}")

        # We'll have 1 pending task here which won't be cancelled as a result of wait's timeout. If we want to cancel it, we'll need to loop over pending and cancel it manually.
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            result = await done_task
            print(result)

asyncio.run(main())


