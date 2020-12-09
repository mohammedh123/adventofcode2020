from typing import Set


def has_sum_pair(nums: Set[int], sum: int) -> bool:
    # Special case: a number is exactly half of the sum
    return any((sum - n in nums) and n * 2 != sum for n in nums)


with open('input') as input_file:
    input = [int(l.strip()) for l in input_file.readlines()]

preamble_size = 25
invalid_number = -1
for idx, num in enumerate(input[preamble_size:], preamble_size):
    if not has_sum_pair(set(input[idx - preamble_size:idx]), num):
        invalid_number = num
        print(f'Part 1: {invalid_number}')
        break

left_window_idx = 0
right_window_idx = 0
window_sum = input[left_window_idx]

# Expand window (and keep track of sum) until we hit/surpass the invalid number
while window_sum != invalid_number:
    if window_sum > invalid_number:
        left_window_idx += 1
        window_sum -= input[left_window_idx - 1]
    elif window_sum < invalid_number:
        right_window_idx += 1
        window_sum += input[right_window_idx]

window = input[left_window_idx:right_window_idx+1]
print(f'Part 2: {min(window) + max(window)}')