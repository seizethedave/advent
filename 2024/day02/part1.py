import sys
from itertools import pairwise

def safe(levels):
    sign = None
    for a, b in pairwise(levels):
        if sign is None:
            sign = a > b
        elif sign != (a > b):
            return False
        if not 1 <= abs(a - b) <= 3:
            return False
    else:
        return True

num_safe = 0

for report in sys.stdin:
    if safe(int(l) for l in report.split(' ')):
        num_safe += 1

print(num_safe)
