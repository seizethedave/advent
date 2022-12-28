import sys
from collections import deque
import copy
from itertools import zip_longest, chain

Monster = [
    "                  #",
    "#    ##    ##    ###",
    " #  #  #  #  #  #",
]
MonsterWidth = 20
MonsterWeight = 15

FlipH = 1
FlipV = 2

class Tile:
    def __init__(self, tile_id):
        self.tile_id = tile_id
        self.grid = []
        self.right = None
        self.down = None
        self.visited = False

    def link_edges(self):
        if self.right is None:
            yield ('right', [r[-1] for r in self.grid])
        if self.down is None:
            yield ('down', self.grid[-1])

    def get_top_edge_options(self):
        """
        Return (flip type, degree of CW rotation, edge)
        flip/rotation must be applied to grid for edge to actually appear as top edge.
        """
        return [
            (None, 0, self.grid[0]),
            (FlipV, 90, [r[0] for r in self.grid]),
            (FlipH, 180, self.grid[-1]),
            (None, 270, [r[-1] for r in self.grid]),
            (FlipH, 0, self.grid[0][::-1]),
            (None, 90, [r[0] for r in self.grid][::-1]),
            (None, 180, self.grid[-1][::-1]),
            (FlipV, 270, [r[-1] for r in self.grid][::-1]),
        ]

    def get_left_edge_options(self):
        """
        Same as above, but flip/rotation must be applied for edge to appear as left edge.
        """
        return [
            (None, 0, [r[0] for r in self.grid]),
            (None, 90, self.grid[-1]),
            (FlipH, 0, [r[-1] for r in self.grid]),
            (FlipH, 270, self.grid[0]),
            (FlipV, 0, [r[0] for r in self.grid][::-1]),
            (FlipH, 90, self.grid[-1][::-1]),
            (None, 180, [r[-1] for r in self.grid][::-1]),
            (None, 270, self.grid[0][::-1]),
        ]

    def transform(self, flip, rotate):
        # Flip, then rotate.
        if flip == FlipH:
            transformed = [row[::-1] for row in self.grid]
        elif flip == FlipV:
            transformed = copy.deepcopy(self.grid[::-1])
        else:
            transformed = copy.deepcopy(self.grid)

        rotated = copy.deepcopy(transformed)
        sz = len(rotated)

        while rotate > 0:
            source = copy.deepcopy(rotated)
            for i in range(sz):
                for j in range(sz):
                    rotated[i][j] = source[sz - j - 1][i]
            rotate -= 90

        self.grid = rotated

    def link(self, neighbor, tile_dir):
        self.__dict__[tile_dir] = neighbor

    def __repr__(self):
        return f"Tile({self.tile_id})"

# Read input:
tiles = []
for line in sys.stdin:
    line = line.rstrip()
    if line.startswith("Tile"):
        tile = Tile(int(line[5:].rstrip(":")))
        tiles.append(tile)
    elif line:
        tile.grid.append(list(line))

# We know upper left is tile 1439 from part A. Start with 1439 and
# link all tiles with right and down pointers.

upper_left_tile = [t for t in tiles if t.tile_id == 1439][0]
visit_queue = deque([upper_left_tile])

while visit_queue:
    t = visit_queue.popleft()
    if t.visited:
        continue
    t.visited = True
    for direction, e in t.link_edges():
        for t2 in tiles:
            if t.tile_id == t2.tile_id:
                continue
            if direction == "right":
                for flip, rot, e2 in t2.get_left_edge_options():
                    if e == e2:
                        t.link(t2, direction)
                        t2.transform(flip, rot)
                        visit_queue.append(t2)
                        break
            elif direction == "down":
                for flip, rot, e2 in t2.get_top_edge_options():
                    if e == e2:
                        t.link(t2, direction)
                        t2.transform(flip, rot)
                        visit_queue.append(t2)
                        break

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def get_master_grid():
    row = upper_left_tile
    while row is not None:
        tcol = row
        for rownum in range(1, 9):
            tcol = row
            while tcol is not None:
                yield from iter(tcol.grid[rownum][1:-1])
                tcol = tcol.right
        row = row.down

# Form amorphous chars yielded from get_master_grid into new large NxN master grid.
grid_size = 12 * (10 - 2)
big_grid = [list(row) for row in grouper(get_master_grid(), grid_size)]

def is_monster_at_pos(grid, x, y):
    for my, row in enumerate(Monster):
        for mx, char in enumerate(row):
            if char == "#":
                if grid[y + my][x + mx] != char:
                    return False
    else:
        return True

def find_monsters_1d(grid):
    monsters = 0
    for y in range(0, len(grid) - len(Monster)):
        for x in range(0, len(grid[0]) - MonsterWidth):
            if is_monster_at_pos(grid, x, y):
                monsters += 1
    return monsters

def find_monsters_all_transforms():
    master = Tile("master")

    for flip, rot in [
        (None, 0), (None, 90), (None, 180), (None, 270),
        (FlipH, 0), (FlipH, 90), (FlipV, 0), (FlipV, 90),
    ]:
        master.grid = copy.deepcopy(big_grid)
        master.transform(flip, rot)
        monsters = find_monsters_1d(master.grid)
        if monsters:
            print(f"found {monsters} monsters with transform {flip} {rot}")
            monster_chars = monsters * MonsterWeight
            all_chars = len(list(filter(lambda c: c == "#", chain.from_iterable(master.grid))))
            print(f"{all_chars} - {monster_chars} = {all_chars - monster_chars}")
            return

find_monsters_all_transforms()