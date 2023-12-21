#!/usr/bin/env python3

import copy

with open("input21.txt") as f:
    garden = [list(l.strip()) for l in f.readlines()]

for y in range(0,len(garden)):
    if 'S' in garden[y]:
        x = garden[y].index('S')
        garden[y][x] = '.'
        break

print(f"Size is {len(garden[0])}, {len(garden)}. Start at {x}, {y}")

x = 130
y = 0

steps = (131*3)+66+66


def neighbours(x, y, width, height):
    dirs = [ (1,0), (0,-1), (-1,0), (0,1) ]
    n = []
    for (dx,dy) in dirs:
        if x+dx >= 0 and x+dx < width and y+dy >= 0 and y+dy < height:
            n.append((x+dx, y+dy))
    return n

def generate(garden, new_garden):
    width = len(garden[0])
    height = len(garden)
    for y in range(0,height):
        for x in range(0,width):
            if new_garden[y][x] == '#':
                continue
            n = neighbours(x, y, width, height)
            for (tx, ty) in n:
                if garden[ty][tx] == 'O':
                    new_garden[y][x] = 'O'

def count(garden):
    total = 0
    for row in garden:
        total += sum([1 if cell=='O' else 0 for cell in row])
    return total

start_garden = copy.deepcopy(garden)
start_garden[y][x] = 'O'

for i in range(0,steps):
    new_garden = copy.deepcopy(garden)
    generate(start_garden, new_garden)
    start_garden = new_garden

for row in new_garden:
    print(''.join(row))
print(count(new_garden))
