def add_str(*args, **kwargs):
    """Concatenates all arguments as strings. Prints results to stdout."""
    # List comp for moving kwargs into list
    kwargs_list = ["%s=%s" % (k, kwargs[k]) for k in kwargs]
    print("".join(args), ",".join(kwargs_list))

def add_num(*args, **kwargs):
    """Adds all arguments as numbers of type int or float. Prints results to stdout."""
    t = globals()["__builtins__"][kwargs["type"]]
    print(sum(map(t, args)))
