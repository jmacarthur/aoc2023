#!/usr/bin/env python3

patterns = []
current_pattern = []
with open("input13.txt") as f:
    while True:
        l = f.readline()
        if l == "":
            break
        l = l.strip()
        if l == "":
            if current_pattern:
                patterns.append(current_pattern)
                current_pattern = []
        else:
            current_pattern.append(l)
    if current_pattern:
        patterns.append(current_pattern)
        current_pattern = []

def h_mirrored(pattern, after_column):
    l = min(after_column, len(pattern[0])-after_column)
    errors = 0
    for line in pattern:
        t1 = line[after_column-l:after_column]
        t2 = list(reversed(line[after_column:after_column+l]))
        for i in range(0,len(t1)):
            if t1[i] != t2[i]:
                errors += 1
    return errors == 0

def v_mirrored(pattern, after_row):
    l = min(after_row, len(pattern)-after_row)
    t1 = pattern[after_row-l:after_row]
    t2 = list(reversed(pattern[after_row:after_row+l]))
    errors = 0
    for i in range(0,len(t1)):
        for j in range(0,len(pattern[0])):
            if t1[i][j] != t2[i][j]:
                errors += 1
    return errors == 0

print(f"{len(patterns)} patterns loaded")

for l in patterns[0]:
    print(l)

total = 0
for p in patterns:
    for x in range(1,len(p[0])):
        if h_mirrored(p, x):
            total += x
    for y in range(1, len(p)):
        if v_mirrored(p, y):
            total += 100*y
print(total)
