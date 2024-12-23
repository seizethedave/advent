import sys
import re

s = 0
enabled = True

for line in sys.stdin:
    for m in re.findall(r"(mul)\(([0-9]{1,3}),([0-9]{1,3})\)|(do)\(\)|(don't)\(\)", line):
        a, b, c, d, e = m
        if a == "mul":
            if enabled:
                b = int(b)
                c = int(c)
                s += (b * c)
        elif d == "do":
            enabled = True
        elif e == "don't":
            enabled = False

print(s)
