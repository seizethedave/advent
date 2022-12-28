import sys
import itertools

Active = "#"
Inactive = "."
Dirs = (-1, 0, +1)
Increments = [d for d in itertools.product(Dirs, Dirs, Dirs) if d != (0, 0, 0)]

data = set()
frontier = [(0, 0), (0, 0), (0, 0)]

def active_neighbors(x, y, z):
    """
    Return coordinates of active neighboring cubes.
    """
    hits = []
    for dx, dy, dz in Increments:
        coord = (x + dx, y + dy, z + dz)
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
                c = (x, y, z)
                actives = len(active_neighbors(x, y, z))
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
            set_active((x, y, 0))

for _ in range(6):
    transform()
print(len(data))