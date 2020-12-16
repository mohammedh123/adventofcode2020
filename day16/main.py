import re

from dataclasses import dataclass
from itertools import chain, product
from math import prod
from typing import Iterable, List, Tuple


@dataclass
class Rule:
    rule_name: str
    lower_range: Tuple[int, int]
    upper_range: Tuple[int, int]

    def validate_value(self, value: int) -> bool:
        return self.lower_range[0] <= value <= self.lower_range[1] or \
               self.upper_range[0] <= value <= self.upper_range[1]


rules_regex = re.compile(r'([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)')

rules = []
my_ticket: List[int]
nearby_tickets: List[List[int]]
with open('input') as file_input:
    lines = [l.strip() for l in file_input.readlines()]

i = 0
while i < len(lines):
    line = lines[i]

    if match := rules_regex.match(line):
        field_name = match.group(1)
        lower_range = int(match.group(2)), int(match.group(3))
        upper_range = int(match.group(4)), int(match.group(5))
        rules.append(Rule(field_name, lower_range, upper_range))
    elif line == 'your ticket:':
        my_ticket = list(map(int, lines[i + 1].split(',')))
        i += 1  # Skip extra line
    elif line == 'nearby tickets:':
        nearby_tickets = (list(map(int, l.split(','))) for l in lines[i + 1:])
        break  # Done processing input

    i += 1

invalid_tickets = []
valid_tickets = []
invalid_value_sum = 0

for ticket in nearby_tickets:
    is_valid_ticket = True
    for value in ticket:
        if all(not rule.validate_value(value) for rule in rules):
            invalid_value_sum += value
            is_valid_ticket = False

    if is_valid_ticket:
        valid_tickets.append(ticket)
    else:
        invalid_tickets.append(ticket)

print(f'Part 1: {invalid_value_sum}')

# Form the initial 'simplified' list of possible indices
# e.g. for the sample given on the site, it'll look like:
# [[[1, 2],    [0, 1, 2], [0, 1, 2]],
#  [[0, 1],    [0, 1, 2], [0, 1, 2]],
#  [[0, 1, 2], [0, 1],    [0, 1, 2]]]
# You then go column by column, "reducing" the possible values as much as you
# can (by only keeping the common indices)
# e.g. from the above example, we end up with:
# [[1], [0, 1], [0, 1, 2]]
# Now reduce it as much we can, each step looking for lists with 1 element and
# removing them from the rest of the lists and updating our final index list.
# We'll need to do this multiple times, until we're out of elements.
# [[1], [0, 1], [0, 1, 2]]
#   Found a [1] at index 0, so reduce and update our master list [1, -1, -1]
# [[], [0], [0, 2]]
#   Found a [0] at index 1, so reduce and update our master list [1, 0, -1]
# [[], [], [2]]
#   Found a [2] at index 2, so reduce and update our master list [1, 0, 2]
# Now the rest of the problem is just looking up mapped indices.
   
valid_indexes = [[[i for i, r in enumerate(rules) if r.validate_value(v)] for v in vt] for vt in valid_tickets]
interim_indices = [0] * len(rules)  # Dummy initial value, will be a list of sets of size len(rules)
final_indices = [-1] * len(rules)  # Final list of ints indicating indices

for column in range(len(rules)):
    column_idxs = set(range(len(rules)))  # Default to all the rules
    for row in valid_indexes:
        column_idxs.intersection_update(row[column])
        if len(column_idxs) == 1:  # Done with this column
            break
    interim_indices[column] = column_idxs

print(interim_indices)
while final_indices.count(-1):
    # Collect all single elements and cull them from the rest of the set
    single_elements = set()
    for i, idxs in enumerate(interim_indices):
        if len(idxs) == 1:
            final_index = min(idxs)
            single_elements.add(final_index)
            final_indices[i] = final_index
    
    for idxs in interim_indices:
        idxs.difference_update(single_elements)

# Get fields that start with departure and their mapped values
departure_idxs = set(idx for idx, r in enumerate(rules) if r.rule_name.startswith('departure'))
departure_values = []
for i, mapped_idx in enumerate(final_indices):
    if mapped_idx in departure_idxs:
        departure_values.append(my_ticket[i])

print(f'Part 2: {prod(departure_values)}')