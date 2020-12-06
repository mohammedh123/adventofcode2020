from collections import Counter
from itertools import chain
from typing import List


groups: List[List[str]]
with open('input') as input_file:
    groups = [group.split() for group in input_file.read().split('\n\n')]

print(f'Part 1: {sum(len(set(chain.from_iterable(g))) for g in groups)}')

sum: int = 0
for group in groups:
    # Count up how many people have answered each question per group
    counter = Counter(chain.from_iterable(group))
    
    # ...and sum up how many questions have been answered by everyone in the group
    sum += len([c for c in counter.values() if c == len(group)])

print(f'Part 2: {sum}')