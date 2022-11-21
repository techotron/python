# This code will iterate over the coroutines in the generator inside the the "async for" block. 
# The code will run the first coroutine (which async sleeps for 1 second) then does the same for the next coroutine as it iterates over the next one.
# The code takes roughly 3 seconds to complete it total

import asyncio
from util import delay, async_timed

async def postitive_integers_async(until: int):
    for integer in range(1, until):
        await delay(integer)
        yield integer

@async_timed()
async def main():
    async_generator = postitive_integers_async(3)

    # Type is <class 'async_generator'>.
    # An async_generator differs from a synchronous generator in that instead of generating plain python objects as elements, it generates coroutines that we can await until we get a result.
    # Because they're coroutines, we have to use the "async for" syntax.
    print(type(async_generator))
    async for number in async_generator:
        print(f"Got number {number}")

asyncio.run(main())
