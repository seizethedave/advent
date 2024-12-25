import sys

def is_valid(testval, operands, tally=0):
    if not tally:
        tally, *operands = operands
    if not operands:
        return tally == testval
    if tally > testval:
        # Already too large.
        return False
    n, *operands = operands
    return (
        is_valid(testval, operands, tally + n) or
        is_valid(testval, operands, tally * n) or
        # part 2:
        is_valid(testval, operands, int(str(tally) + str(n)))
    )

def sum_valid(inputs):
    return sum(testval for testval, operands in inputs if is_valid(testval, operands))

if __name__ == "__main__":
    inputs = []
    for line in sys.stdin:
        l, r = line.split(": ")
        testval = int(l)
        operands = [int(v) for v in r.split()]
        inputs.append((testval, operands))

    print(sum_valid(inputs))

    