#!/usr/bin/env python3

from enum import Enum

class Direction(Enum):
    EAST = 0
    NORTH = 1
    WEST = 2
    SOUTH = 3

direction_to_delta = {
    Direction.EAST:  ( 1,  0),
    Direction.WEST:  (-1,  0),
    Direction.NORTH: ( 0, -1),
    Direction.SOUTH: ( 0,  1) }

def opposite(direction):
    return Direction((direction.value + 2) % 4)

def left_of(direction):
    return Direction((direction.value + 1) % 4)

def right_of(direction):
    return Direction((direction.value + 3) % 4)

class Cell():
    def __init__(self):
        self.exits = []

cell_exit_mapping = {
    "|": [Direction.NORTH, Direction.SOUTH],
    "-": [Direction.EAST, Direction.WEST],
    "L": [Direction.NORTH, Direction.EAST],
    "J": [Direction.NORTH, Direction.WEST],
    "7": [Direction.SOUTH, Direction.WEST],
    "F": [Direction.SOUTH, Direction.EAST],
    ".": [] }

with open("input10.txt") as f:
    input_rows = [l.strip() for l in f.readlines()]

width = len(input_rows[0])
height = len(input_rows)

print(f"The map is {width} x {height} cells.")

for (y,row) in enumerate(input_rows):
    if 'S' in row:
        break

start_y = y
start_x = input_rows[y].index('S')

print(f"Start position is ({start_x}, {start_y}).")

start_cell = Cell()

# Figure out what exits 'S' actually has
for direction, (dx, dy) in direction_to_delta.items():
    if start_y+dy >= height or start_y+dy < 0:
        continue
    if start_x+dx >= width or start_x+dx < 0:
        continue
    neighbour = input_rows[start_y+dy][start_x+dx]
    if opposite(direction) in cell_exit_mapping[neighbour]:
        start_cell.exits.append(direction)

print(f"Start cell has exits: {start_cell.exits}")

visited_cells = { (start_x, start_y): 0 }

assert len(start_cell.exits) == 2

def next_step(exits, visited_cells, x, y):
    global input_rows
    for e in exits:
        (dx, dy) = direction_to_delta[e]
        (tx, ty) = (x+dx, y+dy)
        if (tx, ty) not in visited_cells:
            return ((tx, ty), e)
    return (None, None)

def mark_map_inside(position, direction):
    pass

def mark_map_outside(position, direction):
    pass

(path1, dir1) = next_step(start_cell.exits, visited_cells, start_x, start_y)
visited_cells[path1] = visited_cells[(start_x, start_y)]+1
(path2, dir2) = next_step(start_cell.exits, visited_cells, start_x, start_y)
visited_cells[path2] = visited_cells[(start_x, start_y)]+1

while True:
    dist = visited_cells[path1]
    (newpath1, dir1) = next_step(cell_exit_mapping[input_rows[path1[1]][path1[0]]], visited_cells, path1[0], path1[1])
    if newpath1:
        visited_cells[newpath1] = dist+1
        mark_map_inside(path1, left_of(dir1))
        mark_map_outside(path1, right_of(dir1))
        path1 = newpath1
    dist = visited_cells[path2]
    (newpath2, dir2) = next_step(cell_exit_mapping[input_rows[path2[1]][path2[0]]], visited_cells, path2[0], path2[1])
    if newpath2:
        visited_cells[newpath2] = dist+1
        mark_map_outside(path2, left_of(dir2))
        mark_map_inside(path2, right_of(dir2))
        path2 = newpath2
    else:
        break

print(visited_cells)

longest_path = max(visited_cells.values())

print(f"Longest path: {longest_path}")

