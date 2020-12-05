from operator import attrgetter
from typing import List


class BoardingPass:
    """
    The boarding pass row can be determined by representing the "row bits" of the
    pass (first 7 characters) and the "column bits" (next 3 characters) as binary
    (F/L -> 0, B/R -> 1).
    """

    def __init__(self, boarding_pass: str):
        self._boarding_pass_str = boarding_pass
        self._boarding_pass_as_binary_str = boarding_pass.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1')
    
    @property
    def row(self):
        return int(self._boarding_pass_as_binary_str[:7], 2)

    @property
    def column(self):
        return int(self._boarding_pass_as_binary_str[7:], 2)
    
    @property
    def seat_id(self):
        return 8 * self.row + self.column


boarding_passes: List[str] 
with open('input') as input_file:
    boarding_passes = [BoardingPass(l.strip()) for l in input_file.readlines()]

print(f"Part 1: {max(map(attrgetter('seat_id'), boarding_passes))}")

# Find hole in range
sorted_seat_ids = sorted(map(attrgetter('seat_id'), boarding_passes))
for idx in range(len(sorted_seat_ids) - 1):
    if sorted_seat_ids[idx + 1] != sorted_seat_ids[idx] + 1:
        print(f"Part 2: {sorted_seat_ids[idx] + 1}")
        break
    