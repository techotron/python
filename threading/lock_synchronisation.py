# Using the same database example in race_condition.py, demonstrate using a lock (aka mutex) on a resource to avoid the race condition problem
# The premise is if a lock has already been acquired on a resource, then the calling thread will wait until it's released.

# Another type of locking mechansim is to use a RLock (reentrant lock). This is a lock which can be called multiple times but must be released the same number of times it was called in order to release a resource.
#  This is useful in situations where there might be a sort of locking loop where a thread needs to call a function which makes use of the same lock which has already been acquired. 
#  This SO answer has a nice example: https://stackoverflow.com/questions/22885775/what-is-the-difference-between-lock-and-rlock

import concurrent.futures
import logging
import threading
import time

class FakeDatabase:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def locked_update(self, name):
        logging.info(f"Thread {name}: starting to update")
        logging.debug(f"Thead {name} about to lock")
        
        # Enter lock context manager to acquire the lock
        with self._lock:
            logging.debug(f"Thread {name} has lock")
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)
            self.value = local_copy
            logging.debug(f"Thread {name} is about to release lock")

        # Lock is released automatically when exiting the lock context manager
        # A common bug to be aware of is a deadlock whereby the lock is never released properly and therefore other threads waiting for the resource block the program indefinetly. Using a context manager to handing the acquire/release greatly reduces the chances of these bugs.
        logging.debug(f"Thread {name} after release")
        logging.info(f"Thread {name}: finishing update")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    # Set level to debug so we can see the extended output
    logging.getLogger().setLevel(logging.DEBUG)

    database = FakeDatabase()
    logging.info(f"Testing update, Starting value is {database.value}")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            executor.submit(database.locked_update, index)
    logging.info(f"Testing update, Ending value is {database.value}")
