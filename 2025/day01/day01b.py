from day01 import nums

if __name__ == "__main__":
    s = 100
    t = s * 1000000 + 50
    hits = 0
    for n in nums():
        if n == 0:
            continue
        b = t
        t += n
        e = t

        br = b - b % s
        er = e - e % s

        # How many times did we pass zero?
        hits += abs(er - br) // s

        if e < b:
            # descending case.
            if b % s == 0:
                # don't double-count when starting at 0.
                hits -= 1
            if e % s == 0:
                # detect landing on zero when descending. (e.g., 201 -> 200 are in same bucket modulo s.)
                hits += 1

print(hits)

"""

120 -> 101 = 0
120 -> 100 = 1
120 -> 99 = 1

101 -> 99 = 1
100 -> 99 = 0

220 -> 99 = 2
220 -> 100 = 2
220 -> 101 = 1



70 -> 99 = 0
70 -> 100 = 1
70 -> 101 = 1
70 -> 199 = 1
70 -> 200 = 2


"""