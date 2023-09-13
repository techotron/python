import asyncio
from util import delay

async def main():
    results = await asyncio.gather(delay(3), delay(1))
    print(results) # returns [3, 1] proving that gather retains the order of the tasks that they were provided

asyncio.run(main())
