import asyncio


semaphore = asyncio.Semaphore(10)


async def add_user(n):
    async with semaphore:
        print(f"Starting {n}")
        await asyncio.sleep(1)
        print(f"Finishing {n}")


async def add_users():
    # Get iterator
    users = ["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8"]

    tasks = [asyncio.create_task(add_user(n)) for n in users]
    await asyncio.gather(*tasks)


def main():
    asyncio.run(add_users())


if __name__ == "__main__":
    main()