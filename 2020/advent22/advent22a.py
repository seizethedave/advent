import sys
from collections import deque

def read_one_deck():
    sys.stdin.readline()
    d = deque()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            break
        d.append(int(line))
    return d

d1, d2 = read_one_deck(), read_one_deck()

while d1 and d2:
    c1, c2 = d1.popleft(), d2.popleft()
    assert c1 != c2
    if c1 > c2:
        d1.append(c1)
        d1.append(c2)
    else:
        d2.append(c2)
        d2.append(c1)

def score_deck(deck):
    return sum(i * c for i, c in enumerate(reversed(deck), start=1))

print(score_deck(d1 or d2))
