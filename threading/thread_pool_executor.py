import concurrent.futures
import logging
import threading
import time

def thread_function(name):
    logging.info(f"Thread {name}: starting")
    time.sleep(2)
    logging.info(f"Thread {name}: finishing")

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    # Something to note about this pattern is that there is no special ordering to the threads that are run. The scheduling is done by the OS and can't be determined with this pattern

    # Start ThreadPoolExecutor context
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(thread_function, range(3))

    # When the code exits the context manager, it runs a join() on the threads, causing the execution to wait for the threads to return.
