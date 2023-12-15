#!/usr/bin/env python3

from collections import OrderedDict

with open("input15.txt") as f:
    steps = f.readline().strip().split(",")

def hash(string):
    h = 0
    for s in string:
        h += ord(s)
        h *= 17
        h = h & 0xFF
    return h

print(f"{len(steps)} steps.")

boxes = []
for i in range(0,256):
    boxes.append(OrderedDict())

total_part1 = 0

for s in steps:
    total_part1 += hash(s)
    if '=' in s:
        (name, value) = tuple(s.split("="))
        h = hash(name)
        print(name, value)
        boxes[h][name] = value
        print(f"Add/assign {name}={value} in box {h}")
    else:
        name = s[:-1]
        h = hash(name)
        print(f"Remove {name} from box {h} if present")
        if name in boxes[h]:
            del(boxes[h][name])

total_part2 = 0
for i in range(0,256):
    for (index, (name, value)) in enumerate(boxes[i].items(),1):
        power = (i+1)*index*int(value)
        total_part2 += power
    print(i, boxes[i])

print(f"Part 1 total: {total_part1}")
print(f"Part 2 total: {total_part2}")
