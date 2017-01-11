#!/usr/bin/env python3

# post-commit hook to produce gcreds function library

# source and target files
source = 'gcreds'
target = '../cfcli/lib/gcreds.fcn'

try:
    with open(source) as f1:
        with open(target,'a') as f2:
            lines = f1.readlines()
            for line in lines:
                f2.write(line)
                if 'MAIN' in line:
                    break
except FileNotFoundError:
    print("\nEither " + source + " not found to open or " + target + " file not accessible\n")
