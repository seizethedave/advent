import sys
import itertools

Active = "#"
Inactive = "."
Dirs = (-1, 0, +1)
Dimensions = 4
Increments = [d for d in itertools.product(*([Dirs] * Dimensions)) if d != tuple([0] * Dimensions)]


data = set()
frontier = [(0, 0)] * Dimensions

def active_neighbors(*coords):
    """
    Return coordinates of active neighboring cubes.
    """
    hits = []
    for increments in Increments:
        coord = tuple(a + b for a, b in zip(coords, increments))
        if coord in data:
            hits.append(coord)
    return hits

def set_active(coord):
    global frontier
    data.add(coord)
    # Expand the frontier as needed.
    for i, v in enumerate(coord):
        frontier[i] = (min(frontier[i][0], v - 1), max(frontier[i][1], v + 1))

def transform():
    activate = []
    deactivate = []

    for x in range(frontier[0][0], frontier[0][1] + 1):
        for y in range(frontier[1][0], frontier[1][1] + 1):
            for z in range(frontier[2][0], frontier[2][1] + 1):
                for w in range(frontier[3][0], frontier[3][1] + 1):
                    c = (x, y, z, w)
                    actives = len(active_neighbors(x, y, z, w))
                    if c in data:
                        if actives not in [2, 3]:
                            deactivate.append(c)
                    elif actives == 3:
                        activate.append(c)

    # apply the actions.
    for c in activate:
        set_active(c)
    for c in deactivate:
        data.discard(c)

for y, row in enumerate(sys.stdin):
    for x, ch in enumerate(row):
        if ch == Active:
            set_active((x, y, 0, 0))

for _ in range(6):
    transform()
print(len(data))