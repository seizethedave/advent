import sys

class Map:
    def __init__(self):
        self.ranges = []

    def add_range(self, dest, src, length):
        self.ranges.append((dest, src, length))

    def translate(self, value):
        for (d, s, l) in self.ranges:
            if s <= value < s + l:
                return d + value - s
        else:
            return value

if __name__ == "__main__":
    maps = []

    for line in sys.stdin:
        line = line.strip()
        if line.startswith("seeds:"):
            r = line[7:]
            seeds = [int(v) for v in r.split(" ")]
        elif line.endswith("map:"):
            thismap = Map()
            maps.append(thismap)
        elif line == "":
            pass
        else:
            # dest src length triple.
            dest, src, length = [int(v) for v in line.split(" ")]
            thismap.add_range(dest, src, length)

    def seed_to_loc(s):
        spot = s
        for m in maps:
            spot = m.translate(spot)
        return spot
        
    locs = []

    # Now go from seeds to location.
    for s in seeds:
        locs.append(seed_to_loc(s))

    print(min(locs))

    # Part 2:

    def pairwise(it):
        while True:
            try:
                yield (next(it), next(it))
            except StopIteration:
                break
        
    range_seeds = list(pairwise(iter(seeds)))

    best = 9999999999999999999
    for (start, stride) in range_seeds:
        best = min(
            best,
            min(seed_to_loc(i) for i in range(start, start+stride)))
        print("so far: {}".format(best))

    print(best)