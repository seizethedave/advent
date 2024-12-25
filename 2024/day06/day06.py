import sys

def read_map():
    blockades = set()
    height = 0

    for y, line in enumerate(sys.stdin):
        line = line.rstrip()
        width = len(line)
        height = max(height, y + 1)
        for x, ch in enumerate(line):
            if ch == "^":
                guard_pos = (y, x)
            elif ch == "#":
                blockades.add((y, x))

    return guard_pos, (-1, 0), blockades, height, width

def turn_right(dy, dx):
    return {
        (-1, 0): (0, 1),
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0),
    }[(dy, dx)]

def spots_visited(gy, gx, dy, dx, blockades, height, width):
    seen = {(gy, gx)}

    while True:
        ny = gy + dy
        nx = gx + dx

        if not(0 <= ny < height) or not(0 <= nx < width):
            break

        if (ny, nx) in blockades:
            dy, dx = turn_right(dy, dx)
        else:
            gy, gx = ny, nx
            seen.add((gy, gx))
    return len(seen)

def is_inf_route(gy, gx, dy, dx, blockades, height, width):
    seen = {(gy, gx, dy, dx)}
    while True:
        ny = gy + dy
        nx = gx + dx
        if (ny, nx, dy, dx) in seen:
            # It's a cycle.
            return True
        elif not(0 <= ny < height) or not(0 <= nx < width):
            # No cycle: exited the map.
            return False
        if (ny, nx) in blockades:
            dy, dx = turn_right(dy, dx)
        else:
            gy, gx = ny, nx
            seen.add((gy, gx, dy, dx))

def count_inf_routes(gy, gx, dy, dx, blockades, height, width):
    inf = 0
    for y in range(height):
        for x in range(width):
            if (y, x) != (gy-1, gx) and (y, x) not in blockades:
                # Place temp blockage and run it.
                blockades.add((y, x))
                if is_inf_route(gy, gx, dy, dx, blockades, height, width):
                    inf += 1
                blockades.discard((y, x))
    return inf

if __name__ == "__main__":
    (gy, gx), (dy, dx), blockades, height, width = read_map()

    print(spots_visited(gy, gx, dy, dx, blockades, height, width))
    print(count_inf_routes(gy, gx, dy, dx, blockades, height, width))
