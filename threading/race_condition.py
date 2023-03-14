# This is an example which demonstrates a race condition problem. The .update() method will be called twice (once by 2 separate threads) and will attempt to update self.value with different values.
# If there wasn't a race condition, you might expect the first thread to update self.value to 1 and then the second thread to update it to 2, however - the ending value of self.value is 1.
#  This is because both threads start when self.value is 0

# If you change the "max_workers" value to 1, you can see the desired behaviour (self.value == 2). 

import time
import logging
import concurrent.futures

class FakeDatabase:
    def __init__(self):
        self.value = 0

    # This minics a DB call which fetches a value, modifies it and saves to back to the DB. In this example, the DB value the class variable, "self.value"
    def update(self, name):
        logging.info(f"Thread {name}: starting update")
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
        logging.info(f"Thread {name}: finished update")

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    database = FakeDatabase()
    logging.info(f"Testing update, Starting value is {database.value}")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            executor.submit(database.update, index)
    logging.info(f"Testing update, Ending value is {database.value}")

# One way to avoid this type of race condition is to use a lock (see lock_synchronisation.py)
