import abc
import re

from collections import deque
from dataclasses import dataclass
from typing import Dict, List


class Rule(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def match(self, text: str) -> List[int]:
        raise NotImplemented


@dataclass
class CompoundRule(Rule):
    subrule_idxs: List[int]

    def match(self, text: str) -> List[int]:
        # Assumes there's a global rulebook
        # This stores the number of characters this rule consumes
        results = []

        # Map indices to the actual rules
        for rule in map(lambda i: rulebook[i], self.subrule_idxs):
            if results:           
                # We need to apply each corresponding subrule to each match
                # and advance the consumed chars count
                results = [r + m for r in results for m in rule.match(text[r:])] 
            else:
                results = rule.match(text)

            # If, after any rule, we have no results left, we can break out early
            if not results:
                return []

        return results


@dataclass
class OrRule(Rule):
    left_clause: CompoundRule
    right_clause: CompoundRule

    def match(self, text: str) -> List[int]:
        return self.left_clause.match(text) + self.right_clause.match(text)


@dataclass
class ConstantRule(Rule):
    constant: str

    def match(self, text: str) -> List[int]:
        if text.startswith(self.constant):
            return [1]

        return []


def get_rulebook_and_values() -> Dict[int, Rule]:
    compound_rule_regex = re.compile(r'^(\d+): ([\d ]+)$')
    or_rule_regex = re.compile(r'^(\d+): ([\d ]+) \| ([\d ]+)$')
    constant_rule_regex = re.compile(r'^(\d+): "(\w)"$')

    with open('input') as input_file:
        rule_lines, values = input_file.read().split('\n\n')
        rule_lines = [s.strip() for s in rule_lines.split('\n')]
        values = [s.strip() for s in values.split('\n')]

    rulebook = {}
    for l in rule_lines:
        if match := compound_rule_regex.match(l):
            rulebook[int(match.group(1))] = CompoundRule(list(map(int, match.group(2).split())))
        elif match := or_rule_regex.match(l):
            left_clause = CompoundRule(list(map(int, match.group(2).split())))
            right_clause = CompoundRule(list(map(int, match.group(3).split())))
            rulebook[int(match.group(1))] = OrRule(left_clause, right_clause)
        elif match := constant_rule_regex.match(l):
            rulebook[int(match.group(1))] = ConstantRule(match.group(2))

    return rulebook, values


def get_total_matches(rulebook: Dict[int, Rule], values: List[str]) -> int:
    total_matches = 0
    for v in values:
        results = rulebook[0].match(v)
        if any(chars_consumed == len(v) for chars_consumed in results):
            total_matches += 1
    return total_matches


if __name__ == "__main__":
    rulebook, values = get_rulebook_and_values()
    print(f'Part 1: {get_total_matches(rulebook, values)}')

    # Update rulebook for pt 2
    rulebook[8] = OrRule(
        left_clause=CompoundRule([42]),
        right_clause=CompoundRule([42, 8])
    )
    rulebook[11] = OrRule(
        left_clause=CompoundRule([42, 31]),
        right_clause=CompoundRule([42, 11, 31])
    )
    print(f'Part 2: {get_total_matches(rulebook, values)}')