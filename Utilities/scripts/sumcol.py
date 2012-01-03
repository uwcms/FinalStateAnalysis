#!/usr/bin/env python

'''

Sum a column from stdin

Usage:

    cat data.txt | sumcol.py [ncol]

'''

import sys
import re

def sum_col(stream, index, delimiter='\s+'):
    '''
    Parse input stream, and sum up the [index] column.
    The delimiter is a regex.
    '''
    rx = re.compile(delimiter)
    total = 0.
    for line in stream:
        line = line.strip()
        if not line:
            continue
        field = rx.split(line)[index]
        total += float(field)
    return total

if __name__ == "__main__":
    index = int(sys.argv[1])
    result = sum_col(sys.stdin, index)
    sys.stdout.write(str(result) + '\n')
    sys.exit(0)
