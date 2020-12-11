from copy import deepcopy
from enum import Enum
from functools import cached_property
from itertools import product
from typing import Callable, Iterable, List, Tuple


OCCUPIED = '#'
EMPTY = 'L'
FLOOR = '.'
ADJACENT_OFFSETS = [
    (-1, -1),   (0, -1),    (1, -1),
    (-1, 0),                (1, 0),
    (-1, 1),    (0, 1),     (1, 1),
]


# Assumes to be used with a List[List[str]]
class Grid(list):
    @cached_property
    def width(self) -> int:
        return len(self[0])

    @cached_property
    def height(self) -> int:
        return len(self)


class GridProcessor:
    def __init__(
        self,
        grid: Grid,
        get_offending_occupancies_func: Callable[[List[str], int, int], Iterable[Tuple[int, int]]],
        max_offending_occupants: int,
    ):

        self.grid = grid
        self.get_offending_occupancies_func = get_offending_occupancies_func
        self.max_offending_occupants = max_offending_occupants

    def count_occupied_seats(self) -> int:
        return sum(row.count(OCCUPIED) for row in self.grid)

    def apply_rules(self):
        new_grid = deepcopy(self.grid)

        # Use old grid to check seat status, as to be unaffected by rules
        # updating adjacent seats, but update new grid
        for x, y in product(range(self.grid.width), range(self.grid.height)):
            if self.grid[y][x] == FLOOR:
                continue

            offending_occupancy_count = sum(1 for _ in self.get_offending_occupancies_func(self.grid, x, y))

            if self.grid[y][x] == EMPTY and offending_occupancy_count == 0:
                new_grid[y][x] = OCCUPIED
            elif self.grid[y][x] == OCCUPIED and offending_occupancy_count >= self.max_offending_occupants:
                new_grid[y][x] = EMPTY

        self.grid = new_grid

    def process_seats(self) -> int:
        # Returns the number of seats that are occupied after processing seats with rules
        occupied_seat_count = self.count_occupied_seats()
        while True:
            self.apply_rules()
            new_occupied_seat_count = self.count_occupied_seats()
            if new_occupied_seat_count == occupied_seat_count:
                return occupied_seat_count

            occupied_seat_count = new_occupied_seat_count


def get_adjacent_occupancies(grid: Grid, cx: int, cy: int) -> Tuple[int, int]:
    for dx, dy in ADJACENT_OFFSETS:
        x, y = cx + dx, cy + dy
        if 0 <= x < grid.width and 0 <= y < grid.height and grid[y][x] == OCCUPIED:
            yield x, y


def get_raycast_occupancies(grid: Grid, cx: int, cy: int) -> Tuple[int, int]:
    for dx, dy in ADJACENT_OFFSETS:
        x, y = cx + dx, cy + dy
        # Keep casting the ray until we're off grid or if we hit a seat
        while 0 <= x < grid.width and 0 <= y < grid.height:
            if grid[y][x] == OCCUPIED:
                yield x, y
                break
            elif grid[y][x] == EMPTY:
                break

            x, y = x + dx, y + dy


with open('input') as input_file:
    grid = Grid(list(l.strip()) for l in input_file.readlines())

pt1_processor = GridProcessor(grid, get_adjacent_occupancies, 4)
pt2_processor = GridProcessor(grid, get_raycast_occupancies, 5)
print(f'Part 1: {pt1_processor.process_seats()}')
print(f'Part 2: {pt2_processor.process_seats()}')
