# Example of capturing exceptions when using gather. 
# Drawbacks to this is that you have to wait for the results to return before filtering the exceptions.
# It's also a problem if we want to process results as soon as they come in because gather waits for everything to finish

import asyncio
import aiohttp

from chapter_04 import fetch_status, async_timed

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ["https://example.com", "python://example.com"]
        tasks = [fetch_status(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        exceptions = [res for res in results if isinstance(res, Exception)]
        successfull_results = [res for res in results if not isinstance(res, Exception)]

        print(f"All results: {results}")
        print(f"Finished successfully: {successfull_results}")
        print(f"Threw exceptions: {exceptions}")

asyncio.run(main())
