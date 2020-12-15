from collections import defaultdict, deque
from itertools import chain, count


with open('input') as input_file:
    nums = list(map(int, input_file.readline().split(',')))

latest_num = -1
memory_idxs = defaultdict(lambda: deque([], maxlen=2))


def speak(num: int, idx: int):
    memory_idxs[num].append(idx)
    global latest_num
    latest_num = num

# Set up initial memory
for idx, num in enumerate(nums, 1):
    speak(num, idx)

for idx in count(len(nums) + 1):
    if len(memory_idxs[latest_num]) == 1:  # First time a number has been spoken
        number_to_speak = 0
    else:
        # Get the difference in the last two times we've seen the last number
        number_to_speak = memory_idxs[latest_num][1] - memory_idxs[latest_num][0]

    speak(number_to_speak, idx)

    if idx == 2020:
        print(f'Part 1: {number_to_speak}')
    elif idx == 30000000:
        print(f'Part 2: {number_to_speak}')
        break
