from collections import defaultdict
from typing import List


def pt1_solution(adapter_joltages: List[int]) -> int:
    differences = defaultdict(int)
    current_joltage_rating = 0
    for joltage in adapter_joltages:
        differences[joltage - current_joltage_rating] += 1
        current_joltage_rating = joltage

    # Built-in adapter is always 3 higher than the highest adapter
    differences[3] += 1
    
    return differences[1] * differences[3]


def pt2_solution(adapter_joltages: List[int]) -> int:
    # Assumes adapter_joltages is sorted in asc order
    # Creates a list with a cell for each joltage from 0...max(joltage)+1+3,
    # so we can safely get max(joltage) + 3 without indexing errors
    dp_table = [0] * (adapter_joltages[-1] + 1 + 3)
    
    # Seed the initial value (max + 3)
    dp_table[adapter_joltages[-1] + 3] = 1
        
    # Construct the table backwards
    for joltage in reversed(adapter_joltages):
        dp_table[joltage] = sum(dp_table[joltage + x] for x in (1, 2, 3))

    return dp_table[adapter_joltages[0]]


with open('input') as input_file:
    # Add 0 as a joltage, for the charging outlet
    adapter_joltages = sorted([int(l.strip()) for l in input_file] + [0])

print(f'Part 1: {pt1_solution(adapter_joltages)}')
print(f'Part 2: {pt2_solution(adapter_joltages)}')