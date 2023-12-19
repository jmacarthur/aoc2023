#!/usr/bin/env python3

plans = []

with open("input18.txt") as f:
    for planline in [l.strip() for l in f.readlines()]:
        fields = planline.split()
        plans.append((fields[0], int(fields[1]), fields[2][2:-1]))

direction_delta = { 'U': (0,-1), 'D': (0,1), 'L': (-1,0), 'R': (1,0) }

x = 0
y = 0
places = [(x,y)]

for p in plans:
    (dx, dy) = direction_delta[p[0]]
    for i in range(0,p[1]):
        x += dx
        y += dy
        if (x,y) in places:
            print(f"Crossing existing path at {(x,y)}")
        else:
            places.append((x,y))

print(f"Path length is {len(places)}")

min_x = min(point[0] for point in places)
max_x = max(point[0] for point in places)
min_y = min(point[1] for point in places)
max_y = max(point[1] for point in places)

print(f"Coordinate ranges: {min_x} -> {max_x}, {min_y} -> {max_y}")

lagoon = []
for i in range(0,max_y-min_y+1):
    lagoon.append(['.'] * (max_x-min_x+1))

x = -min_x
y = -min_y
for p in plans:
    lagoon[y][x] = '#'
    (dx, dy) = direction_delta[p[0]]
    for i in range(0,p[1]):
        x += dx
        y += dy
        lagoon[y][x] = '#'

volume = 0

total_flood = 0
for row in lagoon:
    str_row = ''.join(row)
    if '.#.' in str_row:
        index = str_row.index('.#.')
        if index == str_row.index('#')-1:
            row[index+2] = '*'
            total_flood += 1


def flood(lagoon):
    flooded = 0
    for y in range(1,len(lagoon)-1):
        for x in range(1,len(lagoon[0])-1):
            for (dx,dy) in direction_delta.values():
                if lagoon[y+dy][x+dx] == "*" and lagoon[y][x] == ".":
                    lagoon[y][x] = '*'
                    flooded += 1
    return flooded

while True:
    flooded = flood(lagoon)
    total_flood += flooded
    if flooded == 0:
        break
for row in lagoon:
    print(''.join(row))

print(total_flood, len(places), total_flood+len(places))
