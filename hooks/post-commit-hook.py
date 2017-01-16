#!/usr/bin/env python3

# post-commit hook to produce gcreds function library

# source and target files
source = 'gcreds'
target = '../cfcli/lib/gcreds.fcn'

# str markers
start_marker='function declaration start'
end_marker='start MAIN'

try:
    with open(source) as f1:
        lines = f1.readlines()
        for i, line in enumerate(lines):
            if start_marker in line:
                start = i
            if end_marker in line:
                end = i
    with open(target,'w') as f2:
        for line in range(start, end + 1):
                f2.write(lines[line])
except FileNotFoundError:
    print("\nPost-Commit-Hook ERROR")
    print("Either " + source + " not found to open or " + target + " file not accessible\n")
