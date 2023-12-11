import sys

Start = 'S'
PipeNE = 'L'
PipeNW = 'J'
PipeSE = 'F'
PipeSW = '7'
PipeNS = '|'
PipeEW = '-'
Ground = '.'

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

PipesNorth = {k for k, v in Turns.items() if any(d == N for (_, d) in v)}
PipesSouth = {k for k, v in Turns.items() if any(d == S for (_, d) in v)}
PipesEast = {k for k, v in Turns.items() if any(d == E for (_, d) in v)}
PipesWest = {k for k, v in Turns.items() if any(d == W for (_, d) in v)}

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

def count_contained(grid) -> int:
    # Scan every row L -> R. If we encounter a pipe that extends north, consider
    # that a pipe crossing. Count the ground spots as inside if we've done an
    # odd number of crossings.
    inside = 0
    for row in grid:
        crossed = 0
        for col in row:
            if col in PipesNorth:
                crossed += 1
            elif col == Ground:
                inside += crossed % 2
    return inside

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
        dirs.append(N)
    if grid_get(grid, startY, startX+1) in PipesWest:
        dirs.append(E)
    if grid_get(grid, startY, startX-1) in PipesEast:
        dirs.append(W)
    if grid_get(grid, startY+1, startX) in PipesNorth:
        dirs.append(S)

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

    print(steps)

    # Part 2. Figure out what S was, then make a cleaned grid where all
    # the "junk" pipes are replaced with ground characters.

    sd = set(dirs)
    if sd == {N, E}:
        s = PipeNE
    elif sd == {N, W}:
        s = PipeNW
    elif sd == {S, E}:
        s = PipeSE
    elif sd == {S, W}:
        s = PipeSW
    elif sd == {N, S}:
        s = PipeNS
    elif sd == {E, W}:
        s = PipeEW

    cleaned_grid = []
    for y, row in enumerate(grid):
        clean_row = ''
        for x, char in enumerate(row):
            if char == Start:
                clean_row += s
            else:
                clean_row += char if (y, x) in visited else Ground
        cleaned_grid.append(clean_row)

    print(count_contained(cleaned_grid))
