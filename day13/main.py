import itertools
import math

from typing import List, Tuple

        
def get_solution(values: List[Tuple[int, int]], search_from: int) -> int:
    # Returns the first solution that solves the problem for the given
    # set of [(phase, minute), ...]
    
    search_step = math.lcm(*[m for _, m in values[:-1]])
    for n in itertools.count(search_from, search_step):
        for phase, minute in values:
            if (n + phase) % minute != 0:
                break  # This multiple doesn't satisfy at least one of the phase/minute combos
        else:  # Got through all the values! Found our solution.
            return n


with open('input') as input_file:
    departure_time = int(input_file.readline().strip())
    values = [s for s in input_file.readline().strip().split(',')]
    values = [(idx, int(i)) for idx, i in enumerate(values) if i != 'x']
    
earliest_bus = (None, 1000000000000)
for _, minute in values:
    nearest_departure = math.ceil(departure_time / minute) * minute
    if nearest_departure < earliest_bus[1]:
        earliest_bus = minute, nearest_departure

print(f'Part 1: {earliest_bus[0] * (earliest_bus[1] - departure_time)}')

search_from = 0
for i in range(2, len(values) + 1):
    search_from = get_solution(values[:i], search_from)

print(f'Part 2: {search_from}')