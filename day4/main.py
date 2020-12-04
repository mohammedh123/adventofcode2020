import re

from dataclasses import dataclass
from typing import Dict, List, Tuple


def validate_height(s):
    match = re.match(r'(\d+)(cm|in)', s)
    if not match:
        return False
        
    height, unit = match.groups()    
    if unit == 'cm':
        return 150 <= int(height) <= 193
    elif unit == 'in':
        return 59 <= int(height) <= 76


VALID_EYE_COLORS = frozenset(['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'])
VALIDATORS = {
    'byr': lambda s: int(s) and 1920 <= int(s) <= 2002,
    'iyr': lambda s: int(s) and 2010 <= int(s) <= 2020,
    'eyr': lambda s: int(s) and 2020 <= int(s) <= 2030,
    'hgt': validate_height,
    'hcl': lambda s: bool(re.match(r'#[\da-f]{6}', s)),
    'ecl': lambda s: s in VALID_EYE_COLORS,
    'pid': lambda s: len(s) == 9 and s.isdigit(),
    'cid': lambda s: True,
}


def tokenize(line: str) -> Tuple[str, str]:
    for kvp in line.split():
        yield tuple(kvp.split(':'))


def is_valid_passport_pt1(passport: Dict[str, str]) -> bool:
    missing_fields = set(VALIDATORS.keys()).difference(passport.keys())
    
    return not missing_fields or missing_fields == {'cid'}


def is_valid_passport_pt2(passport: Dict[str, str]) -> bool:
    return is_valid_passport_pt1(passport) and all(VALIDATORS[k](v) for k, v in passport.items())


passports: List[Dict[str, str]] = []
with open('input') as input_file:
    current_passport = []

    for line in input_file:
        line = line.strip()

        if not line:
            passports.append(dict(current_passport))
            current_passport = []
        else:
            current_passport.extend(tokenize(line.strip()))

    passports.append(dict(current_passport))

print(f'Part 1: {[is_valid_passport_pt1(p) for p in passports].count(True)}')
print(f'Part 2: {[is_valid_passport_pt2(p) for p in passports].count(True)}')