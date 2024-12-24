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

if __name__ == "__main__":
    (gy, gx), (dy, dx), blockades, height, width = read_map()
    seen = {(gy, gx)}

    while True:
        ny = gy + dy
        nx = gx + dx

        if not (0 <= ny < height) or not(0 <= nx < width):
            break

        if (ny, nx) in blockades:
            dy, dx = turn_right(dy, dx)
        else:
            gy, gx = ny, nx
            seen.add((gy, gx))

    print(len(seen))

