#!/usr/bin/env python3

import re

regex = re.compile('(one|two|three|four|five|six|seven|eight|nine|[1-9])')

cardinals = [ 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine' ]

def digit(string):
    if string in cardinals:
        return chr(ord('0') + cardinals.index(string))
    else:
        return string

total = 0

with open("input1.txt") as f:
    for l in f.readlines():
        first = None
        last = None
        for i in range(0,len(l)-1):
            m = regex.search(l[i:])
            if m:
                if first is None:
                    first = m.group(0)
                last = m.group(0)
        composite = digit(first) + digit(last)
        print(composite)
        total += int(composite)

print(total)
