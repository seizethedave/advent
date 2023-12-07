import sys
import math

def count_solutions(time, distance):
    ct = 0
    for i in range(1, time):
        if (time - i) * i > distance:
            ct += 1
    return ct

if __name__ == "__main__":
    tl, dl = list(sys.stdin)
    times = [int(v) for v in tl.split()[1:]]
    distances = [int(v) for v in dl.split()[1:]]
    spec = zip(times, distances)
    print(math.prod(count_solutions(t, d) for t, d in spec))

    # Part 2: join up the numbers and re-run them.
    t = int("".join(str(n) for n in times))
    d = int("".join(str(n) for n in distances))
    print(count_solutions(t, d))
    