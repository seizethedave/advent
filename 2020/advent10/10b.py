import sys
from functools import lru_cache

diff_max = 3
jolts = sorted(int(j) for j in sys.stdin)
jolts.insert(0, 0)
jolts.append(jolts[-1] + diff_max)

@lru_cache
def search(i):
    if i >= len(jolts) - 1:
        return 1

    count = 0

    for j in range(i + 1, i + 1 + diff_max):
        try:
            if jolts[j] - jolts[i] <= diff_max:
                count += search(j)
        except IndexError:
            break

    return count

print(search(0))