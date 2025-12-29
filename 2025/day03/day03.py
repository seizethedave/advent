import sys
from functools import lru_cache

ninf = float('-inf')

def joltage2(items, digits):
    @lru_cache
    def joltage_recursive(i, d):
        if d == 0:
            # it's OK to not consume all items.
            return 0
        if d == 1 and i == len(items) - 1:
            return items[i]
        if i >= len(items):
            return ninf

        return max(
            # items_i included
            10 ** (d-1) * items[i] + joltage_recursive(i+1, d - 1),
            # items_i skipped
            joltage_recursive(i+1, d)
        )

    return joltage_recursive(0, digits)

print (
    sum(
        joltage2([int(c) for c in line.rstrip()], 12)
        for line in sys.stdin
    )
)
