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
    logging.info("Main      : before creating thread")
    # x = threading.Thread(target=thread_function, args=(1,)) # This is non-daemon thread, meaning the program will wait for the thread to finish
    x = threading.Thread(target=thread_function, args=(1,), daemon=True) # This is a daemon thread, meaning the main process will not wait for the thread unless its join() method is called
    logging.info("Main      : before running thread")
    x.start()
    logging.info("Main      : wait for the thread to finish")
    # x.join() # wait for the threads to finish (join blocks execution until it returns)
    logging.info("Main      : all done")
