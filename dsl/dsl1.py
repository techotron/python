#!/usr/bin/env python3
import sys
import importlib

# The source file is the 1st arg of the script
if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} <src.dsl>")
    sys.exit(1)

sys.path.insert(0, "/home/eddy/git/github.com/techotron/python/dsl/modules")

with open(sys.argv[1], 'r') as file:
    for line in file:
        line = line.strip()
        if not line or line[0] == "#":
            continue
        parts = line.split()
        print(parts)

        mod = importlib.import_module(parts[0])
        print(mod)

getattr(mod, parts[1])(parts[2], parts[3])
