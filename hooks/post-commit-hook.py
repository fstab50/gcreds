#!/usr/bin/env python3

# post-commit hook to produce gcreds function library

sourcefile = 'gcreds'

try:
    with open(sourcefile) as f1:
        with open('../cfcli/lib/gcreds.fcn','a') as f2:
            lines = f1.readlines()
            for line in lines:
                f2.write(line)
                if 'MAIN' in line:
                    break
except FileNotFoundError:
    print("\n" + sourcefile + " not found for opening\n")
