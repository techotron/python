# Extra Threading Primitives
These are some primitives that are worth knowing about but not demo'd in the code examples contained in this folder.

[Source](https://realpython.com/intro-to-python-threading/#threading-objects)

## Semaphore
`threading.Semaphore`
This is a counter witha few special properties:
- The counting is atomic - this means there is a guarantee that the OS will not swap out the thread in the middle of incrementing or decrementing the counter
- The counter is incremented when you call `.release()` and decremented when you call `.acquire()`. 
- If a thread calls `.acquire()` when the counter is zero, that thread will block until a different thread calls `.release()` and increments the counter by 1.

An example use case is to protect a resource with limited capacity, eg a pool of connections where you want to limit the size of the pool to a specific number.

## Timer
`threading.Timer`
A way to schedule a function to be called after a certain amount of time has passed. Eg:
```python
t = threading.Timer(30.0, my_function)
t.start()
```

In this example, `my_function` will be called _at sometime_ after 30 seconds from when `t.start()` is called. There is no promise that it'll be run exactly at 30 seconds after.
A running timer can be stopped with `t.cancel()`

## Barrier
`threading.Barrier`
This can be used to keep a fixed number of threads in sync. When called, you need to specify how many threads to synchronise. Each thread calls `.wait()` on the Barrier and will remain blocked until the specified number of threads have called `.wait()`, at which point they'll all be released at the same time.

A use case for this is to allow a pool of threads to initialise themselves. Having the threads wait on a barrier after they are initialised will ensure that none of the threads start running before all of the threads are finished with their initialisation.

