#!/usr/bin/env python3

from functools import partial
# Uses python-astar by Julien Rialland. Get this from https://github.com/jrialland/python-astar.git
from python_astar import astar

with open("test17.txt") as f:
    rows = [[int(x) for x in line.strip()] for line in f.readlines()]

print(rows)

def moves(pos_node, rows):
    pos = pos_node.data
    retrace = pos_node
    for i in range(0,3):
        retrace = retrace.came_from
        if retrace is None:
            break
    (x,y) = pos
    vertical_only = False
    horizontal_only = False
    if retrace:
        (dx,dy) = (x-retrace.data[0], y-retrace.data[1])
        if abs(dx)==3:
            vertical_only = True
        if abs(dy)==3:
            horizontal_only = True
        print(f"Retraced path from {(x,y)} to {(retrace.data[0], retrace.data[1])}; hence, horizontal={horizontal_only}, vertical={vertical_only}")
    width = len(rows[0])
    height = len(rows)
    current_elevation = rows[y][x]
    directions = [(1,0), (0,-1), (-1,0), (0,1)]
    possible_moves = []
    for (dx, dy) in directions:
        if x+dx < 0 or y+dy < 0 or x+dx >= width or y+dy >= height:
            continue
        if vertical_only and dx!=0:
            continue
        if horizontal_only and dy!=0:
            continue
        possible_moves.append((x+dx, y+dy))
    return possible_moves

def move_cost(from_point, to_point, rows):
    (x,y) = to_point
    return rows[y][x]

start = (0,0)
end = (len(rows[0])-1, len(rows)-1)

path = list(astar.find_path( start,
                             end,
                             neighbors_fnct = partial(moves, rows=rows),
                             heuristic_cost_estimate_fnct = lambda a,b: 1,
                             distance_between_fnct = partial(move_cost, rows=rows)))
print(path, len(path))
heat_loss = 0

for pos in path[1:]:
    (x,y) = pos
    heat_loss += rows[y][x]

print(heat_loss)

for row in range(0,len(rows)):
    line = ''
    for col in range(0,len(rows[0])):
        if (col, row) in path:
            line += "*"
        else:
            line += str(rows[row][col])
    print(line)
