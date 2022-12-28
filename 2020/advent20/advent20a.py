import sys
import math
from collections import defaultdict

class Tile:
    def __init__(self, tile_id):
        self.tile_id = tile_id
        self.grid = []

    def edges(self):
        yield self.grid[0]
        yield self.grid[-1]
        yield ''.join(r[0] for r in self.grid)
        yield ''.join(r[-1] for r in self.grid)

    def __repr__(self):
        return f"Tile({self.tile_id})"

tiles = []
linemap = defaultdict(set)

for line in sys.stdin:
    line = line.rstrip()
    if line.startswith("Tile"):
        tile = Tile(int(line[5:].rstrip(":")))
        tiles.append(tile)
    elif line:
        tile.grid.append(line)

for t in tiles:
    for e in t.edges():
        if e not in linemap:
            e = e[::-1]
        linemap[e].add(t)

c = defaultdict(int)
for e, ts in linemap.items():
    for t in ts:
        c[t] += len(ts)
print(math.prod([k.tile_id for k, v in c.items() if v == 6]))