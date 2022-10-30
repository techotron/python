import asyncio
from time import sleep

concurrency = 25
total = 200

class My_Async_Queue():
    def __init__(self) -> None:
        self.first_q = asyncio.Queue()
        self.second_q = asyncio.Queue()
        self.third_q = asyncio.Queue()

    async def first_delay(self):
        print("starting first delay loop")
        while True:
            # Await here blocks the coroutine until something is returned from the queue.get() call
            i = await self.first_q.get()
            print(f"[first] sleeping start - {i}")
            await asyncio.sleep(1)
            print(f"[first] sleeping ended - {i}")
            await self.second_q.put(i)
            self.first_q.task_done()

    async def second_delay(self):
        print("starting second delay loop")
        while True:
            # Await here blocks the coroutine until something is returned from the queue.get() call
            i = await self.second_q.get()
            print(f"[second] sleeping start - {i}")
            await asyncio.sleep(1)
            print(f"[second] sleeping ended - {i}")
            await self.third_q.put(i)
            self.second_q.task_done()

    async def third_delay(self):
        print("starting third delay loop")
        while True:
            # Await here blocks the coroutine until something is returned from the queue.get() call
            i = await self.third_q.get()
            print(f"[third] sleeping start - {i}")
            await asyncio.sleep(1)
            print(f"[third] sleeping ended - {i}")
            self.third_q.task_done()


    async def run(self):
        # Multi-dimensional array of tasks. This will spawn sets of $concurrency number of tasks, acting as workers.
        #  In our case here, the tasks are forever loops which are await-ing on a queue.get() call to return.
        workers = [
            [
                asyncio.create_task(self.first_delay()) for _ in range(concurrency)
            ],
            [
                asyncio.create_task(self.second_delay()) for _ in range(concurrency)
            ],
            [
                asyncio.create_task(self.third_delay()) for _ in range(concurrency)
            ]
        ]

        # At this point, we have a number (concurrency * len(workers)) of coroutines which are all blocked, waiting on their respective queues to have items on them.


        for i in range(total):
            # This is where we first unblock the queues by adding an item onto the first one. 
            await self.first_q.put(i)

        for q in [self.first_q, self.second_q, self.third_q]:
            # queue.join() will block execution (ie, cancelling the workers) until the queues have been fully processed, so this just ensures 
            #  that all the queues are empty before cancelling the tasks.
            # The functions themselves are passing "items" down the chain (first_delay -> second_delay -> third_delay)
            await q.join()

        for ws in workers:
            for w in ws:
                w.cancel()



queue = My_Async_Queue()
loop = asyncio.get_event_loop()
loop.run_until_complete(queue.run())
