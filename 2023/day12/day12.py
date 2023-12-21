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
        return 1 if spec_empty else 0
    if spec_empty:
        return 0 if (Damaged in springs) else 1

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
    
def embiggen_spec(spec):
    bigspec = []
    for _ in range(5):
        bigspec.extend(spec)
    return tuple(bigspec)

if __name__ == "__main__":
    specs = list(iter_specs())

    #for s, spec in specs:
    #    print(s, spec, count_arrangements(s, spec, 0))
    print(sum(count_arrangements(s, spec) for s, spec in specs))

    big_specs = [
        ("?".join([s] * 5), embiggen_spec(spec))
        for s, spec in specs
    ]

    print(sum(count_arrangements(s, spec) for s, spec in big_specs))
