import sys

MOVES = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}

MOVES_NUM = [MOVES['R'], MOVES['D'], MOVES['L'], MOVES['U']]

def decode_triple(d, n, c):
    return MOVES[d], n

def decode_triple_hex(d, n, c):
    return MOVES_NUM[int(c[-1])], int(c[:5], 16)

def iter_input():
    for line in sys.stdin:
        d, n, c = line.split()
        yield d, int(n), c.strip('()#')

def points(input_triples, decoder):
    path_len = 0
    y = 0
    x = 0
    pts = [(0, 0)]
    for t in input_triples:
        (dy, dx), steps = decoder(*t)
        y += steps * dy
        x += steps * dx
        path_len += steps
        pts.append((y, x))

    return pts, path_len

def shoelace_trapezoid_area(vertices):
    n = len(vertices)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += (vertices[i][1] + vertices[j][1]) * (vertices[j][0] - vertices[i][0])
    return abs(area // 2)

if __name__ == "__main__":
    inputs = list(iter_input())

    pts, path_len = points(inputs, decoder=decode_triple)
    print(shoelace_trapezoid_area(pts) + path_len // 2 + 1)

    pts, path_len = points(inputs, decoder=decode_triple_hex)
    print(shoelace_trapezoid_area(pts) + path_len // 2 + 1)
