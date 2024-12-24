import sys
from collections import Counter, defaultdict

def make_ordering(update, orderings):
    active_set = set(update)

    g = set()
    pointing = defaultdict(set)
    degree = Counter()
    for a, b in orderings:
        if a not in active_set or b not in active_set:
            continue

        degree[b] += 1
        pointing[a].add(b)
        g.add(a)
        g.add(b)

    ready = set(n for n in g if degree[n] == 0)
    order_num = 0
    ordering = {}

    while ready:
        n = ready.pop()
        ordering[n] = order_num
        order_num += 1
        for other in pointing[n]:
            degree[other] -= 1
            if degree[other] == 0:
                ready.add(other)
    
    return ordering

def in_order(update, orderings):
    prev = -1
    for u in update:
        o = orderings[u]
        if o <= prev:
            return False
        prev = o
    else:
        return True

if __name__ == "__main__":
    order_pairs = []
    updates = []
    seen_blank = False

    for line in sys.stdin:
        line = line.rstrip()
        if not line:
            seen_blank = True
            continue

        if not seen_blank:
            a, b = line.split("|")
            order_pairs.append((int(a), int(b)))
        else:
            updates.append([int(n) for n in line.split(",")])

    s = 0
    incorrect = 0

    for update in updates:
        ordering = make_ordering(update, order_pairs)
        if in_order(update, ordering):
            s += update[len(update) // 2]
        else:
            update = sorted(update, key=lambda v: ordering[v])
            incorrect += update[len(update) // 2]

    print(s)
    print(incorrect)