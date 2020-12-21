from __future__ import annotations

import re

from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from itertools import chain
from typing import List, Set


@dataclass
class Food:
    ingredients: Set[str]
    possible_allergens: Set[str]


regex = re.compile(r'^(.*) \(contains (.*)\)$')

with open('input') as input_file:
    lines = [l.strip() for l in input_file]

foods = []
all_ingredients = set()
all_allergens = set()
for l in lines:
    match = regex.match(l)
    ingredients = set(match.group(1).split())
    allergens = set(match.group(2).split(', '))
    
    foods.append(Food(ingredients, allergens))
    all_ingredients.update(ingredients)
    all_allergens.update(allergens)

foods_by_allergen = {a: [f for f in foods if a in f.possible_allergens] for a in all_allergens}

ingredient_to_allergen = {}
dangerous_ingredients = set()
queue = deque(all_allergens)
while queue:
    allergen = queue.popleft()
    
    # Go through every food set that contains this allergen
    # If the intersection of the ingredients are 1 element, we are done with this
    common_ingredients = set.intersection(*[set(f.ingredients) for f in foods_by_allergen[allergen]])
    
    # Get rid of "solved" ingredients
    common_ingredients.difference_update(ingredient_to_allergen.keys())

    if len(common_ingredients) == 1:
        ingredient_to_allergen[min(common_ingredients)] = allergen
        dangerous_ingredients.add(min(common_ingredients))
    else:
        # We don't have enough information to do this one. We'll get to it later.
        queue.append(allergen)

no_allergens_ingredients = all_ingredients - dangerous_ingredients
ingredient_counter = Counter(chain.from_iterable(f.ingredients for f in foods))
print(f'Part 1: {sum(ingredient_counter[i] for i in no_allergens_ingredients)}')
print(f'Part 2: {",".join(sorted(ingredient_to_allergen, key=ingredient_to_allergen.get))}')