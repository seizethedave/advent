import sys

a = []
b = []

for line in sys.stdin:
    left, right = line.split()
    a.append(int(left))
    b.append(int(right))

a.sort()
b.sort()

print(sum(abs(i - j) for i, j in zip(a, b)))
