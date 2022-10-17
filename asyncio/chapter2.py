import asyncio
import requests

from asyncio import CancelledError, Future
from util import delay, async_timed

def listing2_2():
    async def coroutine_add_one(number: int) -> int:
        return number + 1

    def add_one(number: int) -> int:
        return number + 1

    function_result = add_one(1)
    coroutine_result = coroutine_add_one(1)

    print(f"Function result: {function_result} and the type is {type(function_result)}")
    print(f"Coroutine result: {coroutine_result} and the type is {type(coroutine_result)}")



def listing2_3():
    async def coroutine_add_one(number: int) -> int:
        return number + 1

    # Create an event loop using asyncio.run()
    result = asyncio.run(coroutine_add_one(1))

    print(result)



def listing2_4():
    async def coroutine_add_one(number: int) -> int:
        return number + 1

    async def main() -> None:
        one_plus_one = await coroutine_add_one(1)
        two_plus_one = await coroutine_add_one(2)
        print(one_plus_one)
        print(two_plus_one)

    asyncio.run(main())



def listing2_5():
    async def hello_world_message() -> str:
        await asyncio.sleep(1)
        return "Hello World!"

    async def main() -> None:
        await hello_world_message()
        print(hello_world_message)

    asyncio.run(main())


# This is still a sequential model even though it's using async functions. "await" will pause the current coroutine until it's returned
def listing2_7():
    async def add_one(number: int) -> int:
        return number + 1

    async def hello_world_message() -> str:
        await delay(1)
        return "Hello World!"

    async def main() -> None:
        message = await hello_world_message()
        one_plus_one = await add_one(1)
        print(one_plus_one)
        print(message)

    asyncio.run(main())



def listing2_8():
    async def main():
        sleep_for_three = asyncio.create_task(delay(3))
        print(type(sleep_for_three))
        result = await sleep_for_three
        print(result)

    asyncio.run(main())


# A task is a wrapper around a coroutine. It's scheduled to run as soon as possible, this generally means the first time it hits an "await" statement.
# Therefore, the tasks are scheduled on the "await sleep_for_three" line.
def listing2_9():
    async def main():
        sleep_for_three = asyncio.create_task(delay(3))
        sleep_again = asyncio.create_task(delay(3))
        sleep_once_more = asyncio.create_task(delay(3))

        await sleep_for_three
        await sleep_again
        await sleep_once_more

    asyncio.run(main())    



def listing2_10():
    delay_seconds = 5
    async def hello_every_second():
        for i in range(delay_seconds + 3):
            await asyncio.sleep(1)
            print("I'm running other code while I'm waiting!")

    async def main():
        first_delay = asyncio.create_task(delay(delay_seconds))
        second_delay = asyncio.create_task(delay(delay_seconds))
        await hello_every_second()
        await first_delay
        await second_delay

    asyncio.run(main())


def listing2_11():
    async def main():
        long_task = asyncio.create_task(delay(10))
    
        seconds_elapsed = 0
    
        while not long_task.done():
            print('Task not finished, checking again in a second.')
            await asyncio.sleep(1)
            seconds_elapsed = seconds_elapsed + 1
            if seconds_elapsed == 5:
                long_task.cancel()
    
        try:
            # The cancel method above doesn't stop the task in it's tracks. It only stops when you're at an await point.
            await long_task
        except CancelledError:
            print('Our task was cancelled')
    
    asyncio.run(main())    



def listing2_12():
    async def main():
        delay_task = asyncio.create_task(delay(2))
        try:
            result = await asyncio.wait_for(delay_task, timeout=1)
            print(result)
        except asyncio.exceptions.TimeoutError:
            print("Got a timeout!")
            print(f"Was the task cancelled? {delay_task.cancelled()}")

    asyncio.run(main())


def listing2_13():
    async def main():
        task = asyncio.create_task(delay(10))
    
        try:
            result = await asyncio.wait_for(asyncio.shield(task), 5)
            print(result)
        except asyncio.exceptions.TimeoutError:
            print("Task took longer than five seconds, it will finish soon!")
            result = await task
            print(result)
      
    asyncio.run(main())


# Futures
def listing2_14():
    my_future = Future()
    print(f"Is my_future done? {my_future.done()}")
    my_future.set_result(42)
    print(f"Is my_future done? {my_future.done()}")
    print(f"What is the result of my_future? {my_future.result()}")


# awaiting a future
def listing2_15():
    def make_request() -> Future:
        future = Future()
        # Create a task to asynchronously set the value of the future
        asyncio.create_task(set_future_value(future))
        return future

    async def set_future_value(future) -> None:
        # Wait 1 second before setting the value of the future
        await asyncio.sleep(1)
        future.set_result(42)

    async def main():
        future = make_request()
        print(f"Is the future done? {future.done()}")
        # Pause main until the future's value is set. This is where the task get's "run" because we're awaiting it.
        value = await future
        print(f"Is the future done? {future.done()}")
        print(value)

    asyncio.run(main())


# Measuring coroutine execution using a custom decorator
def listing2_17():
    @async_timed()
    async def _delay(delay_seconds: int) -> int:
        await asyncio.sleep(delay_seconds)

    @async_timed()
    async def main():
        task_one = asyncio.create_task(_delay(2))
        task_two = asyncio.create_task(_delay(3))

        await task_one
        await task_two

    asyncio.run(main())


# Example of when not to use async (ie, CPU bound work)
def listing2_18():

    @async_timed()
    async def cpu_bound_work() -> int:
        counter = 0
        for i in range(100000000):
            counter = counter + 1
        return counter
    
    
    @async_timed()
    async def main():
        task_one = asyncio.create_task(cpu_bound_work())
        task_two = asyncio.create_task(cpu_bound_work())

        # Theses tasks will still run sequentially because asyncio has a single threaded concurrency model and is bound by the GIL
        await task_one
        await task_two
    
    
    asyncio.run(main())


# Example of why not to make all functions async (as a CPU bound task could block an IO task from being awaited)
def listing2_19():
    @async_timed()
    async def cpu_bound_work() -> int:
        counter = 0
        for i in range(100000000):
            counter = counter + 1
        return counter
    
    
    @async_timed()
    async def main():
        task_one = asyncio.create_task(cpu_bound_work())
        task_two = asyncio.create_task(cpu_bound_work())
        delay_task = asyncio.create_task(delay(4))

        # Collectively, these tasks will take the sum of each one. This is because the CPU bound tasks "block" the async sleep from executing concurrently.
        #  If we created "delay_task" first however, then it would sleep for 4 seconds whilst task_one began so would make a bit of saving.
        # Multi-processing is a better way to handle CPU bound work.
        await task_one
        await task_two
        await delay_task
    
    
    asyncio.run(main())


# Example of how wrapping normal API called (eg requests.get()) still blocks the main thread. Generally, any function that performs I/O that is not a coroutine
#  or performs time-consuming CPU operations can be considered blocking.
# It's possible to use the requests library but you have to explicitly tell asyncio to use multithreading with a thread pool executor
def listing2_20():
    @async_timed()
    async def get_example_status() -> int:
        return requests.get('http://www.example.com').status_code
    
    
    @async_timed()
    async def main():
        task_1 = asyncio.create_task(get_example_status())
        task_2 = asyncio.create_task(get_example_status())
        task_3 = asyncio.create_task(get_example_status())

        # Total time for main() to complete is the sum of each task - meaning no concurrency happened
        await task_1
        await task_2
        await task_3
   
    asyncio.run(main())    

# Creating the event loop manually. (In previous examples, asyncio.run() does this for you)
def listing2_21():
    async def main():
        await asyncio.sleep(1)

    loop = asyncio.new_event_loop()

    try:
        loop.run_until_complete(main())
    finally:
        loop.close()


# Adding a task to an existing event loop
def listing2_22():
    def call_later():
        print("I'm being called in the future!")

    async def main():
        loop = asyncio.get_running_loop()
        loop.call_soon(call_later)
        await delay(1)

    asyncio.run(main())


# Enabling debug mode
# The default settings will log a warning if a coroutine takes longer than 100 milliseconds but is configurable in the loop settings: loop.slow_callback_duration = .250
# eg:
# loop = asyncio.get_event_loop()
# loop.slow_callback_duration = .250
def listing2_23():
    @async_timed()
    async def cpu_bound_work() -> int:
        counter = 0
        for i in range(100000000):
            counter = counter + 1
        return counter
    
    
    async def main() -> None:
        task_one = asyncio.create_task(cpu_bound_work())
        await task_one
    
    asyncio.run(main(), debug=True)


if __name__ == "__main__":
    listing2_9()


