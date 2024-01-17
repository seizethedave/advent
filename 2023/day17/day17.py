import sys
import heapq

DIR_CHAR = {
    (1, 0): "v",
    (0, 1): ">",
    (-1, 0): "^",
    (0, -1): "<",
}

def next_moves(last_move, y, x, endY, endX, remaining, forward_min_max):
    min_forward, max_forward = forward_min_max
    strides = max_forward - remaining
    backward = tuple(-v for v in last_move)

    def allowed(dy, dx, rem):
        """
        Only allow moves to the target space that satisfy the min_forward moves
        requirement.
        """
        return (
            (y + dy != endY or x + dx != endX)
            or max_forward - rem >= min_forward
        )

    for m in DIR_CHAR.keys():
        dy, dx = m
        if m == last_move:
            if remaining > 0 and allowed(dy, dx, remaining - 1):
                yield (dy, dx, remaining - 1)
        elif m == backward:
            # Can't back up.
            pass
        elif strides >= min_forward:
            # Turning. By emitting this move we've used up one of the
            # MAX_FORWARD movements.
            if allowed(dy, dx, max_forward - 1):
                yield (dy, dx, max_forward - 1)

def dist(y1: int, x1: int, y2: int, x2: int) -> int:
    return abs(y2 - y1) + abs(x2 - x1)

def search(grid, startY, startX, endY, endX, forward_min_max):
    height = len(grid)
    width = len(grid[0])
    def get(yy, xx):
        if not(0 <= yy < height and 0 <= xx < width):
            raise IndexError()
        return int(grid[yy][xx])

    visited = set()
    fringe = [(0, 0, (startY, startX), (0, 0), 0)]

    while fringe:
        (_, heat, (vy, vx), last_move, remaining) = heapq.heappop(fringe)

        if vy == endY and vx == endX:
            return heat

        if (vy, vx, last_move, remaining) in visited:
            continue
        visited.add((vy, vx, last_move, remaining))

        for dy, dx, nrem in next_moves(last_move, vy, vx, endY, endX, remaining, forward_min_max):
            ny = vy + dy
            nx = vx + dx
            try:
                nheat = heat + get(ny, nx)
            except IndexError:
                continue
            h = nheat + dist(ny, nx, endY, endX)
            heapq.heappush(fringe, (h, nheat, (ny, nx), (dy, dx), nrem))

if __name__ == "__main__":
    grid = [line.rstrip() for line in sys.stdin]
    height = len(grid)
    width = len(grid[0])
    print(search(grid, 0, 0, height - 1, width - 1, (0, 3)))
    print(search(grid, 0, 0, height - 1, width - 1, (4, 10)))
