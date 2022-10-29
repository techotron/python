import asyncio
from time import sleep

concurrency = 5
total = 20


class My_Async_Queue():
    def __init__(self) -> None:
        self.first_q = asyncio.Queue()
        self.second_q = asyncio.Queue()
        self.third_q = asyncio.Queue()

    async def first_delay(self):
        while True:
            i = await self.first_q.get()
            print(f"[first] sleeping start - {i}")
            await asyncio.sleep(1)
            print(f"[first] sleeping ended - {i}")
            await self.second_q.put(i)
            self.first_q.task_done()

    async def second_delay(self):
        while True:
            i = await self.second_q.get()
            print(f"[second] sleeping start - {i}")
            await asyncio.sleep(1)
            print(f"[second] sleeping ended - {i}")
            await self.third_q.put(i)
            self.second_q.task_done()

    async def third_delay(self):
        while True:
            i = await self.third_q.get()
            print(f"[third] sleeping start - {i}")
            await asyncio.sleep(1)
            print(f"[third] sleeping ended - {i}")
            self.third_q.task_done()


    async def run(self):
        # Multi-dimensional array of tasks. This will spawn sets of $concurrency number of tasks, acting as workers.
        #  They do no run until we hit (almost) any "await" keyword
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

        # At this point, nothing is executed yet. Tasks are queued but not actually running

        for i in range(total):
            # TODO: For some reason, even though we have tasks scheduled at this point, they're not triggered by this await keyword...
            await self.first_q.put(i) 

        # At this point, still nothing is being executed. Items have been added to the first queue though

        # If the below 2 lines were uncommented, the worker tasks would be triggered and start executing ALL items in "total". The only
        #  thing the sleep(10000) is blocking are the tasks getting cancelled, so the script would just hang for 10000 seconds.
        # await asyncio.sleep(i)
        # sleep(10000)


        for q in [self.first_q, self.second_q, self.third_q]:
            # NOW things are getting executed. First queue consists of 20 items. The following is from the first of a "print(q)":
            #   <Queue maxsize=0 _queue=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19] tasks=20>

            # join() will block until the queues have been processed, so this just ensures that all the queues are empty before cancelling the tasks
            #  The functions themselves are passing "items" down the chain (first_delay -> second_delay -> third_delay)

            # This await triggers the tasks defined in workers. So we'd see concurrency * len(workers) tasks. Or more precisely, tasks for:
            #   concurrency * first_delay()
            #   concurrnecy * second_delay()
            #   concurrency * third_delay()
            # Each of them are a consumer/producer which are poping items off the queue and putting them onto the next queue in the chain.
            await q.join()

        for ws in workers:
            for w in ws:
                w.cancel()


queue = My_Async_Queue()
loop = asyncio.get_event_loop()
loop.run_until_complete(queue.run())
