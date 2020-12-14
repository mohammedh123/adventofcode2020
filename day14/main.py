import re

from functools import partial
from itertools import chain, combinations
from typing import List, Tuple


# From official Python itertools powerset recipe
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def apply_mask_to_int(mask: str, n: int) -> str:
    result = list(f'{n:036b}')

    for idx, char in enumerate(mask):
        if char != '0':
            result[idx] = char

    return ''.join(result)


def pt1_solution(instructions: List[Tuple[str, str]]) -> int:
    mask = {}
    memory = {}

    for lhs, rhs in instructions:
        if lhs == 'mask':
            # Clear the previous mask, and update
            mask = {}
            for idx, char in filter(lambda t: t[1] != 'X', enumerate(rhs)):
                char = int(char)
                mask[35 - idx] = char
        else:
            # mem command
            match = re.search(r'\[(\d+)\]', lhs)
            address = int(match.group(1))
            value = int(rhs)

            # apply mask before setting value
            for offset, mask_value in mask.items():
                if mask_value == 0:
                    value &= ~(1 << offset)  # Clear the offset'th bit
                elif mask_value == 1:
                    value |= (1 << offset)  # Set the offset'th bit n

            memory[address] = value

    return sum(memory.values())


def pt2_solution(instructions: List[Tuple[str, str]]) -> int:
    mask: str
    memory = {}

    for lhs, rhs in instructions:
        if lhs == 'mask':
            mask = rhs
        else:
            match = re.search(r'\[(\d+)\]', lhs)
            address = int(match.group(1))

            masked_value = apply_mask_to_int(mask, address)

            # Zero-out the X bits (this will be our initial number)
            zerod_value = int(masked_value.replace('X', '0'), 2)

            # Get all the different combos of bits for masked X values
            combos = powerset(i for i, char in enumerate(reversed(mask)) if char == 'X')

            # Now we can just add each of these values to the base
            # and we have our addresses -- set em
            for offset in map(lambda c: sum(map(partial(pow, 2), c)), combos):
                memory[zerod_value + offset] = int(rhs)

    return sum(memory.values())


with open('input') as file_input:
    instrs = [l.strip().split(' = ') for l in file_input]
    instrs = [(lhs, rhs) for lhs, rhs in instrs]

print(f'Part 1: {pt1_solution(instrs)}')
print(f'Part 2: {pt2_solution(instrs)}')
