from collections import deque
from copy import deepcopy


def calculate_score(deck):
    return sum(idx * card for idx, card in enumerate(reversed(deck), 1))


def play_game_pt1(original_p1_deck, original_p2_deck):
    p1_deck = deepcopy(original_p1_deck)
    p2_deck = deepcopy(original_p2_deck)

    while p1_deck and p2_deck:
        p1_top = p1_deck.pop(0)
        p2_top = p2_deck.pop(0)

        if p1_top > p2_top:
            p1_deck.extend((p1_top, p2_top))
        elif p2_top > p1_top:
            p2_deck.extend((p2_top, p1_top))

    return calculate_score(p1_deck), calculate_score(p2_deck)


def play_game_pt2(p1_deck, p2_deck):
    decks_played = set()

    while p1_deck and p2_deck:
        # If we've played this game before, default to P1 winning
        key = (tuple(p1_deck), tuple(p2_deck))
        if key in decks_played:
            return (0, p1_deck)
        decks_played.add(key)

        p1_top = p1_deck.pop(0)
        p2_top = p2_deck.pop(0)

        if len(p1_deck) >= p1_top and len(p2_deck) >= p2_top:
            # Play a new subgame
            winner, _ = play_game_pt2(p1_deck[0:p1_top], p2_deck[0:p2_top])
        else:
            winner = 0 if p1_top > p2_top else 1

        if winner == 0:
            p1_deck.extend((p1_top, p2_top))
        else:
            p2_deck.extend((p2_top, p1_top))

    return (0, p1_deck) if p1_deck else (1, p2_deck)


with open('input') as input_file:
    player_decks = [l.split('\n') for l in input_file.read().split('\n\n')]

p1_deck = list(map(int, player_decks[0][1:]))
p2_deck = list(map(int, player_decks[1][1:]))

print(f'Part 1: {max(play_game_pt1(p1_deck, p2_deck))}')

_, winning_deck = play_game_pt2(p1_deck, p2_deck)
print(f'Part 2: {calculate_score(winning_deck)}')
