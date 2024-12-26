import sys
from collections import defaultdict
import itertools

def antinodes(points):
    for (y1, x1), (y2, x2) in itertools.combinations(points, 2):
        sy, sx = y2-y1, x2-x1
        yield (y1-sy, x1-sx)
        yield (y2+sy, x2+sx)

def antinodes2(points, height, width):
    for (y1, x1), (y2, x2) in itertools.combinations(points, 2):
        sy, sx = y2-y1, x2-x1
        yield (y1, x1)
        yield (y2, x2)
        for i in itertools.count(start=1):
            c1y, c1x = (y1-i*sy, x1-i*sx)
            c2y, c2x = (y2+i*sy, x2+i*sx)
            if in1 := 0 <= c1y < height and 0 <= c1x < width:
                yield (c1y, c1x)
            if in2 := 0 <= c2y < height and 0 <= c2x < width:
                yield (c2y, c2x)
            if not in1 and not in2:
                break

if __name__ == "__main__":
    height = 0
    width = 0
    points = defaultdict(list)
    for y, line in enumerate(sys.stdin):
        line = line.rstrip()
        height = y + 1
        width = len(line)
        for x, ch in enumerate(line):
            if ch != ".":
                points[ch].append((y, x))

    a = set()
    for ch, pts in points.items():
        for y, x in antinodes(pts):
            if 0 <= y < height and 0 <= x < width:
                a.add((y, x))
    print(len(a))

    a = set()
    for ch, pts in points.items():
        for y, x in antinodes2(pts, height, width):
            a.add((y, x))
    print(len(a))
