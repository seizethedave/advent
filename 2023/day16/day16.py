import sys

Empty = '.'
MirrorNESW = '/'
MirrorNWSE = '\\'
SplitNS = '|'
SplitWE = '-'

class Grid:
    def __init__(self, arr, width):
        self.arr = arr
        self.width = width
        self.height = len(arr) // width

    def get(self, y, x):
        if not (0 <= y < self.height and 0 <= x < self.width):
            raise IndexError("out of bounds")
        return self.arr[y * self.width + x]
    
    def search(self, entry_beam):
        # Initially we have one beam. In each iteration march each beam forward
        # and compute a new series of beams based on what those produce. Avoid
        # re-entering the same places with the same directions as they'll just
        # result in loops.
        visited = set()
        history = set()
        beams = [entry_beam]
        while beams:
            nbeams = []
            for b in beams:
                for bb in b.move():
                    if (bb.y, bb.x, bb.dy, bb.dx) not in history:
                        nbeams.append(bb)
                        visited.add((bb.y, bb.x))
                        history.add((bb.y, bb.x, bb.dy, bb.dx))
            beams = nbeams
        return len(visited)

class Beam:
    def __init__(self, grid, dy, dx, y, x):
        self.grid = grid
        self.dy = dy
        self.dx = dx
        self.y = y
        self.x = x

    def move(self) -> ["Beam"]:
        # Move forward as indicated by dy/dx, then return zero or more resulting
        # beams based on the split/mirror/etc rules.
        self.y += self.dy
        self.x += self.dx
        try:
            dest = self.grid.get(self.y, self.x)
        except IndexError:
            # Gone off the grid. This beam is done.
            return []

        if dest == Empty:
            return [self]
        elif dest == SplitNS:
            if self.dy:
                return [self]
            else:
                return [Beam(grid, -1, 0, self.y, self.x), Beam(grid, 1, 0, self.y, self.x)]
        elif dest == SplitWE:
            if self.dy:
                return [Beam(grid, 0, -1, self.y, self.x), Beam(grid, 0, 1, self.y, self.x)]
            else:
                return [self]
        elif dest == MirrorNESW:
            self.dy, self.dx = -self.dx, -self.dy
            return [self]
        elif dest == MirrorNWSE:
            self.dy, self.dx = self.dx, self.dy
            return [self]

def all_entry_beams(grid):
    for y in range(grid.height):
        yield Beam(grid, 0, 1, y, -1)
        yield Beam(grid, 0, -1, y, grid.width)
    for x in range(grid.width):
        yield Beam(grid, 1, 0, -1, x)
        yield Beam(grid, -1, 0, grid.height, x)

if __name__ == "__main__":
    width = 0
    arr = []
    for y, line in enumerate(sys.stdin):
        line = line.rstrip()
        width = len(line)
        arr.extend(line)

    grid = Grid(arr, width)

    # Part 1:
    print(grid.search(Beam(grid, 0, 1, 0, -1)))

    # Part 2:
    print(max(grid.search(b) for b in all_entry_beams(grid)))
