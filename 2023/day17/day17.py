import sys
import heapq
from itertools import pairwise

MAX_FORWARD = 3

DIR_CHAR = {
    (1, 0): "v",
    (0, 1): ">",
    (-1, 0): "^",
    (0, -1): "<",
}

def next_moves(last_move, remaining):
    for m in DIR_CHAR.keys():
        dy, dx = m
        if m == last_move:
            if remaining > 0:
                yield (dy, dx, remaining - 1)
        elif m == (-last_move[0], -last_move[1]):
            # Can't back up.
            pass
        else:
            # Turning.
            yield (dy, dx, MAX_FORWARD - 1)

def search(grid, startY, startX, endY, endX):
    height = len(grid)
    width = len(grid[0])
    def get(yy, xx):
        if not(0 <= yy < height and 0 <= xx < width):
            raise IndexError()
        return int(grid[yy][xx])

    visited = set()
    fringe = [(0, (startY, startX), [(startY, startX)], (0, 0), 0)]

    while fringe:
        (heat, (vy, vx), path, last_move, remaining) = heapq.heappop(fringe)
        if vy == endY and vx == endX:
            return heat
        if (vy, vx, last_move, remaining) in visited:
            continue
        visited.add((vy, vx, last_move, remaining))

        for dy, dx, nrem in next_moves(last_move, remaining):
            ny = vy + dy
            nx = vx + dx
            try:
                nheat = get(ny, nx)
            except IndexError:
                continue
            heapq.heappush(fringe, (heat + nheat, (ny, nx), path + [(ny, nx)], (dy, dx), nrem))

if __name__ == "__main__":
    grid = [line.rstrip() for line in sys.stdin]
    height = len(grid)
    width = len(grid[0])
    print(search(grid, 0, 0, height - 1, width - 1))