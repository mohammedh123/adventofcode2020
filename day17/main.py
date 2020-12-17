import operator

from collections import defaultdict
from copy import deepcopy
from itertools import product
from typing import Set, Tuple


def solve(max_cycles: int, num_dimensions: int, initial_live_set: Set[Tuple]) -> int:
    total_cycles = 0
    live_set = deepcopy(initial_live_set)
    neighbor_offsets = [
        t
        for t in product((-1, 0, 1), repeat=num_dimensions)
        if not all(v == 0 for v in t)
    ]

    for current_cycle in range(0, max_cycles):
        active_neighbor_count_map = defaultdict(int)
        
        # Populate neighbor counts
        for coord in live_set:
            for offset in neighbor_offsets:
                active_neighbor_count_map[tuple(map(operator.add, coord, offset))] += 1

        # Activate/deactivate cells
        next_live_set = set()
        for coord, count in active_neighbor_count_map.items():
            if coord in live_set:
                if active_neighbor_count_map[coord] in (2, 3):
                    next_live_set.add(coord)
            else:
                if active_neighbor_count_map[coord] == 3:
                    next_live_set.add(coord)

        # "Advance" the world state
        live_set = next_live_set

    return len(live_set)

    
with open('input') as input_file:
    initial_world = [l.strip() for l in input_file]

initial_live_set_pt1 = set((x, y, 0) 
    for y in range(len(initial_world))
    for x in range(len(initial_world[y]))
    if initial_world[y][x] == '#'
)

initial_live_set_pt2 = set((x, y, 0, 0) 
    for y in range(len(initial_world))
    for x in range(len(initial_world[y]))
    if initial_world[y][x] == '#'
)

print(f'Part 1: {solve(6, 3, initial_live_set_pt1)}')
print(f'Part 2: {solve(6, 4, initial_live_set_pt2)}')