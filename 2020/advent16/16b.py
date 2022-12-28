import sys
import re
import math

rules = []
my_ticket = []

def load_input():
    for line in sys.stdin:
        if line == "\n":
            break
        name, values = line.split(":")
        rules.append((
            name,
            [(int(a), int(b)) for a, b in re.findall("(\d+)-(\d+)", values)]
        ))
    # Skip until start of "nearby tickets" data.
    sys.stdin.readline()
    my_ticket.extend(int(x) for x in sys.stdin.readline().split(","))
    sys.stdin.readline()
    sys.stdin.readline()

load_input()

fields = [f for f, vals in rules]
candidates = []
for i in range(len(my_ticket)):
    candidates.append(set(fields))

def valid_for_rule(value, rule):
    name, intervals = rule
    return any(lo <= value <= hi for lo, hi in intervals)

def valid(n):
    return any(valid_for_rule(n, r) for r in rules)

def illegal_rules(n):
    """
    Yields the names of all rules that this value would be illegal for.
    """
    for name, intervals in rules:
        for lo, hi in intervals:
            if lo <= n <= hi:
                break # legal.
        else:
            yield name # None legal for this rule.

final_defs = [None] * len(my_ticket)

def discard_candidate(index, rule_name):
    # Every time we discard a candidate rule, if we drop to 1 rule for the index, we can
    # recursively eliminate that rule from all other indices. (which may drop to 1...)
    candidates[index].discard(rule_name)
    if len(candidates[index]) == 1 and not final_defs[index]:
        remaining_rule = list(candidates[index])[0]
        final_defs[index] = remaining_rule
        for i in range(len(candidates)):
            if i != index:
                discard_candidate(i, remaining_rule)

for line in sys.stdin:
    items = [int(n) for n in line.split(",")]
    if any(not valid(x) for x in items):
        continue
    for i, item in enumerate(items):
        for rule_name in illegal_rules(item):
            discard_candidate(i, rule_name)

print(math.prod(
    v for k, v in zip(final_defs, my_ticket)
    if k.startswith("departure")
))