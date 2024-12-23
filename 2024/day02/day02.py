import sys

def safe(levels, tolerance=0, sign=None, prev_val=None):
    if tolerance < 0:
        return False
    elif len(levels) <= tolerance:
        return True

    v = levels[0]
    if prev_val is None:
        return (
            safe(levels[1:], tolerance, None, v)
            or
            # skip v
            safe(levels[1:], tolerance - 1, None, prev_val)
        )
    
    this_sign = v < prev_val
    if sign is None:
        sign = this_sign
        sign_ok = True
        first_empty_sign = True
    else:
        sign_ok = sign == this_sign
        first_empty_sign = False

    return (
        (sign_ok and (1 <= abs(v - prev_val) <= 3) and safe(levels[1:], tolerance, sign, v))
        or
        # skip v
        safe(levels[1:], tolerance - 1, None if first_empty_sign else sign, prev_val)
    )


safe_part_1 = 0
safe_part_2 = 0

for report in sys.stdin:
    levels = [int(l) for l in report.split(' ')]
    if safe(levels, tolerance=0):
        safe_part_1 += 1
    if safe(levels, tolerance=1):
        safe_part_2 += 1

print(safe_part_1)
print(safe_part_2)
