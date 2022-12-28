import sys
from collections import deque
from itertools import islice

def read_one_deck():
    sys.stdin.readline()
    d = deque()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            break
        d.append(int(line))
    return d

def play_game(deck1, deck2):
    game_history = set()

    while deck1 and deck2:
        game_str = "{}|{}".format(
            ",".join(str(s) for s in deck1),
            ",".join(str(s) for s in deck2)
        )
        if game_str in game_history:
            # player 1 wins.
            return 0
        game_history.add(game_str)

        c1, c2 = deck1.popleft(), deck2.popleft()
        if c1 <= len(deck1) and c2 <= len(deck2):
            round_winner = play_game(
                deque(islice(deck1, c1)),
                deque(islice(deck2, c2)),
            )
        else:
            round_winner = 0 if c1 > c2 else 1

        if round_winner == 0:
            deck1.append(c1)
            deck1.append(c2)
        else:
            deck2.append(c2)
            deck2.append(c1)

    return 0 if deck1 else 1

def score_deck(deck):
    return sum(i * c for i, c in enumerate(reversed(deck), start=1))

d1, d2 = read_one_deck(), read_one_deck()
play_game(d1, d2)
print(score_deck(d1 or d2))
