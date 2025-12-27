import sys

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

    while (inv := int(str(candidate) * 2)) <= hi:
        if inv >= lo:
            yield inv
        candidate += 1

if __name__ == "__main__":
    t = 0
    for a, b in read_ranges():
        for i in invalids(a, b):
            t += i
    print(t)
