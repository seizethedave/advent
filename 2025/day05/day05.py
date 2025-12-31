import sys

def load_input():
    ranges = []
    nums = []
    lines = sys.stdin.readlines()
    seen_blank = False

    for line in lines:
        line = line.rstrip("\n")
        if not line:
            seen_blank = True
            continue

        if not seen_blank:
            lo, hi = line.split("-")
            ranges.append((int(lo), int(hi)))
        else:
            nums.append(int(line))

    return ranges, nums

def in_ranges(ranges, num):
    for (lo, hi) in ranges:
        if lo <= num <= hi:
            return True
    else:
        return False

if __name__ == "__main__":
    ranges, nums = load_input()

    print(
        sum(
            1 for n in nums if in_ranges(ranges, n)
        )
    )
