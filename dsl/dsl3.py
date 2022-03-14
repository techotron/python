#!/usr/bin/env python3
import sys
import importlib

def get_args(dsl_args):
    """return args, kwargs"""
    args = []
    kwargs = {}
    for dsl_arg in dsl_args:
        if "=" in dsl_arg:
            k, v = dsl_arg.split("=", 1)
            kwargs[k] = v
        else:
            args.append(dsl_arg)
    return args, kwargs

def get_help(module_name):
    mod = importlib.import_module(module_name)
    print(mod.__doc__ or "")
    for name in dir(mod):
        if not name.startswith("_"):
            attr = getattr(mod, name)
            print(attr.__name__)
            print(attr.__doc__ or "", "\n")

# The source file is the 1st arg of the script
if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} <src.dsl>")
    print(f"usage 2: {sys.argv[0]} help=<module name>")
    sys.exit(1)

sys.path.insert(0, "/home/eddy/git/github.com/techotron/python/dsl/modules")

if sys.argv[1].startswith("help="):
    get_help(sys.argv[1][5:])
else:
    with open(sys.argv[1], 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line[0] == "#":
                continue
            parts = line.split()
            mod = importlib.import_module(parts[0])
            args, kwargs = get_args(parts[2:])
            getattr(mod, parts[1])(*args, **kwargs)
