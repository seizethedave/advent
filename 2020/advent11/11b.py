import sys
from itertools import chain

Floor = "."
Empty = "L"
Occupied = "#"

SeatStates = [Empty, Occupied]

lines = [list(l.strip()) for l in sys.stdin]

def iter_visible(y, x, seats):
    """
    Walk from (y, x) in each of the 8 directions until a "visible" seat is encountered.
    """
    for dy, dx in [
        (-1, -1), (-1, 0), (-1, +1),
        ( 0, -1),          ( 0, +1),
        (+1, -1), (+1, 0), (+1, +1),
    ]:
        yy = y
        xx = x
        while True:
            yy += dy
            xx += dx
            if not(0 <= yy < len(seats) and 0 <= xx < len(seats[0])):
                break
            if seats[yy][xx] in SeatStates:
                yield seats[yy][xx]
                break


def transform(seats):
    actions = []

    for y, row in enumerate(seats):
        for x, seatval in enumerate(row):
            if seatval == Floor:
                continue

            visible_neighbors = len(
                [n for n in iter_visible(y, x, seats) if n == Occupied]
            )

            if seatval == Empty and visible_neighbors == 0:
                actions.append((y, x, Occupied))
            elif seatval == Occupied and visible_neighbors >= 5:
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