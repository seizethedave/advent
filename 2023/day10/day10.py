import sys

Start = 'S'
PipeNE = 'L'
PipeNW = 'J'
PipeSE = 'F'
PipeSW = '7'
PipeNS = '|'
PipeEW = '-'

N = (-1, 0)
E = (0, 1)
W = (0, -1)
S = (1, 0)

Turns = {
    # This says that a NE pipe (L) will turn a southward trajectory east
    # and a westward trajectory north.
    PipeNE: [(S, E), (W, N)],
    PipeNW: [(E, N), (S, W)],
    PipeSE: [(N, E), (W, S)],
    PipeSW: [(E, S), (N, W)],
    # And the straight pipes just keep on trucking:
    PipeNS: [(S, S), (N, N)],
    PipeEW: [(E, E), (W, W)],
}

PipesNorth = {PipeNE, PipeNW, PipeNS}
PipesSouth = {PipeSE, PipeNS, PipeSW}
PipesEast = {PipeNE, PipeSE, PipeEW}
PipesWest = {PipeNW, PipeSW, PipeEW}

def grid_get(grid, y, x):
    try:
        return grid[y][x]
    except IndexError:
        return None

class Cursor:
    def __init__(self, grid, y, x, dy, dx):
        self.grid = grid
        self.x = x
        self.y = y
        self.dy = dy
        self.dx = dx

    def step(self):
        self.y += self.dy
        self.x += self.dx
        ch = grid_get(grid, self.y, self.x)
        assert ch is not None
        for (src, dest) in Turns[ch]:
            if (self.dy, self.dx) == src:
                self.dy, self.dx = dest
                break

    @property
    def pos(self):
        return (self.y, self.x)

if __name__ == "__main__":
    grid = []
    startY = None
    startX = None
    for y, line in enumerate(sys.stdin):
        ll = line.strip()
        if (start := ll.find(Start)) != -1:
            startY = y
            startX = start
        grid.append(ll)

    dirs = []

    if grid_get(grid, startY-1, startX) in PipesSouth:
        dirs.append((-1, 0))
    if grid_get(grid, startY, startX+1) in PipesWest:
        dirs.append((0, 1))
    if grid_get(grid, startY, startX-1) in PipesEast:
        dirs.append((0, -1))
    if grid_get(grid, startY+1, startX) in PipesNorth:
        dirs.append((1, 0))

    (dy1, dx1), (dy2, dx2) = dirs
    cursor1 = Cursor(grid, startY, startX, dy1, dx1)
    cursor2 = Cursor(grid, startY, startX, dy2, dx2)

    steps = 0
    visited = {(startY, startX)}
    while True:
        cursor1.step()
        cursor2.step()
        if cursor1.pos in visited or cursor2.pos in visited:
            break
        steps += 1
        visited.add(cursor1.pos)
        visited.add(cursor2.pos)
        print("{} {}".format(cursor1.pos, cursor2.pos))

    print(steps)