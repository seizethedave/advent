import sys
import operator
from itertools import count

sys.stdin.readline() # Skip first line.

buses = [
    (1 if c == "x" else int(c))
    for c in sys.stdin.readline().split(",")
]

"""
Build [(index, bus), (index, bus), ...]
Use the largest bus number to generate candidates.
Consider the buses in decreasing order of size to eliminate candidates more quickly.
"""

constraints = sorted(list(enumerate(buses)), key=operator.itemgetter(1), reverse=True)
(i, biggest), constraints = constraints[0], constraints[1:]

lo = 100000000000000
n = (lo - (lo % biggest))
it = 0
while True:
    it += 1
    if it % 1000000 == 0:
        print(it, n)
    for j, val in constraints:
        if (n + j - i) % val != 0:
            break
    else:
        print(n - i)
        break
    n += biggest