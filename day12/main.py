from enum import Enum
from typing import List, Tuple


def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return int(abs(x2 - x1) + abs(y2 - y1))


def process_instructions_pt1(instructions: List[Tuple[str, int]]) -> Tuple[int, int]:
    angle = 1 + 0j
    position = 0 + 0j

    for action, value in instructions:
        if action == 'N':
            position += 1j * value
        elif action == 'S':
            position -= 1j * value
        elif action == 'E':
            position += value
        elif action == 'W':
            position -= value
        elif action == 'L':
            angle *= 1j ** (value // 90)  # Multiplying by i^n -> rotates 90*n deg CCW
        elif action == 'R':
            angle /= 1j ** (value // 90)  # Dividing by i^n -> rotates 90*n deg CW
        elif action == 'F':
            position += angle * value

    return position.real, position.imag


def process_instructions_pt2(instructions: List[Tuple[str, int]]) -> Tuple[int, int]:
    position = 0 + 0j
    waypoint = 10 + 1j  # Relative to ship

    for action, value in instructions:
        if action == 'N':
            waypoint += 1j * value
        elif action == 'S':
            waypoint -= 1j * value
        elif action == 'E':
            waypoint += value
        elif action == 'W':
            waypoint -= value
        elif action == 'L':
            waypoint *= 1j ** (value // 90)  # Multiplying by i^n -> rotates 90*n deg CCW
        elif action == 'R':
            waypoint /= 1j ** (value // 90)  # Dividing by i^n -> rotates 90*n deg CW
        elif action == 'F':
            position += waypoint * value

    return position.real, position.imag


with open('input') as input_file:
    instructions = [(i[0], int(i[1:])) for i in (l.strip() for l in input_file)]

pt1_position = process_instructions_pt1(instructions)
print(f'Part 1: {manhattan_distance(0, 0, *pt1_position)}')

pt2_position = process_instructions_pt2(instructions)
print(f'Part 2: {manhattan_distance(0, 0, *pt2_position)}')
