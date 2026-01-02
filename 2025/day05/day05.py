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

def merge(ranges):
    output = []

    for (lo2, hi2) in sorted(ranges):
        try:
            lo1, hi1 = output.pop()
        except IndexError:
            output.append((lo2, hi2))
        else:
            if lo2 <= hi1 + 1:
                output.append((lo1, max(hi1, hi2)))
            else:
                # Not overlapping.
                output.append((lo1, hi1))
                output.append((lo2, hi2))

    return output


if __name__ == "__main__":
    ranges, nums = load_input()

    print(
        sum(
            1 for n in nums if any(
                lo <= n <= hi for (lo, hi) in ranges
            )
        )
    )

    print(sum(hi - lo + 1 for lo, hi in merge(ranges)))
