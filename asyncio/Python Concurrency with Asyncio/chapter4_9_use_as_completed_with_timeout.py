# Use a timeout in the as_completed call. This will keep track how long the as_completed call has taken
# Drawbacks to using as_completed is that results come in when they're ready so any ordering that went in is lost

import asyncio
import aiohttp

from util import async_timed
from chapter_04 import async_timed, fetch_status

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [fetch_status(session, "https://example.com", 1),
                    fetch_status(session, "https://example.com", 10),
                    fetch_status(session, "https://example.com", 10)]

        for done_task in asyncio.as_completed(fetchers, timeout=2):
            try:
                result = await done_task
                print(result)
            except asyncio.TimeoutError:
                print("We got a timeout error!")

        # This will show 2 fetch_status calls are running eg
        #  <Task pending name='Task-1' coro=<main() running at /Users/edwardsnow...
        #  <Task pending name='Task-2' coro=<fetch_status() running at /Users/edwardsnow...
        #  <Task pending name='Task-3' coro=<fetch_status() running at /Users/edwardsnow...
        # The pending tasks for fetch_status() are there because the timeout doesn't cancel the pending tasks in the background.
        for task in asyncio.tasks.all_tasks():
            print(task)

asyncio.run(main())
