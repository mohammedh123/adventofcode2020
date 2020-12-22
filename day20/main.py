from __future__ import annotations

import numpy as np
import re

from collections import defaultdict, deque
from functools import cached_property
from math import isqrt, prod
from typing import Dict, List


class Tile:    
    def __init__(self, tile_id: int, data: List[str]):
        self.tile_id = tile_id
        self.reference_data = np.array([list(l) for l in data])
        self.neighbors = {}
        self.rotation = 0
        # Preload the rotated arrays
        # Note that numpy rotates CCW, so to be consistent with our CW winding,
        # we need to multiply k by -1        
        self.rotated_data = [np.rot90(self.reference_data, -num_rots) for num_rots in range(0, 4)]

    @property
    def borders(self):
        # order is: [N, E, S, W]; aka idx * 90 corresponds to angle
        return [
            ''.join(self.data[0]),
            ''.join(self.data[:,-1]),
            ''.join(reversed(self.data[-1])),
            ''.join(reversed(self.data[:,0])),
        ]

    @property
    def data(self):
        return self.rotated_data[self.rotation]

    def flip_horizontally(self):
        self.rotated_data = [np.fliplr(a) for a in self.rotated_data]
        
    def flip_vertically(self):
        self.rotated_data = [np.flipud(a) for a in self.rotated_data]

    def rotate(self, num_90_degree_rotations: int):
        self.rotation = (self.rotation + num_90_degree_rotations) % 4

    def set_neighbor(self, idx: int, tile: Tile):
        self.neighbors[idx] = tile

    def strip_borders(self):
        self.rotated_data = [a[1:-1,1:-1] for a in self.rotated_data]


def search_image_for_pattern(image_data: List[List[str]], pattern: List[str]):
    pattern_width = max(x for x, y in pattern) + 1
    pattern_height = max(y for x, y in pattern) + 1

    matching_coords = []
    for y in range(len(image_data) - pattern_height):
        for x in range(len(image_data[0]) - pattern_width):
            for dx, dy in pattern:
                if not image_data[y + dy][x + dx] == '#':
                    break  # This x,y combo won't work
            else:  # Got through the entire pattern, found a hit.
                matching_coords.append((x, y))

    return matching_coords


def is_tile_sharing_borders(tile_a: Tile, tile_b: Tile) -> bool:
    # If a border of A is equal to a border of B, that means B needs to be flipped.
    # If a border of A is equal to a border of B that's been REVERSED, that means B
    # doesn't need to be flipped.
    for idx, border in enumerate(tile_a.borders):
        for other_idx, other_border in enumerate(tile_b.borders):
            if border == other_border or border == other_border[::-1]:
                return True
    return False


def get_adjacencies(tiles: List[Tile]):
    adjacencies = defaultdict(list)
    
    for tile in tiles:
        for other_tile in tiles:
            if tile == other_tile: continue

            if is_tile_sharing_borders(tile, other_tile):
                adjacencies[tile.tile_id].append(other_tile)

    return adjacencies


with open('input') as input_file:
    tile_strs = [t.split('\n') for t in input_file.read().split('\n\n')]
    tiles = []
    tile_map = {}
    for tile_str in tile_strs:
        match = re.match(r'^Tile (\d+)\:$', tile_str[0])
        tile_id = int(match.group(1))
        tiles.append(Tile(tile_id, tile_str[1:]))
        tile_map[tile_id] = tiles[-1]

# Determine size of grid
size = isqrt(len(tiles))
tile_grid = [[0]*size for _ in range(size)]  # 2D grid with dummy values

adjacencies = get_adjacencies(tiles)
processed_tile_ids = set()
tiles_to_process = deque([tiles[0]])

while tiles_to_process:
    tile = tiles_to_process.popleft()
    # Go through everyone one of its neighbors and align and set neighborhood
    for neighbor in adjacencies[tile.tile_id]:
        # Ignore tiles that we've already processed
        if neighbor.tile_id in processed_tile_ids:
            continue

        # If any of the tiles need to be flipped, then do it now
        for idx, border in enumerate(tile.borders):
            for other_idx, other_border in enumerate(neighbor.borders):
                rotations_needed_to_align = (idx + 2 - other_idx) % 4
                # If a border of A is equal to a border of B, that means B needs to be flipped.
                # If a border of A is equal to a border of B that's been REVERSED, that means B
                # doesn't need to be flipped.
                if border == other_border:
                    neighbor.rotate(rotations_needed_to_align)
                    if idx % 2 == 0:  # N/S borders needs to flip horizontally
                        neighbor.flip_horizontally()
                    else:
                        neighbor.flip_vertically()
                    tile.set_neighbor(idx, neighbor)
                    neighbor.set_neighbor((idx + 2) % 4, tile)
                elif border == other_border[::-1]:
                    neighbor.rotate(rotations_needed_to_align)
                    tile.set_neighbor(idx, neighbor)
                    neighbor.set_neighbor((idx + 2) % 4, tile)

        # Queue each unprocessed neighbor
        if neighbor.tile_id not in processed_tile_ids:
            tiles_to_process.append(neighbor)

    processed_tile_ids.add(tile.tile_id)

tile_grid = [[0]*size for _ in range(isqrt(len(tiles)))]  # 2D grid with dummy values

# Find top left corner piece to start iterating off of
# NB: corner pieces only have 2 adjacencies, 0 = north, +1 clockwise
corner_tile = next(t for t in tiles if len(t.neighbors) == 2 and 1 in t.neighbors and 2 in t.neighbors)
tiles_to_process = deque([(corner_tile, 0, 0)])
processed_tile_ids = set()
while tiles_to_process:
    tile, x, y = tiles_to_process.popleft()
    if tile.tile_id in processed_tile_ids:
        continue

    # Update tile grid and enqueue the neighbors
    tile_grid[y][x] = tile
    for idx, neighbor in tile.neighbors.items():
        if idx == 0: dx, dy = 0, -1
        elif idx == 1: dx, dy = 1, 0
        elif idx == 2: dx, dy = 0, 1
        elif idx == 3: dx, dy = -1, 0

        tiles_to_process.append((neighbor, x + dx, y + dy))

    processed_tile_ids.add(tile.tile_id)

for tile in tiles:
    tile.strip_borders()

# Form the stitched grid line-by-line
tile_size = len(tile_grid[0][0].data)
total_size = len(tile_grid) * tile_size
image_data = [[0]*total_size for _ in range(total_size)]
for y in range(total_size):
    for x in range(total_size):
        tile_x = x // tile_size
        tile_y = y // tile_size
        tile_data_x = x % tile_size
        tile_data_y = y % tile_size
        image_data[y][x] = tile_grid[tile_y][tile_x].data[tile_data_y][tile_data_x]
reference_image_data = np.array(image_data)

raw_pattern = [
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   ',
]

pattern = [
    (x, y)
    for y in range(len(raw_pattern))
    for x in range(len(raw_pattern[y]))
    if raw_pattern[y][x] == '#'
]

final_view = reference_image_data
final_results = []
for num_rotations in range(4):
    for flip in (False, True):
        view = np.rot90(reference_image_data, num_rotations)
        if flip:
            view = np.flipud(view)

        if results := search_image_for_pattern(view.tolist(), pattern):
            final_results = results
            final_view = view 
            break

print(f'Part 1: {prod([k for k, v in adjacencies.items() if len(v) == 2])}')

sea_monster_coords = set([(tlx + dx, tly + dy) for tlx, tly in final_results for dx, dy in pattern])
pound_coords = set([(x, y) for y in range(total_size) for x in range(total_size) if final_view[y][x] == '#'])
print(f'Part 2: {len(pound_coords - sea_monster_coords)}')