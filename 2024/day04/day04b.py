import sys
from collections import Counter

def contains(g, word, y, x, dy, dx):
    for c in word:
        if not(0 <= y < len(g) and 0 <= x < len(g[y])):
            return False
        if g[y][x] != c:
            return False
        y += dy
        x += dx
    else:
        return True

def scan(g):
    hits = Counter()
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            for dy, dx in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
                if contains(g, 'MAS', y, x, dy, dx):
                    hits[(y+dy, x+dx)] += 1 # the location of the 'A'
    return len([v for v in hits.values() if v == 2]) # number of 'A' locations encountered twice

grid = []
for row in sys.stdin:
    grid.append(row.rstrip("\n"))
print(scan(grid))
