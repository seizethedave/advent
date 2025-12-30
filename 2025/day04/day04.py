import sys

Empty = "."
Paper = "@"
Limit = 3

dirs = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]

def load_grid():
    g = []
    for line in sys.stdin:
        g.append(list(line.rstrip("\n")))
    return g


if __name__ == "__main__":
    grid = load_grid()

    height = len(grid)
    width = len(grid[0])
    
    marks = []
    for r in grid:
        marks.append([0] * len(r))

    def inc(y, x, v=1):
        if not(0 <= y < height and 0 <= x < width):
            return
        marks[y][x] += v

    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == Paper:
                for dy, dx in dirs:
                    inc(y+dy, x+dx)

    ct = 0
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == Paper and marks[y][x] <= Limit:
                ct += 1
    print(ct)

    # Part 2:
    removed = 0

    while True:
        changed = False
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                if c == Paper and marks[y][x] <= Limit:
                    removed += 1
                    for dy, dx in dirs:
                        inc(dy+y, dx+x, v=-1)
                    row[x] = Empty
                    changed = True

        if not changed:
            break

    print(removed)
