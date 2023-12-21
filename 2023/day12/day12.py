import sys
from functools import lru_cache

Operational = "."
Damaged = "#"
Unknown = "?"

def iter_specs():
    for line in sys.stdin:
        springs, right = line.strip().split(" ")
        spec = tuple(int(c) for c in right.split(","))
        yield springs, spec

@lru_cache
def count_arrangements(springs: str, spec, terminal=False):
    springs_empty = (springs == "")
    spec_empty = len(spec) == 0

    if springs_empty:
        return 0 if not spec_empty else 1
    if spec_empty:
        return 0 if Damaged in springs else 1

    def skip():
        return count_arrangements(springs[1:], spec, False)

    def consume():
        if terminal:
            # Can't consume a # if we're terminal.
            return 0

        match, *rest = spec
        if Operational in springs[:match] or len(springs) < match:
            return 0

        # We consumed it.
        return count_arrangements(springs[match:], tuple(rest), True)

    if springs.startswith(Operational):
        return skip()
    elif springs.startswith(Unknown):
        return skip() + consume()
    elif springs.startswith(Damaged):
        return consume()

if __name__ == "__main__":
    specs = list(iter_specs())

    print(sum(count_arrangements(s, spec) for s, spec in specs))

    big_specs = [
        (Unknown.join([s] * 5), spec * 5)
        for s, spec in specs
    ]

    print(sum(count_arrangements(s, spec) for s, spec in big_specs))
