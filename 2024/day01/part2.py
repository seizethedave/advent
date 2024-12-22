import sys
from collections import Counter

a = []
b = Counter()

for line in sys.stdin:
    left, right = line.split()
    a.append(int(left))
    b[int(right)] += 1

print(sum(i * b[i] for i in a))
