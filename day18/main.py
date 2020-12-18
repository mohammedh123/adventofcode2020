import operator as op

from collections import deque
from typing import Dict, List


OPERATORS = '+-*/'


def convert_to_prefix(expr: str, op_precedences: Dict[str, int]) -> List[str]:
    expr = expr.replace(' ', '')

    output = []
    ops = deque()

    for chr in expr:
        if chr in OPERATORS:
            if ops and ops[-1] != '(' and op_precedences[ops[-1]] <= op_precedences[chr]:
                output.append(ops.pop())

            ops.append(chr)
        elif chr == '(':
            ops.append(chr)
        elif chr == ')':
            while (top := ops.pop()) != '(':
                output.append(top)
        else:
            output.append(chr)

    output.extend(reversed(ops))  # dump the rest of the ops stack
    return output


def evaluate_prefix(tokens: List[str]) -> int:
    vals = []
    op_map = {
        '*': op.mul,
        '+': op.add,
    }
    for token in tokens:
        if token in op_map:
            value = op_map[token](vals[-2], vals[-1])
            del vals[-2:]
            vals.append(value)
        else:
            vals.append(int(token))

    return value


with open('input') as input_file:
    solutions = [l.strip() for l in input_file]

pt1_precedence_map = {'+': 1, '*': 1}
pt2_precedence_map = {'+': 1, '*': 2}
print(f'Part 1: {sum(evaluate_prefix(convert_to_prefix(s, pt1_precedence_map)) for s in solutions)}')
print(f'Part 2: {sum(evaluate_prefix(convert_to_prefix(s, pt2_precedence_map)) for s in solutions)}')
