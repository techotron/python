# This is an example of a synchronous generator function. Generator functions create sequences of data "lazily", meaning the entire sequence doesn't need to exist in memory before we iterate over it. This can be useful for large datasets.
def positive_integers(until: int):
    for integer in range(until):
        yield integer

# The type of positive_iterator is <class 'generator'> (rather that a list, for example)
positive_iterator = positive_integers(2)

# the next() utility function will trigger one iteration of the generator function. 
print(next(positive_iterator))
print(next(positive_iterator))
