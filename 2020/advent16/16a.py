import sys
import re
import pprint

rules = []

def load_input():
    for line in sys.stdin:
        if line == "\n":
            break
        rules.extend(
            (int(a), int(b)) for a, b in re.findall("(\d+)-(\d+)", line)
        )
    # Skip until start of "nearby tickets" data.
    sys.stdin.readline()
    sys.stdin.readline()
    sys.stdin.readline()
    sys.stdin.readline()

load_input()

def invalid(n):
    return not any(lo <= n <= hi for lo, hi in rules)

score = 0
for line in sys.stdin:
    items = [int(n) for n in line.split(",")]
    score += sum(filter(invalid, items))
print(score)
