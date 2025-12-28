import sys

def joltage(line):
    # precompute a list where the i'th element is the max element from `line` in
    # any position >= i.
    l2 = list(line)
    for z in range(len(l2) - 2, -1, -1):
        l2[z] = max(l2[z], l2[z+1])

    return max(
        v * 10 + l2[i+1]
        for i, v in enumerate(line[:len(line)-1])
    )

print (
    sum(
        joltage([int(c) for c in line.rstrip()])
        for line in sys.stdin
    )
)
