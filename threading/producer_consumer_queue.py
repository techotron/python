# https://realpython.com/intro-to-python-threading/#producer-consumer-using-queue
# Check the above link to see the example output with some context. For example, even though we set the max size of the queue to 10, the producer thread
#  can get swapped out (by the OS) with the consumer thread, meaning the consumer will start reading from the queue before it's full. 
# It's worth remembering that the OS can swap threads whenever :)

import random
import logging
import concurrent.futures
import threading
import time
import queue

def producer(pipeline, event):
    """"Pretend we're getting a number from the network"""
    while not event.is_set():
        message = random.randint(1, 101)
        logging.info(f"Producer got message: {message}")
        pipeline.set_message(message, "Producer")

    logging.info("Producer received EXIT event. Exiting")


def consumer(pipeline, event):
    """Pretend we're saving a number in the database"""
    while not event.is_set():
        message = pipeline.get_message("Consumer")
        logging.info(f"Consumer storing message: {message} (queue size={pipeline.qsize()})")

    logging.info("Consumer received EXIT event. Exiting")

class Pipeline(queue.Queue):
    def __init__(self):
        super().__init__(maxsize=10)

    def get_message(self, name):
        logging.debug(f"{name}: about to get from queue")
        value = self.get() # Inherited method from the queue.Queue class
        logging.debug(f"{name}: got {value} from queue")
        return value

    def set_message(self, value, name):
        logging.debug(f"{name}: about to add {value} to queue")
        self.put(value)
        logging.debug(f"{name}: added {value} to queue")



if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    # logging.getLogger().setLevel(logging.DEBUG)
    
    pipeline = Pipeline()
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(consumer, pipeline, event)

        time.sleep(0.1)
        logging.info("Main: about to set event")
        event.set()
        logging.info(f"Final queue size: {pipeline.qsize()}")

