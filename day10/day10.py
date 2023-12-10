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

box_drawing_map = {
    "|": "\u2503",
    "-": "\u2501",
    "L": "\u2517",
    "J": "\u251B",
    "7": "\u2513",
    "F": "\u250f",
    "S": "S",
    ".": "."
}

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

cell_exit_mapping['S'] = start_cell.exits

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

inside_outside_map = []
for y in range(0,height):
    inside_outside_map.append([0]*width)

path1 = (start_x, start_y)
path2 = (start_x, start_y)

# Now make the 'big map' - a double scale version of the original for flood filling
big_width = width*2+1
big_height = height*2+1
print(f"Making big map which is {big_width} x {big_height}")
big_map = []
for y in range(0,big_height):
    big_map.append(['.']*big_width)

big_map[start_y*2][start_x*2] = '#'

while True:
    dist = visited_cells[path1]
    (x,y) = path1
    (newpath1, dir1) = next_step(cell_exit_mapping[input_rows[path1[1]][path1[0]]], visited_cells, path1[0], path1[1])
    if newpath1:
        (dx, dy) = direction_to_delta[dir1]
        big_map[dy+y*2][dx+x*2] = '#'
        big_map[dy*2+y*2][dx*2+x*2] = '#'
        visited_cells[newpath1] = dist+1
        path1 = newpath1
    dist = visited_cells[path2]
    (x,y) = path2
    (newpath2, dir2) = next_step(cell_exit_mapping[input_rows[path2[1]][path2[0]]], visited_cells, path2[0], path2[1])
    if newpath2:
        (dx, dy) = direction_to_delta[dir2]
        big_map[dy+y*2][dx+x*2] = '#'
        big_map[dy*2+y*2][dx*2+x*2] = '#'
        visited_cells[newpath2] = dist+1
        path2 = newpath2
    else:
        break

# We still need to join path1 to path2 on the big map.
(x1, y1) = path1
(x2, y2) = path2
(dx, dy) = (x1-x2, y1-y2)
big_map[y2*2+dy][x2*2+dx] = '#'

longest_path = max(visited_cells.values())

print(f"Longest path: {longest_path}")

# This is just a visualisation.
for (y,row) in enumerate(input_rows):
    line = ""
    for(x,char) in enumerate(row):
        if (x,y) in visited_cells:
            line += box_drawing_map[char]
        else:
            line += "."
    print(line)

# Look for a point inside the map. This won't always work,
# if for example the loop is a square whose left edge is at x=0,
# but for any map in the examples and input it's fine.
flood_start_x = None
flood_start_y = None
for (rownumber, row) in enumerate(big_map):
    line = ''.join(row)
    if ".#." in line:
        flood_start_x = line.index(".#.")+2
        flood_start_y = rownumber
        break

assert x is not None, "No entry pattern found"

print(f"Starting flood at {flood_start_x}, {flood_start_y}")

big_map[flood_start_y][flood_start_x] = ' '

# Perform an iterative flood fill
while True:
    flooding = 0
    for y in range(0, len(big_map)):
        for x in range(0, len(big_map[0])):
            if big_map[y][x] != ' ':
                continue
            for (dx,dy) in direction_to_delta.values():
                if x+dx < 0 or x+dx >= big_width or y+dy < 0 or y+dy >= big_height:
                    continue
                if big_map[y+dy][x+dx] == '.':
                    big_map[y+dy][x+dx] = ' '
                    flooding += 1
    if flooding == 0:
        break

# You can print the big map here, but it's a bit big for most terminals.
if False:
    for row in big_map:
        print (''.join(row))

# Now count up how many even-numbered grid squares have spaces:
inside_spaces = 0
for y in range(0, big_height, 2):
    for x in range(0, big_width, 2):
        if big_map[y][x] == ' ':
            inside_spaces += 1

print(f"{inside_spaces} interior spaces")
