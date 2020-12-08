from collections import deque
from enum import Enum
from typing import List, Tuple


class OpCode(Enum):
    JUMP = 'jmp'
    ACCUMULATOR = 'acc'
    NOOP = 'nop'


def invert_instruction(opcode: OpCode, arg: int) -> Tuple[OpCode, int]:
    if opcode == OpCode.JUMP:
        return OpCode.NOOP, arg
    elif opcode == OpCode.NOOP:
        return OpCode.JUMP, arg
    return opcode, arg


def invert_instructions_at_idx(instructions: List[Tuple[OpCode, int]], idx: int) -> List[Tuple[OpCode, int]]:
    instructions[idx] = invert_instruction(*instructions[idx])
    return instructions


def execute_instructions(instructions: List[Tuple[OpCode, int]]) -> Tuple[int, bool]:
    # Returns the accumulator up until escape (either through infinite-loop
    # detection, or finishing execution), and whether or not the program
    # successfully completes.

    executed_instr_idxs = set()
    instr_idx = 0
    accumulator = 0

    while instr_idx not in executed_instr_idxs and instr_idx < len(instructions):
        executed_instr_idxs.add(instr_idx)
        
        current_opcode, arg = instructions[instr_idx]
        
        if current_opcode == OpCode.ACCUMULATOR:
            accumulator += arg
            instr_idx += 1
        elif current_opcode == OpCode.JUMP:
            instr_idx += arg
        elif current_opcode == OpCode.NOOP:
            instr_idx += 1
    
    return accumulator, instr_idx == len(instructions)


instructions: List[Tuple[str, int]]
with open('input') as input_file:
    instructions = [(OpCode(l[0:3]), int(l[4:])) for l in input_file]

print(f'Part 1: {execute_instructions(instructions)[0]}')

# Just bruteforce part 2 since backtracking looks hella ugly
for idx in range(len(instructions)):
    opcode, arg = instructions[idx]
    if opcode == OpCode.ACCUMULATOR:
        continue

    # Try the program as is first, then try it with the current instruction
    # inverted.
    accumulator, completed = execute_instructions(instructions)
    if not completed:
        invert_instructions_at_idx(instructions, idx)
        accumulator, completed = execute_instructions(instructions)
        if not completed:
            invert_instructions_at_idx(instructions, idx)
    
    if completed:
        print(f'Part 2: {accumulator}')
        break
