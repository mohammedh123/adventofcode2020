from functools import partial, reduce
from typing import List, Tuple


def generate_coordinates(slope: Tuple[int, int], max_y: int) -> Tuple[int, int]:
    x, y = slope
    while y < max_y:
        yield x, y
        x += slope[0]
        y += slope[1]


def is_tree_at_location(tile: List[str], x: int, y: int) -> bool:
    return tile[y][x % len(tile[y])] == '#'


def count_trees(tile: List[str], slope: Tuple[int, int]) -> int:
    return sum(is_tree_at_location(tile, x, y) for x, y in generate_coordinates(slope, max_y=len(tile)))


tile: List[str]
with open('input') as input_file:
    tile = [l.strip() for l in input_file]

print(f'Part 1: {count_trees(tile, (3, 1))}')

slopes = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]
print(f'Part 2: {reduce(lambda x, y: x*y, map(partial(count_trees, tile), slopes))}')
