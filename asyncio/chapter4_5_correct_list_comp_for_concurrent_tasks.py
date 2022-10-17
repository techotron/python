import asyncio
from util import async_timed, delay

@async_timed()
async def main() -> None:
    delay_times = [3, 3, 3]
    # Create (but not "do") the awaitables. Returns instantly
    tasks = [asyncio.create_task(delay(seconds)) for seconds in delay_times]
    # Schedule the awaitables
    [await task for task in tasks]

asyncio.run(main())

# This works because the first list comprehension (for tasks) is using "create_tasks" which returns instantly. 

