#!/usr/bin/env python3

with open("input11.txt") as f:
    input_rows = [l.strip() for l in f.readlines()]

expanding_rows = [n for n in range(0,len(input_rows)) if '#' not in input_rows[n]]
expanding_cols = []
for c in range(0, len(input_rows[0])):
    if not any([row[c]=='#' for row in input_rows]):
        expanding_cols.append(c)
print(f"Expanding cols are {expanding_cols}; rows are {expanding_rows}")

galaxy_locations = []

for (y,row) in enumerate(input_rows):
    gal_x = [n for n in range(0,len(row)) if row[n]=='#']
    galaxy_locations.extend([(x,y) for x in gal_x])

print(galaxy_locations)

def sum_distances(galaxy_locations, expanding_cols, expanding_rows, expansion):
    distance_sum = 0
    for i in range(0,len(galaxy_locations)):
        for j in range(0,i):
            (x1,y1) = galaxy_locations[i]
            (x2,y2) = galaxy_locations[j]
            x_travel = range(min(x1,x2)+1, max(x1,x2)+1)
            y_travel = range(min(y1,y2)+1, max(y1,y2)+1)
            dist = abs(x2-x1) + abs(y2-y1)
            dist += (expansion-1)*sum([1 if x in expanding_cols else 0 for x in x_travel])
            dist += (expansion-1)*sum([1 if y in expanding_rows else 0 for y in y_travel])
            distance_sum += dist
    return distance_sum

part1sum = sum_distances(galaxy_locations, expanding_cols, expanding_rows, 2)
print(f"Total distance between all pairs with expansion=2: {part1sum}")

part2sum = sum_distances(galaxy_locations, expanding_cols, expanding_rows, 1000000)
print(f"Total distance between all pairs with expansion=1000000: {part2sum}")

