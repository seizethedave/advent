import sys

def is_valid(testval, tally, operands):
    if not operands:
        return tally == testval
    if tally > testval:
        # Already too large.
        return False
    n, *operands = operands
    return (
        is_valid(testval, int(str(tally) + str(n)), operands) # (part 2)
        or is_valid(testval, tally * n, operands)
        or is_valid(testval, tally + n, operands)
    )

def sum_valid(inputs):
    return sum(
        testval for testval, operands in inputs
        if is_valid(testval, operands[0], operands[1:])
    )

if __name__ == "__main__":
    inputs = []
    for line in sys.stdin:
        l, r = line.split(": ")
        testval = int(l)
        operands = [int(v) for v in r.split()]
        inputs.append((testval, operands))

    print(sum_valid(inputs))
