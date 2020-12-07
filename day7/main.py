import re

from collections import defaultdict, deque
from typing import List, Set, Tuple


EMPTY_BAG = 'no other bags'
INPUT_REGEX = re.compile(r'(?P<bag_type>[\w ]+) bags contain (?P<contents>.+)\.$')
CONTENT_REGEX = re.compile(r'(?P<count>\d+) (?P<bag_type>[\w ]+) bags?')

# Use two graphs because I'm too lazy to implement a bidirectional graph that
# works for key -> list(values). We'll use one for part 1, one for part 2.
contains_graph = defaultdict(list)
contained_by_graph = defaultdict(list)

# Used for part 2; correlates with contains_graph
weights = {}


def parse_bag_contents(content: str) -> Tuple[int, str]:
    match = CONTENT_REGEX.match(content)
    return int(match.group('count')), match.group('bag_type')


def populate_graphs(lines: List[str]):
    for line in lines:
        match = INPUT_REGEX.match(line)
        bag_type = match.group('bag_type')
        contents = match.group('contents')

        if contents == EMPTY_BAG:
            continue

        for count, contained_bag_type in map(parse_bag_contents, contents.split(', ')):
            contained_by_graph[contained_bag_type].append(bag_type)

            contains_graph[bag_type].append(contained_bag_type)
            weights[(bag_type, contained_bag_type)] = count


with open('input') as input_file:
    lines = [l.strip() for l in input_file]

populate_graphs(lines)

seen_bag_types = set()
bags_to_process = deque(contained_by_graph['shiny gold'])

while bags_to_process:
    bag_type = bags_to_process.popleft()
    bags_to_process.extend(contained_by_graph[bag_type])
    seen_bag_types.add(bag_type)

print(f'Part 1: {len(seen_bag_types)}')

bags_to_process = deque([('shiny gold', 1)])
total = 0

# Basically: add bag amounts as you traverse, while propagating the "bag multiplier" (how many bags this bag is in)
while bags_to_process:
    bag_type, multiplier = bags_to_process.popleft()

    for contained_bag_type in contains_graph[bag_type]:
        bag_count = weights[(bag_type, contained_bag_type)]
        bags_to_process.append((contained_bag_type, multiplier * bag_count))
        total += multiplier * bag_count

print(f'Part 2: {total}')
