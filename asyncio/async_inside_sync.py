import asyncio

concurrency = 10
things_to_process = 10

async def async_sleep():
    print("async sleep")
    await asyncio.sleep(2)


async def executor(queue: asyncio.Queue):
    print("starting executor")
    while True:
        _ = await queue.get()
        await async_sleep()
        queue.task_done()

async def run(queue: asyncio.Queue):
    workers = [
        asyncio.create_task(executor(queue)) for _ in range(concurrency)
    ]

    for i in range(things_to_process):
        await queue.put(i)

    await queue.join()

    for worker in workers:
        worker.cancel()


def main():

    queue  = asyncio.Queue()
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(queue))


if __name__ == "__main__":
    main()
