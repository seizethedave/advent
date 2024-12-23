import sys

def contains(g, y, x, dy, dx):
    for c in 'XMAS':
        if not(0 <= y < len(g) and 0 <= x < len(g[y])):
            return False
        if g[y][x] != c:
            return False
        y += dy
        x += dx
    else:
        return True

def scan(g):
    ct = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            for dy, dx in [
                (0, 1), (1, 0), (0, -1), (-1, 0),
                (1, 1), (1, -1), (-1, -1), (-1, 1)
            ]:
                if contains(g, y, x, dy, dx):
                    ct += 1
    return ct

grid = []
for row in sys.stdin:
    grid.append(row.rstrip("\n"))
print(scan(grid))
