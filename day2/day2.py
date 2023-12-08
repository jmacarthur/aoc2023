#!/usr/bin/env python3

import re

game_regex = re.compile("Game (\d+): (.*)")

def process_colours(set_text):
    (r,g,b) = (0,0,0)
    for field in set_text.split(", "):
        subfields = field.split()
        if subfields[1] == "red":
            r = int(subfields[0])
        elif subfields[1] == "green":
            g = int(subfields[0])
        elif subfields[1] == "blue":
            b = int(subfields[0])
        else:
            print(f"Odd field: {field}")
            assert False
    return (r,g,b)

games = {}

with open("input2.txt") as f:
    for l in f.readlines():
        m = game_regex.match(l)
        if m:
            game = m.group(1)
            remainder = m.group(2)
            sets = [process_colours(s) for s in remainder.split("; ")]
            print (game,sets)
            games[int(game)] = sets
        else:
            print(f"Odd line: {l}")
            assert False

def valid_game(sets):
    for (r,g,b) in sets:
        if r>12 or g>13 or b>14:
            return False
    return True

total = 0
total_power = 0

for (key, sets) in games.items():
    if valid_game(sets):
        total += key
    max_red = max([s[0] for s in sets])
    max_green = max([s[1] for s in sets])
    max_blue = max([s[2] for s in sets])
    print(key, valid_game(sets), max_red*max_green*max_blue)
    total_power += max_red*max_green*max_blue

print(f"Total of IDs for valid games (part 1): {total}")
print(f"Total of power for game sets (part 2): {total_power}")
