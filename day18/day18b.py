#!/usr/bin/env python3

plans = []

with open("test18.txt") as f:
    for planline in [l.strip() for l in f.readlines()]:
        fields = planline.split()
        hexdata = fields[2][2:-1]
        plans.append((int(hexdata[:5],16), int(hexdata[5], 16)))

direction_delta = { 3: (0,-1), 1: (0,1), 2: (-1,0), 0: (1,0) }

x = 0
y = 0
places = [(x,y)]
wall_length = 0
vertical_walls = []
horizontal_walls = []
for p in plans:
    (dx, dy) = direction_delta[p[1]]
    distance = p[0]

    if p[1] == 1:
        vertical_walls.append((x, y, y+distance))
    elif p[1] == 3:
        vertical_walls.append((x, y-distance, y))
    if p[1] == 0:
        horizontal_walls.append((y, x, x+distance))
    elif p[1] == 2:
        horizontal_walls.append((y, x-distance, x))
    x += dx*distance
    y += dy*distance
    places.append((x,y))
    wall_length += distance

print(f"Path length is {len(places)} nodes; wall length {wall_length}")

max_y = max([p[1] for p in places])
min_y = min([p[1] for p in places])

print(min_y, max_y)

total_flooded = 0
for y in range(min_y, max_y+1):
    row_flooded = 0
    prev_x = None
    walls_in_range = [wall for wall in vertical_walls if y>=wall[1] and y<=wall[2]]
    inside = False
    wall_locations = [w[0] for w in sorted(walls_in_range, key=lambda x:x[0])]
    for x in wall_locations:
        if inside:
            row_flooded += x-prev_x-1
        if any([w[0]==y and w[1]==x for w in horizontal_walls]):
            inside = False
            prev_x = x
            continue
        inside = not inside
        prev_x = x
    total_flooded += row_flooded
    print(f"Row {y} = {row_flooded} {wall_locations}")

vertical_wall_length = sum([w[2]-w[1]-1 for w in vertical_walls])
print(total_flooded, wall_length, total_flooded+wall_length)

