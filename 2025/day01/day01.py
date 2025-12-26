import sys

def nums():
    for line in sys.stdin:
        line = line.rstrip()
        d, v = line[0], int(line[1:])
        yield v if d == "R" else -v


if __name__ == "__main__":
    s = 100
    t = 50
    hits = 0
    for n in nums():
        t += n
        if t % s == 0:
            hits += 1

    print(hits)
