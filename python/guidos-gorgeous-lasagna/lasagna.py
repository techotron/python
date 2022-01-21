from time import time

EXPECTED_BAKE_TIME = 40
PREPARATION_TIME = 2

def bake_time_remaining(timeElapsed):
    """Calculate the bake time remaining.

    :param elapsed_bake_time: int baking time already elapsed.
    :return: int remaining bake time derived from 'EXPECTED_BAKE_TIME'.

    Function that takes the actual minutes the lasagna has been in the oven as
    an argument and returns how many minutes the lasagna still needs to bake
    based on the `EXPECTED_BAKE_TIME`.
    """
    return EXPECTED_BAKE_TIME - timeElapsed

def preparation_time_in_minutes(layers):
    """Return the amount of preparation time required given the number of layers

    :param layers: int number of layers
    :return: int preparation time

    Function that takes the number of layers the lasanga has and returns the 
    preparation time it'll require
    """
    return layers * PREPARATION_TIME


def elapsed_time_in_minutes(number_of_layers, elapsed_bake_time):
    """Return the elapsed time in minutes from starting to prepare the
    lasanga

    :param number_of_layers: int number of layers the lasanga has
    :param elapsed_bake_time: int time the lasanga has already baked for
    :return: int time the lasanga has baked for

    Calculate the amount of time that has elapsed in minutes
    """
    return (number_of_layers * PREPARATION_TIME) + elapsed_bake_time