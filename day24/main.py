import regex

from collections import deque
from copy import deepcopy
from functools import lru_cache


NEIGHBOR_DIRECTIONS = {
    'e': (1, -1, 0),
    'se': (0, -1, 1),
    'sw': (-1, 0, 1),
    'w': (-1, 1, 0),
    'nw': (0, 1, -1),
    'ne': (1, 0, -1),
}


@lru_cache
def neighbors(coord):
    # this is 3x faster than the commented line
    yield (coord[0] + 1, coord[1] - 1, coord[2])
    yield (coord[0], coord[1] - 1, coord[2] + 1)
    yield (coord[0] - 1, coord[1], coord[2] + 1)
    yield (coord[0] - 1, coord[1] + 1, coord[2])
    yield (coord[0], coord[1] + 1, coord[2] - 1)
    yield (coord[0] + 1, coord[1], coord[2] - 1)
    # yield from (tuple(t + offset for t, offset in zip(coord, d)) for d in NEIGHBOR_DIRECTIONS.values())


input_regex = regex.compile(r'(e|se|sw|w|nw|ne)+')
with open('input') as input_file:
    flip_dirs = [input_regex.match(s.strip()).captures(1) for s in input_file]

black_tiles = set()
for flips in flip_dirs:
    # Converts each 'movement' into an offset vector and sums them up into a new tuple
    tile_pos = tuple(sum(col) for col in zip(*map(lambda d: NEIGHBOR_DIRECTIONS[d], flips)))

    if tile_pos in black_tiles:
        black_tiles.remove(tile_pos)
    else:
        black_tiles.add(tile_pos)

print(f'Part 1: {len(black_tiles)}')

day = 0
while (day := day + 1) <= 100:
    tiles_to_process = set(black_tiles)
    for coord in black_tiles:
        tiles_to_process.update(neighbors(coord))

    new_black_tiles = set()
    for coord in tiles_to_process:
        num_adjacent_black_tiles = sum(1 for c in neighbors(coord) if c in black_tiles)
        if num_adjacent_black_tiles == 2 and coord not in black_tiles:
            new_black_tiles.add(coord)
        elif num_adjacent_black_tiles in (1, 2) and coord in black_tiles:
            new_black_tiles.add(coord)

    black_tiles = new_black_tiles

print(f'Part 2: {len(black_tiles)}')
