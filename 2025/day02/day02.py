import sys
import itertools

def read_ranges():
    l = sys.stdin.readline()
    l.strip()
    ranges = l.split(",")
    for r in ranges:
        l, r = r.split("-")
        yield int(l), int(r)

def invalids1(lo, hi):
    # cut lo in half and start enumerating possible invalid IDs.
    slo = str(lo)

    if len(slo) == 1:
        candidate = 1
    else:
        candidate = int(slo[:len(slo)//2])

    while (inv := int(str(candidate) * 2)) <= hi:
        if inv >= lo:
            yield inv
        candidate += 1

def invalids2(lo, hi):
    for n in range(lo, hi + 1):
        if is_invalid(str(n)):
            yield n

def is_invalid(ns):
    for l in range(1, len(ns)//2+1):
        m, r = divmod(len(ns), l)
        if r > 0:
            # |ns| not cleanly divisible by l.
            continue
        if ns == ns[:l] * m:
            return True
    return False

if __name__ == "__main__":
    t = 0
    for a, b in read_ranges():
        for i in invalids2(a, b):
            t += i
    print(t)
