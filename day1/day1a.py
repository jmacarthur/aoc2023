#!/usr/bin/env python3

total = 0

with open("input1.txt") as f:
    for l in f.readlines():
        digits = []
        for char in l:
            if char.isdigit():
                digits.append(char)
        combined = digits[0] + digits[-1]
        total += int(combined)

print(total)
