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

if __name__ == "__main__":
    ranges, nums = load_input()

    print(
        sum(
            1 for n in nums if any(
                lo <= n <= hi for (lo, hi) in ranges
            )
        )
    )
