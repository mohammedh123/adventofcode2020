from collections import deque
from copy import deepcopy
from itertools import chain
from operator import attrgetter


class CupNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


class CupSet:
    def __init__(self, list_of_cup_values):
        self.original_length = len(list_of_cup_values)
        
        # Use all the memory in the world for an O(1) find
        self.node_list = [0] * (len(list_of_cup_values) + 1)  # 1-indexed because lazy
        self.head = None

        previous_node = None
        for val in list_of_cup_values:
            new_node = CupNode(val)
            self.node_list[val] = new_node

            if not self.head:
                self.head = new_node

            if previous_node:
                previous_node.next = new_node

            previous_node = new_node

        # previous_node = final node in the list -- link it back to the first
        previous_node.next = self.head        

    def remove_next_n(self, n):
        # We take advantage of the fact that we know cup values
        # includes all the values from 1 to the length of the values
        # when calculating max/min
        new_next = self.head.next
        for _ in range(n):
            yield new_next
            new_next = new_next.next

        self.head.next = new_next

    def readd_cups_at_destination_value(self, destination_value, cups):
        # Assumes cups is 3-tuple of CupNode
        destination_node = self.find(destination_value)
        old_destination_next = destination_node.next
        destination_node.next = cups[0]
        cups[2].next = old_destination_next

    def find(self, val):
        # Assumes the value is in the cup set
        return self.node_list[val]

    def advance_head(self):
        self.head = self.head.next
        
    def advance_until_value(self, val):
        self.head = self.find(val)

    def values(self):
        seen = set()
        head = self.head
        while head:
            if head.val in seen:
                break
            seen.add(head.val)
            yield head.val
            head = head.next


def play_game(cups, final_turn):
    turn = 0

    get_val = attrgetter('val')
    while (turn := turn + 1) <= final_turn:
        cup = cups.head.val

        removed_cups = tuple(cups.remove_next_n(3))

        destination_cup_value = cup - 1
        if destination_cup_value < 1:
            destination_cup_value = cups.original_length

        while destination_cup_value in map(get_val, removed_cups):
            destination_cup_value -= 1
            
            if destination_cup_value < 1:
                destination_cup_value = cups.original_length

        cups.readd_cups_at_destination_value(destination_cup_value, removed_cups)
        cups.advance_head()

    return cups


with open('input') as input_file:
    cups = list(map(int, input_file.readline().strip()))

cupset = CupSet(cups)
pt1_result = play_game(cupset, 100)
cupset.advance_until_value(1)
print(f'Part 1: {"".join(map(str, list(cupset.values())[1:]))}')

p2_cups = list(chain(cups, range(max(cups) + 1, 1000001)))
cupset = CupSet(p2_cups)
pt2_result = play_game(cupset, 10000000)
cupset.advance_until_value(1)
result = cupset.head.next.val * cupset.head.next.next.val
print(f'Part 2: {result}')