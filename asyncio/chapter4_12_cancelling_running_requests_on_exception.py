# The drawbacks of using ALL_COMPLETED is that we won't see exceptions untill all tasks have completed. This might be a problem, if we get throttling errors from the endpoint and want to hanle that in a proactive way.
# This is when we could use the FIRST_EXCEPTION option with wait()
# With FISRT_EXCEPTION, there are 2 behaviours:
#  - If no exceptions are returned: Similar to ALL_COMPLETED. We'll wait for all tasks to complete. Pending will be empty
#  - 1 or more exceptions: wait will immediately return. Done will contain any tasks which completed alongside any exceptions encounted. The pending set may be empty but might have tasks that are still running.
# The pending set can be used to manage the currently running tasks.

# Drawback of FIRST_EXCEPTION is that we still need to wait for all coroutines to complete before we can see the results

import asyncio
import aiohttp
import logging

from chapter_04 import fetch_status
from util import async_timed

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = \
            [asyncio.create_task(fetch_status(session, "python://bad.com")),
            asyncio.create_task(fetch_status(session, "https://example.com", delay=3)),
            asyncio.create_task(fetch_status(session, "https://example.com", delay=3))]

        done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_EXCEPTION)

        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error("Request got an exception", 
                                exc_info=done_task.exception())

        for pending_task in pending:
            pending_task.cancel()

asyncio.run(main())
