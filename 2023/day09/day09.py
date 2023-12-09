import sys

def pairwise(it):
    left = next(it)
    for right in it:
        yield (left, right)
        left = right

def next_from_stack(s, depth=0):
    if depth == len(s) - 1:
        return 0
    return s[depth][-1] + next_from_stack(s, depth + 1)

def prev_from_stack(s, depth=0):
    if depth == len(s) - 1:
        return 0
    return s[depth][0] - prev_from_stack(s, depth + 1)

def compute_next(values, finalizer_func):
    # Build a stack of difference lists until they're all zero, then invoke the
    # provided recursive func to carry out the last extension part.
    stk = [values]
    top = values
    while True:
        result = []
        all_zeroes = True
        for l, r in pairwise(iter(top)):
            diff = r - l
            result.append(diff)
            if diff != 0:
                all_zeroes = False
        stk.append(result)
        top = result
        if all_zeroes:
            return finalizer_func(stk)
    
if __name__ == "__main__":
    def iter_ints():
        for line in sys.stdin:
            yield [int(v) for v in line.split()]

    inputs = list(iter_ints())

    print(sum(compute_next(i, next_from_stack) for i in inputs))
    print(sum(compute_next(i, prev_from_stack) for i in inputs))
