import sys
from itertools import chain

Floor = "."
Empty = "L"
Occupied = "#"

lines = [list(l.strip()) for l in sys.stdin]

def iter_adjacent(y, x, seats):
    for dy, dx in [
        (-1, -1), (-1, 0), (-1, +1),
        ( 0, -1),          ( 0, +1),
        (+1, -1), (+1, 0), (+1, +1),
    ]:
        yy = y + dy
        xx = x + dx
        if 0 <= yy < len(seats) and 0 <= xx < len(seats[0]):
            yield seats[yy][xx]

def transform(seats):
    actions = []

    for y, row in enumerate(seats):
        for x, seatval in enumerate(row):
            if seatval == Floor:
                continue

            occupied_neighbors = len(
                [n for n in iter_adjacent(y, x, seats) if n == Occupied]
            )

            if seatval == Empty and occupied_neighbors == 0:
                actions.append((y, x, Occupied))
            elif seatval == Occupied and occupied_neighbors >= 4:
                actions.append((y, x, Empty))

    # Otherwise apply the actions.
    for y, x, state in actions:
        seats[y][x] = state

    return len(actions) > 0

while True:
    if not transform(lines):
        print(
            len([s for s in chain.from_iterable(lines) if s == Occupied])
        )
        break