from collections import Counter
from dataclasses import dataclass
from typing import Tuple

@dataclass
class PasswordPolicy:
    min_token: int
    max_token: int
    required_char: str


def tokenize(line: str) -> Tuple[PasswordPolicy, str]:
    raw_tokens = line.split()
    policy = PasswordPolicy(*map(int, raw_tokens[0].split('-')), raw_tokens[1][0])
    password = raw_tokens[2]
    
    return policy, password


def is_valid_password_pt1(policy: PasswordPolicy, password: str) -> bool:
    return policy.min_token <= Counter(password)[policy.required_char] <= policy.max_token


def is_valid_password_pt2(policy: PasswordPolicy, password: str) -> bool:
    return (password[policy.min_token-1] == policy.required_char) ^ (password[policy.max_token-1] == policy.required_char)


with open('input') as input_file:
    lines = input_file.readlines()


print('Part 1: ', [is_valid_password_pt1(*tokenize(line)) for line in lines].count(True))
print('Part 2: ', [is_valid_password_pt2(*tokenize(line)) for line in lines].count(True))