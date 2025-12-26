import sys
import math

def read_ranges():
    l = sys.stdin.readline()
    l.strip()
    ranges = l.split(",")
    for r in ranges:
        l, r = r.split("-")
        yield int(l), int(r)

def invalids(lo, hi):
    # cut lo in half and start enumerating possible invalid IDs.
    slo = str(lo)

    if len(slo) == 1:
        candidate = 1
    else:
        candidate = int(slo[:len(slo)//2])

    while True:
        inv = int(str(candidate) * 2)
        candidate += 1
        if inv < lo:
            continue
        elif inv > hi:
            break
        yield inv


if __name__ == "__main__":
    t = 0
    for a, b in read_ranges():
        for i in invalids(a, b):
            t += i
    print(t)
